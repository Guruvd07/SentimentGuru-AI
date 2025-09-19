import pandas as pd
import re
import emoji
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# English stopwords
english_stopwords = set(stopwords.words('english'))

# Hindi stopwords
hindi_stopwords = {
    "और", "का", "है", "को", "से", "पर", "में", "नहीं", "ही", "भी", "तो",
    "था", "थे", "थी", "कर", "करना", "किया", "लिए", "अपना", "उनका",
    "उसके", "वह", "यह", "ये", "उन", "कुछ", "किसी", "हर", "सभी"
}
stop_words = english_stopwords | hindi_stopwords

# Hinglish dictionary
hinglish_dict = {
    "acha": "good", "bahut": "very", "bht": "very", "bohot": "very",
    "mast": "awesome", "shukriya": "thanks", "dhanyavad": "thanks",
    "pyar": "love", "pyaar": "love", "dil": "heart", "dukh": "sad",
    "khushi": "happy", "acha laga": "liked", "samajh": "understand",
    "sikhaya": "taught", "seekha": "learned", "maza": "fun"
}

def normalize_hinglish(text):
    for word, eng in hinglish_dict.items():
        text = re.sub(rf"\b{word}\b", eng, text)
    return text

def clean_text(text):
    if not isinstance(text, str):
        return ""
    
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)  # remove URLs

    # Convert emojis to words
    text = emoji.demojize(text, delimiters=(" ", " "))
    text = text.replace(":", " ")

    # Normalize Hinglish
    text = normalize_hinglish(text)

    # Keep only English + Hindi
    text = re.sub(r'[^a-zA-Z\u0900-\u097F\s]', '', text)

    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]

    return " ".join(tokens)

def preprocess(input_file, output_file):
    """
    Raw comments ko clean karega aur CSV save karega.
    """
    df = pd.read_csv(input_file)

    if "text" not in df.columns:
        raise ValueError("❌ 'text' column not found!")

    df["clean_text"] = df["text"].astype(str).apply(clean_text)
    df.to_csv(output_file, index=False)
    print(f"✅ Preprocessing done! Clean data saved at {output_file}")
    return df

# Example run
if __name__ == "__main__":
    video_id = "bW-Z-iLHz4w"
    preprocess(f"src/data/{video_id}_raw.csv", f"src/data/{video_id}_clean.csv")
