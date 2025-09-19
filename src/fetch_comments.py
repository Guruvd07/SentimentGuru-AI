import os
import googleapiclient.discovery
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

def fetch_comments(video_id, max_comments=200, output_file=None):
    """
    YouTube se comments fetch karega aur CSV me save karega.
    video_id : str -> YouTube video ka ID
    max_comments : int -> kitne comments fetch karne hai
    output_file : str -> save karne ka path (optional)
    """
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

    comments = []
    next_page_token = None

    while len(comments) < max_comments:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            pageToken=next_page_token,
            textFormat="plainText"
        )
        response = request.execute()

        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "author": comment["authorDisplayName"],
                "text": comment["textDisplay"],
                "likes": comment["likeCount"]
            })

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    df = pd.DataFrame(comments)

    # Save only if path provided
    if output_file:
        df.to_csv(output_file, index=False)
        print(f"✅ Comments saved at {output_file}")

    return df

# Example run
if __name__ == "__main__":
    video_id = "bW-Z-iLHz4w"
    fetch_comments(video_id, max_comments=300, output_file=f"src/data/{video_id}_raw.csv")
