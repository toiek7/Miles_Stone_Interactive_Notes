# Test on output/work_20251209_025156

from document_generator.create_final_draft import create_final_draft_json

grouped_data = [
  {
    "group_id": 0,
    "group_start_time": "0:00:00",
    "group_end_time": "0:00:30",
    "group_summary": "The video segment discusses Machine Learning (ML), a method that enables computers to perform tasks without explicit programming by using algorithms trained with large datasets—a process analogous to organic life's experience-based learning. Arthur Samuel, an IBM researcher in the late 1950s who was pioneering artificial intelligence through checkers games, coined this term and conceptualized its foundation for modern ML systems today.\n\nThe key concepts highlighted include:\n\n1. The essence of Machine Learning as a data-driven approach where computers learn from experience rather than being explicitly programmed to execute specific tasks (0:00:05 - 0:00:26). This learning is iterative, with algorithms analyzing and improving upon inputted datasets over time.\n   \n2. The historical context of ML's development at IBM by Arthur Samuel in the late '50s sets a precedent for its evolution into contemporary applications (0:00:16 - 0:00:21). This underscs how far-reaching and transformative this technology has become.\n   \n3. The practical application of ML is evident today, with predictive models integrated within everyday products to perform essential functions such as data classification (e.g., identifying cars on the road) without direct human input for each task execution—showcasing how machines can autonomously interpret and act upon information they have learned from vast amounts of training data (0:00:26 - 0:00:30).\n\nThe segment emphasizes ML's impactful role in automating complex tasks, its historical roots at IBM under Arthur Samuel’s guidance, and how it has become an integral part of modern technology through the use of predictive models for data classification.",
    "group_segments": [
      {
        "start": "0:00:00",
        "end": "0:00:05",
        "text": "Machine Learning, T-Shake computer how to perform a task without explicitly programming it to",
        "label": "introduction"
      },
      {
        "start": "0:00:05",
        "end": "0:00:10",
        "text": "perform said task. Instead, feed data into an algorithm to gradually improve outcomes with",
        "label": "explanation"
      },
      {
        "start": "0:00:10",
        "end": "0:00:16",
        "text": "experience, similar to how organic life learns. The term was coined in 1959 by Arthur Samuel",
        "label": "explanation"
      },
      {
        "start": "0:00:16",
        "end": "0:00:21",
        "text": "at IBM, who was developing artificial intelligence that could play checkers. Half a century later,",
        "label": "introduction"
      },
      {
        "start": "0:00:21",
        "end": "0:00:26",
        "text": "and predictive models are embedded in many of the products we use every day, which perform two",
        "label": "explanation"
      },
      {
        "start": "0:00:26",
        "end": "0:00:30",
        "text": "fundamental jobs. One is to classify data like is there another car on the road, or does this",
        "label": "explanation"
      }
    ]
  },
  {
    "group_id": 1,
    "group_start_time": "0:00:36",
    "group_end_time": "0:00:41",
    "group_summary": "or which YouTube video do you want to watch next. The first step in the process is to acquire and",
    "group_segments": [
      {
        "start": "0:00:36",
        "end": "0:00:41",
        "text": "or which YouTube video do you want to watch next. The first step in the process is to acquire and",
        "label": "transition"
      }
    ]
  },
  {
    "group_id": 2,
    "group_start_time": "0:00:41",
    "group_end_time": "0:01:56",
    "group_summary": "This instructional video segment focuses on Machine Learning (ML), a method that enables computers to perform tasks without explicit programming by using algorithms trained with large datasets for predictive accuracy improvement. Key concepts include data quality, where the adage \"garbage in, garbage out\" highlights the importance of clean and representative training data; feature engineering—a critical task performed by data scientists who transform raw information into features that effectively capture problem essentials to feed algorithms like linear or logistic regression models as well as more complex structures such as decision trees.\n\nThe segment also delves into advanced techniques, particularly convolutional neural networks (CNNs), which are adept at handling image and natural language data by automatically creating additional relevant features for learning tasks—a process that is impractical with manual engineering due to the complexity of these types of datasets. The core idea here revolves around algorithms iteratively refining their predictions against an error function, such as accuracy in classification problems or mean absolute error in regression scenarios; this feedback loop ensures continuous enhancement of model performance over time through exposure to more data and subsequent learning iterations.\n\nThe video underscs the importance of a clear separation between training sets (used for building models) and testing datasets (for validating accuracy), which is essential for assessing how well an ML algorithm generalizes beyond its initial dataset—a critical factor in determining real-world applicability. Overall, this segment educates viewers on foundational aspects of machine learning: data preparation, feature engineering, model selection and training processes, as well as the evaluation metrics that drive iterative improvements for predictive models across various types of problems including classification and regression tasks with complex input forms like images or textual content.",
    "group_segments": [
      {
        "start": "0:00:41",
        "end": "0:00:45",
        "text": "clean up data, lots and lots of data. The better the data represents the problem, the better the",
        "label": "tip"
      },
      {
        "start": "0:00:45",
        "end": "0:00:50",
        "text": "results. Garbage in, garbage out. The data needs to have some kind of signal to be valuable to",
        "label": "tip"
      },
      {
        "start": "0:00:50",
        "end": "0:00:55",
        "text": "the algorithm for making predictions. And data scientists perform a job called feature engineering",
        "label": "explanation"
      },
      {
        "start": "0:00:55",
        "end": "0:01:00",
        "text": "to transform raw data into features that better represent the underlying problem. The next step",
        "label": "explanation"
      },
      {
        "start": "0:01:00",
        "end": "0:01:05",
        "text": "is to separate the data into a training set and testing set. The training data is fed into an",
        "label": "explanation"
      },
      {
        "start": "0:01:05",
        "end": "0:01:11",
        "text": "algorithm to build a model, then the testing data is used to validate the accuracy or error of the",
        "label": "explanation"
      },
      {
        "start": "0:01:11",
        "end": "0:01:16",
        "text": "model. The next step is to choose an algorithm, which might be a simple statistical model like",
        "label": "explanation"
      },
      {
        "start": "0:01:16",
        "end": "0:01:20",
        "text": "linear or logistic regression, or a decision tree that assigns different weights to features in",
        "label": "explanation"
      },
      {
        "start": "0:01:21",
        "end": "0:01:26",
        "text": "the data, or you might get fancy with a convolutional neural network, which is an algorithm that also",
        "label": "explanation"
      },
      {
        "start": "0:01:26",
        "end": "0:01:31",
        "text": "assigns weights to features, but also takes the input data and creates additional features automatically.",
        "label": "explanation"
      },
      {
        "start": "0:01:31",
        "end": "0:01:36",
        "text": "And that's extremely useful for data sets that contain things like images or natural language,",
        "label": "explanation"
      },
      {
        "start": "0:01:36",
        "end": "0:01:40",
        "text": "where manual feature engineering is virtually impossible. Every one of these algorithms learns",
        "label": "explanation"
      },
      {
        "start": "0:01:40",
        "end": "0:01:45",
        "text": "to get better by comparing its predictions to an error function. If it's a classification problem,",
        "label": "explanation"
      },
      {
        "start": "0:01:45",
        "end": "0:01:50",
        "text": "like is this animal a cat or a dog, the error function might be accuracy. If it's a regression",
        "label": "explanation"
      },
      {
        "start": "0:01:50",
        "end": "0:01:56",
        "text": "problem, like how much will a loaf of bread cost next year, then it might be mean absolute error.",
        "label": "tip"
      }
    ]
  },
  {
    "group_id": 3,
    "group_start_time": "0:01:56",
    "group_end_time": "0:02:19",
    "group_summary": "In a segment discussing machine learning (ML), an instructional video emphasizes that ML enables computers to perform tasks without explicit programming by using algorithms trained with large data sets for predictive accuracy enhancement. The transcript highlights Python as the preferred language among data scientists, though R and Julia are also widely used due to their suitability in handling statistical computations inherent in machine learning applications.\n\nThe video further explains that ML culminates in a model—a file designed for inputting specific shapes of training data which then generates predictions aimed at reducing error margins as per the optimization goals set during its creation phase. These models can be integrated into real-world devices or deployed online, showcasing their practical utility beyond theoretical constructs.\n\nKey concepts presented include:\n1. The role and importance of machine learning in automating complex tasks without direct coding instructions for computers to follow;\n2. Python's prevalence among data scientists alongside R and Julia as alternative programming languages that support ML frameworks, each with its own set of tools tailored towards statistical analysis or performance optimization within the field;\n3. The conceptualization of an 'ML model,' which is essentially a predictive tool built to process input in accordance with training parameters for output generation—essentially bridging raw data and actionable insights through iterative learning processes that refine prediction accuracy over time;\n4. Practical application potential, wherein the models can be operationalized on actual devices or within live environments via deployment strategies discussed implicitly by mentioning real-world integration possibilities for ML algorithms post training phase completion. \n\nThe segment underscs how machine learning is not just an academic exercise but a robust toolkit that data scientists employ to create intelligent systems capable of making informed predictions, thereby driving innovation and efficiency in various industries where automated decision-making can be beneficially applied.",
    "group_segments": [
      {
        "start": "0:01:56",
        "end": "0:02:01",
        "text": "Python is the language of choice among data scientists, but R and Julia are also popular options,",
        "label": "introduction"
      },
      {
        "start": "0:02:01",
        "end": "0:02:05",
        "text": "and there are many supporting frameworks out there to make the process approachable.",
        "label": "explanation"
      },
      {
        "start": "0:02:05",
        "end": "0:02:10",
        "text": "The end result of the machine learning process is a model, which is just a file that takes some",
        "label": "explanation"
      },
      {
        "start": "0:02:10",
        "end": "0:02:15",
        "text": "input data in the same shape that it was trained on, then spits out a prediction that tries to minimize",
        "label": "explanation"
      },
      {
        "start": "0:02:15",
        "end": "0:02:19",
        "text": "the error that it was optimized for. It can then be embedded on an actual device or deploy to the",
        "label": "transition"
      }
    ]
  },
  {
    "group_id": 4,
    "group_start_time": "0:02:19",
    "group_end_time": "0:02:34",
    "group_summary": "In a concise introduction to machine learning within an instructional video context (approximately 10 seconds), viewers are prompted with enthusiasm about the potential of building real-world products using this technology, as conveyed by their invitation for engagement through liking and subscribing. The segment serves not only as a call to action but also sets an optimistic tone regarding machine learning's practical applications in industry settings.\n\nFollowing that brief promotional interlude (last roughly 6 seconds), the speaker transitions into offering additional educational content specifically tailored for those interested in deepening their understanding of machine learning concepts, as indicated by a direct invitation to subscribe and follow along with future videos on this channel. This segment underscores an interactive approach aimed at fostering continuous education within its audience base while encouraging community growth around the subject matter discussed.\n\nThe summary encapsulates both aspects of viewer engagement (promotion) as well as educational outreach, highlighting a dual focus on expanding viewership and knowledge dissemination in machine learning—a field where data-driven algorithms learn from vast datasets to enhance predictive accuracy over time. The speaker's closing remark (\"Thanks for watching,\" followed by \"I will see you in the next one\") further establishes an expectation of a continued, evolving educational journey with their channel dedicated to machine learning insights and advancements.\n\nIn essence, these segments convey not only information about what machine learning is—a method where computers learn tasks without explicit programming through data analysis but also how viewers can actively participate in this knowledge-sharing experience by engaging more with the content provided on their platform dedicated to teaching and discussing such technologies.",
    "group_segments": [
      {
        "start": "0:02:19",
        "end": "0:02:24",
        "text": "cloud to build a real world product. This has been machine learning in 100 seconds. Like and",
        "label": "introduction"
      },
      {
        "start": "0:02:28",
        "end": "0:02:34",
        "text": "more machine learning content on this channel. Thanks for watching, and I will see you in the next one.",
        "label": "transition"
      }
    ]
  }
]

from pathlib import Path, PosixPath
relevant_gifs = {0: PosixPath('output/work_20251209_025156/gifs/clip_0.gif'), 
                 2: PosixPath('output/work_20251209_025156/gifs/clip_2.gif'), 
                 3: PosixPath('output/work_20251209_025156/gifs/clip_3.gif'), 
                 4: PosixPath('output/work_20251209_025156/gifs/clip_4.gif')}

clips_dir = "output/work_20251209_025156/gifs"
output_dir = "output/work_20251209_025156"

create_final_draft_json(grouped_data, relevant_gifs, clips_dir, output_dir, logger=None)