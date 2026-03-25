from transformers import pipeline

classifier = pipeline("text-classification")
print(classifier("This is amazing"))