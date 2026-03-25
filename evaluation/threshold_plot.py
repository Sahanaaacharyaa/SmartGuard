from evaluation.evaluate import run_evaluation
import matplotlib.pyplot as plt

thresholds = [0.5, 0.6, 0.7, 0.8, 0.9]

accuracies = []

for t in thresholds:
    print(f"\nRunning for threshold {t}")
    tp, tn, fp, fn, acc = run_evaluation(t)
    accuracies.append(acc)

plt.figure()
plt.plot(thresholds, accuracies, marker='o')

plt.xlabel("Threshold")
plt.ylabel("Accuracy")
plt.title("Accuracy vs Threshold")

plt.show()