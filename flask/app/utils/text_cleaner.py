import re

def clean_text(text):
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"[^a-zA-Z0-9.,!?;'\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_head_tail(text, head=256, tail=256):
    tokens = text.split()
    if len(tokens) <= head + tail:
        return text
    return " ".join(tokens[:head] + tokens[-tail:])

def prepare_text_for_emotion(text):
    text = clean_text(text)
    return extract_head_tail(text)


