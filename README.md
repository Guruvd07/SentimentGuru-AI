🎥 SentimentGuru AI – YouTube Comment Sentiment Analysis
📌 Overview

SentimentGuru AI is a full-stack web app that analyzes YouTube comments and classifies them as Positive, Neutral, or Negative.
The app allows you to paste any YouTube video link, then:
Extracts comments using YouTube API.
Runs sentiment analysis using CardiffNLP RoBERTa Sentiment Model (cardiffnlp/twitter-roberta-base-sentiment).
Displays results on a beautiful website with video preview, sentiment distribution, ratings, and categorized comments.

🌟 Features

✅ Paste YouTube video link → Instant analysis

✅ Shows video preview with title

✅ Generates rating out of 10 based on sentiment score

✅ Categorizes comments: Positive / Neutral / Negative

✅ Displays total comments + count of each sentiment

✅ Interactive UI built with HTML + CSS + JavaScript

✅ Backend powered by Flask

✅ NLP using Transformers (Hugging Face)

✅ Free deployment on Hugging Face Spaces

🛠️ Tech Stack

Frontend: HTML, CSS, JavaScript
Backend: Flask (Python)
NLP Model: cardiffnlp/twitter-roberta-base-sentiment (Hugging Face Transformers)
Visualization: Matplotlib / Chart.js
Deployment: Hugging Face Spaces

⚙️ Model Details
We use the Hugging Face model:
🔗 cardiffnlp/twitter-roberta-base-sentiment

It predicts 3 classes:
0 → Negative
1 → Neutral
2 → Positive

Mapping in app:
labels = {0: "Negative", 1: "Neutral", 2: "Positive"}

📊 Workflow
User Input
Paste YouTube video link in the search box.
Example: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Backend Processing (Flask)
Extract video ID.
Fetch comments from YouTube API.
Pass comments through RoBERTa sentiment model.
Calculate sentiment distribution + rating out of 10.
Frontend Display (Website)
Show video preview (thumbnail + title).
Show rating (e.g., 8.3 / 10).
Show sentiment distribution chart.
List comments in Positive, Neutral, Negative sections.
Show total count summary.

📊 Example Output

Input:
👉 YouTube video link → https://www.youtube.com/watch?v=abc123

Output on Website:
🎬 Video Player + Title

⭐ Rating: 8.2 / 10

📊 Distribution:

Positive: 420 comments
Neutral: 75 comments
Negative: 105 comments
Total: 600 comments

💬 Comment Samples:

Positive → "This video is so helpful!"
Negative → "Worst explanation ever."
Neutral → "Okay, nothing special."


👨‍💻 Author
Developed by Guru Dahiphale 🚀
Feel free to ⭐ the repo if you like it!
