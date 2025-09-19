import pandas as pd
import re
import emoji
from nltk.tokenize import word_tokenize

# ✅ English stopwords (hardcoded, no need for NLTK download)
ENGLISH_STOPWORDS = {
    "i","me","my","myself","we","our","ours","ourselves","you","your","yours",
    "yourself","yourselves","he","him","his","himself","she","her","hers",
    "herself","it","its","itself","they","them","their","theirs","themselves",
    "what","which","who","whom","this","that","these","those","am","is","are",
    "was","were","be","been","being","have","has","had","having","do","does",
    "did","doing","a","an","the","and","but","if","or","because","as","until",
    "while","of","at","by","for","with","about","against","between","into",
    "through","during","before","after","above","below","to","from","up","down",
    "in","out","on","off","over","under","again","further","then","once","here",
    "there","when","where","why","how","all","any","both","each","few","more",
    "most","other","some","such","no","nor","not","only","own","same","so",
    "than","too","very","s","t","can","will","just","don","should","now"
}

# ✅ Hindi stopwords (same as before)
HINDI_STOPWORDS = {
    "और", "का", "है", "को", "से", "पर", "में", "नहीं", "ही", "भी", "तो",
    "था", "थे", "थी", "कर", "करना", "किया", "लिए", "अपना", "उनका",
    "उसके", "वह", "यह", "ये", "उन", "कुछ", "किसी", "हर", "सभी"
}

STOP_WORDS = ENGLISH_STOPWORDS | HINDI_STOPWORDS

# ✅ Hinglish dictionary
HINGLISH_DICT = {
    "acha": "good",
    "bahut": "very",
    "bht": "very",
    "bohot": "very",
    "mast": "awesome",
    "shukriya": "thanks",
    "dhanyavad": "thanks",
    "pyar": "love",
    "pyaar": "love",
    "dil": "heart",
    "dukh": "sad",
    "khushi": "happy",
    "acha laga": "liked",
    "samajh": "understand",
    "sikhaya": "taught",
    "seekha": "learned",
    "maza": "fun"
}

def normalize_hinglish(text):
    for word, eng in HINGLISH_DICT.items():
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

    # Keep only English + Hindi characters
    text = re.sub(r'[^a-zA-Z\u0900-\u097F\s]', '', text)

    # Tokenize
    tokens = word_tokenize(text)

    # Remove stopwords
    tokens = [word for word in tokens if word not in STOP_WORDS]

    return " ".join(tokens)

def preprocess(input_file="data/raw_comments.csv", output_file="data/clean_comments.csv"):
    df = pd.read_csv(input_file)
    
    if "text" not in df.columns:
        print("❌ 'text' column not found!")
        return
    
    df["clean_text"] = df["text"].astype(str).apply(clean_text)
    df.to_csv(output_file, index=False)
    print(f"✅ Preprocessing done! Clean data saved at {output_file}")

if __name__ == "__main__":
    preprocess()
