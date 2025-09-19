from flask import Flask, render_template, request
import pandas as pd
import re, os
from src.fetch_comments import fetch_comments
from src.preprocess import preprocess
from src.sentiment import analyze_sentiment
from googleapiclient.discovery import build
import os

app = Flask(__name__)

# YouTube API setup
API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=API_KEY)

def extract_video_id(url_or_id):
    """Extract video ID from YouTube URL or return as is"""
    match = re.search(r"v=([a-zA-Z0-9_-]{11})", url_or_id)
    return match.group(1) if match else url_or_id

def get_video_info(video_id):
    """Fetch video title + thumbnail"""
    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    response = request.execute()
    if response["items"]:
        snippet = response["items"][0]["snippet"]
        return {
            "title": snippet["title"],
            "thumbnail": snippet["thumbnails"]["high"]["url"]
        }
    return {"title": "Unknown", "thumbnail": ""}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form["video_url"]
        video_id = extract_video_id(video_url)

        # Step 1: Fetch comments
        raw_path = f"data/raw/{video_id}_raw.csv"
        df = fetch_comments(video_id, max_comments=300)
        os.makedirs("data/raw", exist_ok=True)
        df.to_csv(raw_path, index=False)

        # Step 2: Preprocess
        clean_path = f"data/clean/{video_id}_clean.csv"
        os.makedirs("data/clean", exist_ok=True)
        preprocess(raw_path, clean_path)

        # Step 3: Sentiment
        final_path = f"data/final/{video_id}_labeled.csv"
        os.makedirs("data/final", exist_ok=True)
        analyze_sentiment(clean_path, final_path)

        # Step 4: Load results
        df_final = pd.read_csv(final_path)
        pos = (df_final["sentiment"] == "Positive").sum()
        neg = (df_final["sentiment"] == "Negative").sum()
        neu = (df_final["sentiment"] == "Neutral").sum()
        total = len(df_final)

        # Rating logic
        rating = round(((pos * 10) + (neu * 5)) / total, 1)

        # Get video info
        video_info = get_video_info(video_id)

        return render_template("result.html",
                               video_id=video_id,
                               video_info=video_info,
                               total=total, pos=pos, neg=neg, neu=neu,
                               rating=rating,
                               comments=df_final.head(10).to_dict(orient="records"))
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
