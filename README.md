# Miles_Stone_Interactive_Notes

# Description
This repository contains the program that convert the video file into an interactive note in just a few clicks. It also contains the bi-weekly progress for this project and the video tutorials for tasting the program. The program is a simple UI using Streamlit dashboard in python as a prototype to shows the interactive notes.

# Installation
```python -m venv venv # Create virtual environment
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt # Install dependencies
streamlit run UIprototype.py # Run the application
```

# Features
### Insert the video that want the program to process
<img width="929" height="514" alt="image" src="https://github.com/user-attachments/assets/544a3f33-5752-473d-b4ad-3b3a6d3ca25a" />

### Then click the process video button
<img width="914" height="809" alt="image" src="https://github.com/user-attachments/assets/04c9401c-2560-43ba-86d6-5475dc02b13b" />

### The program will run automatically to transcribe the text and print out the transcript
<img width="933" height="838" alt="image" src="https://github.com/user-attachments/assets/b8db6344-1de3-44ea-8957-12a5243e80f2" />

### After Transcription, the program will polished the transcribed text and print out the polished note
<img width="1706" height="705" alt="image" src="https://github.com/user-attachments/assets/6c760be4-137d-44d5-8d0c-29552e910dd6" />

# Limitations
- Whisper transcription can be slow on CPU
- Large video files may cause delays
- UI is a prototype and may lack advanced navigation features


