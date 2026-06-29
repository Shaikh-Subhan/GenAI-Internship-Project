from langdetect import detect
from deep_translator import GoogleTranslator


def detect_language(text):
    try:
        # Short texts are unreliable for langdetect
        if len(text.strip()) < 3:
            return "en"

        lang = detect(text)

        supported = ["en", "hi", "gu", "ur"]
        if lang not in supported:
            return "en"

        return lang

    except:
        return "en"


def translate_to_english(text, source_lang):
    if source_lang == "en":
        return text

    try:
        translated = GoogleTranslator(
            source=source_lang,
            target="en"
        ).translate(text)
        return translated
    except:
        return text


def translate_from_english(text, target_lang):
    if target_lang == "en":
        return text

    try:
        translated = GoogleTranslator(
            source="en",
            target=target_lang
        ).translate(text)
        return translated
    except:
        return text