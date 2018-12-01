from google.cloud import vision, language
from google.cloud.language import enums
from google.cloud.language import types
import six

def mapTextToEmotion(sentiment):
    return ["happy"] #TODO

def googleTextAnalysis(text):
    client = language.LanguageServiceClient()
    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')
    document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT, language='en')
    sentiment = client.analyze_sentiment(document).document_sentiment
    return mapTextToEmotion(sentiment)

def googleImageAnalysis(url):
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = url
    response = client.label_detection(image=image)
    labels = response.label_annotations
    labelDesc = []
    for label in labels:
        labelDesc.append(label.description)
        print(label.description)
    return labelDesc