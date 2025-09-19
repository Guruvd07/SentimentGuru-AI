import pandas as pd
from transformers import pipeline

# Hugging Face model ek hi baar load karna fast hota hai
classifier = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

# Labels mapping
labels = {0: "Negative", 1: "Neutral", 2: "Positive"}

def analyze_sentiment(input_file, output_file):
    """
    Sentiment analysis karega clean comments pe.
    input_file : str -> path of cleaned comments CSV
    output_file : str -> path to save labeled comments CSV
    """
    df = pd.read_csv(input_file)

    # Ensure text column
    if "clean_text" not in df.columns:
        raise ValueError("❌ 'clean_text' column missing in input CSV")

    df["clean_text"] = df["clean_text"].astype(str).fillna("")

    all_results = []
    batch_size = 32

    for i in range(0, len(df), batch_size):
        batch = df["clean_text"].iloc[i:i+batch_size].tolist()
        results = classifier(batch, truncation=True, padding=True, max_length=512)

        for r in results:
            label_num = int(r["label"].split("_")[-1])  # e.g. "LABEL_2"
            all_results.append(labels[label_num])

    df["sentiment"] = all_results
    df.to_csv(output_file, index=False)

    print(f"✅ Sentiment labeling done and saved to {output_file}")
    return df
