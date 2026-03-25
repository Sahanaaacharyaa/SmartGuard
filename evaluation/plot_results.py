from evaluation.evaluate import run_evaluation
import matplotlib.pyplot as plt

tp, tn, fp, fn, accuracy = run_evaluation()

labels = ['TP', 'TN', 'FP', 'FN']
values = [tp, tn, fp, fn]

plt.figure()
plt.bar(labels, values)

plt.title(f"Confusion Matrix (Accuracy: {round(accuracy,2)})")
plt.xlabel("Categories")
plt.ylabel("Count")

plt.show()