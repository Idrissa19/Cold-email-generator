import re


def clean_text(text):
    text = re.sub(r'<[^>]*?>', '', text)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'[^\w\s.,;:!?\'’()/+#-]', ' ', text)
    return ' '.join(text.split())
