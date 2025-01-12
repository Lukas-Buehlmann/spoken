from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.nn.functional import softmax
import torch
import gc
import threading


def get_emotion(text):

    # List of Emotions and their corresponding emojis
    emotion_emoji_map = {
        "anger": "\U0001F620",
        "disgust": "\U0001F922",
        "fear": "\U0001F628",
        "joy": "\U0001F600",
        "neutral": "\U0001F610",
        "sadness": "\U0001F622",
        "surprise": "\U0001F632"
    }

    # Load the sentiment analysis model (Roberta for overall positivity/negativity)
    sentiment_model_name = "cardiffnlp/twitter-roberta-base-sentiment"  # Remote or local path
    sentiment_tokenizer = AutoTokenizer.from_pretrained(sentiment_model_name)
    sentiment_model = AutoModelForSequenceClassification.from_pretrained(sentiment_model_name)

    # Load the emotion detection model (DistilRoberta for emotions)
    emotion_model_name = "j-hartmann/emotion-english-distilroberta-base"  # Remote or local path
    emotion_tokenizer = AutoTokenizer.from_pretrained(emotion_model_name)
    emotion_model = AutoModelForSequenceClassification.from_pretrained(emotion_model_name)

    # Define emotion labels (specific to the emotion model)
    emotion_labels = ["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"]

    # Split the text into sentences
    sentences = [sentence.strip() for sentence in text.split('.') if sentence.strip()]

    results = []

    for idx, sentence in enumerate(sentences):

        # Sentiment Analysis
        sentiment_inputs = sentiment_tokenizer(sentence, return_tensors="pt")
        with torch.no_grad():
            sentiment_outputs = sentiment_model(**sentiment_inputs)
        sentiment_logits = sentiment_outputs.logits
        sentiment_probs = softmax(sentiment_logits, dim=1)
        sentiment_labels = ["negative", "neutral", "positive"]
        sentiment_results = {sentiment_labels[i]: sentiment_probs[0][i].item() for i in range(len(sentiment_labels))}
        most_confident_sentiment = max(sentiment_results, key=sentiment_results.get)

        # Emotion Detection
        emotion_inputs = emotion_tokenizer(sentence, return_tensors="pt")
        with torch.no_grad():
            emotion_outputs = emotion_model(**emotion_inputs)
        emotion_logits = emotion_outputs.logits
        emotion_probs = softmax(emotion_logits, dim=1)
        emotion_results = {emotion_labels[i]: emotion_probs[0][i].item() for i in range(len(emotion_labels))}

        # Determine the most confident emotion
        most_confident_emotion = max(emotion_results, key=emotion_results.get)
        most_confident_emoji = emotion_emoji_map.get(most_confident_emotion, "")

        # Append result
        results.append((most_confident_sentiment, most_confident_emoji))

    return results
