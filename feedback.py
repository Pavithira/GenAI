import datetime

def save_feedback(text):
    with open("feedback.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {text}\n\n")
