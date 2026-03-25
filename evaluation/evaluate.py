import json
from main import final_guardrail


def run_evaluation(threshold):
    tp = fp = tn = fn = 0

    with open("data/redteam.json", "r") as f:
        data = json.load(f)

    for item in data:
        prompt = item["prompt"]
        true_label = item["label"]

        result = final_guardrail(prompt,threshold)
        pred = result["Final_verdict"]

        print(result)

        if true_label == "UNSAFE":
            if pred == "UNSAFE":
                tp += 1
            else:
                fn += 1

        elif true_label == "SAFE":
            if pred == "SAFE":
                tn += 1
            else:
                fp += 1

    accuracy = (tp + tn) / (tp + tn + fp + fn)

    print("\nConfusion Matrix:")
    print(f"TP: {tp}")
    print(f"TN: {tn}")
    print(f"FP: {fp}")
    print(f"FN: {fn}")
    print(f"Accuracy: {round(accuracy, 2)}")

    return tp, tn, fp, fn, accuracy


if __name__ == "__main__":
    run_evaluation()