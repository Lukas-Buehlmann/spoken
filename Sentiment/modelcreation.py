from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Load sentiment model

model_name = "cardiffnlp/twitter-roberta-base-sentiment"

tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Save the model and tokenizer to a local directory

model.save_pretrained("./my_model")

tokenizer.save_pretrained("./my_model")


# Load emotion model

model_name = "j-hartmann/emotion-english-distilroberta-base"

tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Save the model and tokenizer to a local directory

model.save_pretrained("./emotion_model")

tokenizer.save_pretrained("./emotion_model")
