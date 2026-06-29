from modules.multilingual import *

text = "તમારી refund policy શું છે?"

lang = detect_language(text)
print("Detected:", lang)

translated = translate_to_english(text, lang)
print("English:", translated)