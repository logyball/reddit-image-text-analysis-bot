from google.cloud import vision, language
from google.cloud.language import enums
from google.cloud.language import types
import six
import pprint

def addMag(mag):
    if (mag <= 0.1):
        return "weakly"
    elif (mag <= 0.35):
        return "moderately"
    elif (mag <= 0.5):
        return "aggressively"
    else:
        return "overwhelmingly"

def mapTextToEmotion(sentiment):
    tone = []
    score = sentiment.score
    mag = sentiment.magnitude
    tone.append(addMag(mag))
    # very negative
    if score < -0.6:
        tone.append('miserable')
    # weakly negative
    elif score < -0.1:
        tone.append('negative')
    # nuetral
    elif score < 0.1:
        tone.append('nuetral')
    # weakly postiive
    elif score < 0.6:
        tone.append('positive')
    # very positive
    else:
        tone.append('ecstatic')
    return tone

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
    return labelDesc