from modules.sentiment import detect_sentiment

texts = [
    "I love your service",
    "Where is my order?",
    "This is terrible service"
]

for text in texts:
    sentiment, score = detect_sentiment(text)
    print(text)
    print(sentiment, score)
    print()