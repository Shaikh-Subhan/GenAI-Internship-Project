from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis")


def detect_sentiment(text):
    # Safety: limit very long inputs
    text = text[:1000]

    try:
        result = sentiment_pipeline(text, truncation=True)[0]
    except TypeError:
        # Some transformer versions don't support truncation kwarg
        result = sentiment_pipeline(text[:500])[0]

    label = result["label"]
    score = result["score"]

    if score < 0.75:
        label = "NEUTRAL"

    return label, score