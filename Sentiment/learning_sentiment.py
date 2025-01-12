
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.nn.functional import softmax
import torch
import gc
import threading

# Load the sentiment analysis model (Roberta)
sentiment_model_name = "cardiffnlp/twitter-roberta-base-sentiment"  # Remote or local path
sentiment_tokenizer = AutoTokenizer.from_pretrained(sentiment_model_name)
sentiment_model = AutoModelForSequenceClassification.from_pretrained(sentiment_model_name)

# Load the emotion detection model (DistilRoberta for emotions)
emotion_model_name = "j-hartmann/emotion-english-distilroberta-base"  # Remote or local path
emotion_tokenizer = AutoTokenizer.from_pretrained(emotion_model_name)
emotion_model = AutoModelForSequenceClassification.from_pretrained(emotion_model_name)

# Define emotion labels (specific to the emotion model)
emotion_labels = ["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"]

# Input text
text = "I am so thrilled and excited about this opportunity, but also a bit nervous!"

# Sentiment Analysis
sentiment_inputs = sentiment_tokenizer(text, return_tensors="pt")
with torch.no_grad():
    sentiment_outputs = sentiment_model(**sentiment_inputs)
sentiment_logits = sentiment_outputs.logits
sentiment_probs = softmax(sentiment_logits, dim=1)
sentiment_labels = ["negative", "neutral", "positive"]
sentiment_results = {sentiment_labels[i]: sentiment_probs[0][i].item() for i in range(len(sentiment_labels))}

# Emotion Detection
emotion_inputs = emotion_tokenizer(text, return_tensors="pt")
with torch.no_grad():
    emotion_outputs = emotion_model(**emotion_inputs)
emotion_logits = emotion_outputs.logits
emotion_probs = softmax(emotion_logits, dim=1)
emotion_results = {emotion_labels[i]: emotion_probs[0][i].item() for i in range(len(emotion_labels))}

# Combine Results
print(f"Input Text: {text}\n")

print("Sentiment Analysis:")
for sentiment, prob in sentiment_results.items():
    print(f"  {sentiment.capitalize()}: {prob:.4f}")

print("\nEmotion Detection:")
for emotion, prob in emotion_results.items():
    print(f"  {emotion.capitalize()}: {prob:.4f}")

#for thread in threading.enumerate():
    #print(f"Thread Name: {thread.name}, Is Daemon: {thread.daemon}, Is Alive: {thread.is_alive()}")
'''
for thread in threading.enumerate():
    if not thread.daemon and thread is not threading.main_thread():
        print(f"Stopping thread: {thread.name}")
'''
for thread in threading.enumerate():
    if not thread.daemon and thread is not threading.main_thread():
        #print(f"Waiting for thread to finish: {thread.name}")
        thread.join()

del sentiment_tokenizer
del sentiment_model
del emotion_tokenizer
del emotion_model
gc.collect()
