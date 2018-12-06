from google.cloud import vision, language
from google.cloud.language import enums
from google.cloud.language import types
from random import choice
import six
import pprint

# magnitude words
weakList = ['weakly', 'flimsily', 'lamely', 'unconvincingly']
moderateList = ['moderately', 'sort of', 'a bit', 'unconvincingly']
aggroList = ['aggressively', 'forcefully', 'strongly', 'stoutly']
overList = ['overwhelmingly', 'inconcievably', 'astronomically', 'intensely']

# positive/negative words
vBadList = ['miserable', 'agonizing', 'depressed', 'morose']
badList = ['bad', 'negative', 'gloomy', 'pessimistic']
neutralList = ['neutral', 'centrist', 'indifferent', 'apathetic']
posList = ['positive', 'constructive', 'good', 'favorable']
joyList = ['joyful', 'sublime', 'elation', 'ecstatic']

def addMag(mag):
    if (mag <= 0.1):
        return choice(weakList)
    elif (mag <= 0.35):
        return choice(moderateList)
    elif (mag <= 0.5):
        return choice(aggroList)
    else:
        return choice(overList)

def mapTextToEmotion(sentiment):
    tone = []
    score = sentiment.score
    mag = sentiment.magnitude
    tone.append(addMag(mag))
    # very negative
    if score < -0.6:
        tone.append(choice(vBadList))
    # weakly negative
    elif score < -0.1:
        tone.append(choice(badList))
    # nuetral
    elif score < 0.1:
        tone.append(choice(neutralList))
    # weakly postiive
    elif score < 0.6:
        tone.append(choice(posList))
    # very positive
    else:
        tone.append(choice(joyList))
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