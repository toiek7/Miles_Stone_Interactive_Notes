import streamlit as st
import tempfile, subprocess, json, math
from pathlib import Path
import whisper
import openai 
from gpt4all import GPT4All
import os
import re

# Initialize OpenAI client use with server
#client = openai.OpenAI(api_key='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')
#openai.api_key = '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'
#model = GPT4All("gpt4all-lora-quantized")  # local LLM for polishing
model_path = r"C:\Users\Toiek\gpt4all\Meta-Llama-3-8B-Instruct-Q6_K.gguf"
model = GPT4All(model_path)

st.set_page_config(page_title="Video to Notes", layout="wide")
st.title("📹 Teaching Video → Structured Notes")

# Initialize local models
@st.cache_resource
def load_models():
    try:
        whisper_model = whisper.load_model("medium")  # Whisper for transcription
        model_path = r"C:\Users\Toiek\gpt4all\Meta-Llama-3-8B-Instruct-Q6_K.gguf"  # update path if needed
        gpt_model = GPT4All(model_path)  # GPT4All for polishing notes
        st.success("✅ Successfully loaded model!")
        return whisper_model, gpt_model
    except Exception as e:
        st.error(f"❌ Failed to load model: {e}")
        st.stop()

whisper_model, gpt_model = load_models()

# -------- Helper Functions --------
def split_video(video_path: str, segment_length_sec: int = 300):
    """Split video into smaller segments using ffmpeg."""
    base = os.path.splitext(video_path)[0]
    os.makedirs(f"{base}_segments", exist_ok=True)
    output_pattern = f"{base}_segments/segment_%03d.mp4"

    cmd = [
        "ffmpeg", "-i", video_path, "-c", "copy",
        "-map", "0", "-f", "segment",
        "-segment_time", str(segment_length_sec),
        output_pattern
    ]
    subprocess.run(cmd, check=True)
    segments = [os.path.join(f"{base}_segments", f) for f in os.listdir(f"{base}_segments") if f.endswith(".mp4")]
    segments.sort()
    return segments

def run_local_whisper(video_file: str):
    """Transcribe video locally using Whisper."""
    result = whisper_model.transcribe(video_file)
    segments = []
    for seg in result["segments"]:
        segments.append({
            "id": seg["id"],
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"].strip()
        })
    return segments

def chunk_segments(segments, max_words=500):
    """Combine short segments into manageable chunks."""
    chunks, current_chunk, word_count = [], [], 0
    for seg in segments:
        words = seg["text"].split()
        if word_count + len(words) > max_words and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk, word_count = [], 0
        current_chunk.append(seg["text"])
        word_count += len(words)
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def polish_with_gpt4all(model, text_chunk: str):
    """Use GPT4All local model to polish transcript into structured notes."""
    prompt = f"""
    You are a professional teaching assistant.
    Rewrite the following transcript into clear, structured teaching notes:
    - Fix grammar and punctuation
    - Remove filler words
    - Use numbered steps and in each step explain clearly the concepts
    - each bullet point should represent a key idea or step not everything that was said
    - each step then explain each step in detail not just one line and then move on to the next step
    - in each bullet point use sub-bullets to explain the concept in detail
    - Ensure logical flow and coherence
    - Add examples where applicable
    - Add section headings where needed
    - Keep only important teaching content
    - summarize it don't just rewrite the text
    - get rid of unnecessary details like all of the text that does not add to the teaching value
    - don't write every word that was said, summarize and condense the information
    - Do not include explanations, greetings, or meta comments.


    Transcript:
    {text_chunk}
    """
    with model.chat_session() as session:
        response = session.generate(prompt, max_tokens=600, temp=0.7)
    # ---- CLEANUP STEP ----
    clean_text = str(response)

    # Remove chat artifacts or unwanted tags
    clean_text = re.sub(r"<\|.*?\|>", "", clean_text)       # remove tokens like <|eot_id|>
    clean_text = re.sub(r"(?i)^(?:assistant:|system:|user:)\s*", "", clean_text)
    clean_text = re.sub(r"(Please let me know.*|I'm glad.*|Would you like.*)$", "", clean_text, flags=re.I)
    clean_text = clean_text.strip()
    return clean_text

# -------- Streamlit UI --------
uploaded_file = st.file_uploader("Upload your video", type=["mp4", "mov", "mkv"])

if uploaded_file:
    st.video(uploaded_file)

    if st.button("Process Video"):
        with st.spinner("Saving and processing video..."):
            temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            temp_video.write(uploaded_file.read())
            temp_video.close()

        with st.spinner("Splitting video into 5-minute segments..."):
            video_segments = split_video(temp_video.name, segment_length_sec=300)
            st.write(f"Video split into {len(video_segments)} segments.")

        all_segments = []
        for i, seg_path in enumerate(video_segments, start=1):
            st.info(f"Transcribing segment {i}/{len(video_segments)}...")
            seg_text = run_local_whisper(seg_path)
            all_segments.extend(seg_text)

        st.success("✅ Transcription complete!")

        # Combine all text segments into one string
        transcript_text = "\n".join([seg["text"] for seg in all_segments if "text" in seg])

        # Show transcript
        st.subheader("🗒️ Transcript")
        formatted_segments = [
            f"[{math.floor(seg['start']//60):02d}:{math.floor(seg['start']%60):02d} - "
            f"{math.floor(seg['end']//60):02d}:{math.floor(seg['end']%60):02d}] {seg['text']}"
            for seg in all_segments
        ]
        st.text_area("Transcript text:", formatted_segments, height=400)

        with st.spinner("Polishing transcript with GPT4All..."):
            chunks = chunk_segments(all_segments, max_words=500)
            st.write(f"Transcript split into {len(chunks)} chunks for processing.")
            polished_chunks = []
            progress_bar = st.progress(0)

            for i, chunk in enumerate(chunks, start=1):
                polished = polish_with_gpt4all(gpt_model, chunk)
                polished_chunks.append(polished)
                progress_bar.progress(i / len(chunks))

            notes_text = "\n\n".join(polished_chunks)

        st.success("✅ Notes generated!")

        st.subheader("Structured Notes")
        st.markdown(notes_text)

        st.download_button(
            "Download Notes (Markdown)",
            notes_text,
            file_name="notes.md",
            mime="text/markdown"
        )
