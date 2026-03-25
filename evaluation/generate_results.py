import json
import csv
from main import final_guardrail

INPUT_FILE = "data/redteam.json"
OUTPUT_FILE = "evaluation/results.csv"


def generate_results(threshold=0.7):
    
    with open(INPUT_FILE, "r") as f:
        data = json.load(f)

    with open(OUTPUT_FILE, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # header
        writer.writerow(["prompt", "actual", "predicted", "confidence", "category"])

        for item in data:
            prompt = item["prompt"]
            actual = item["label"]

            result = final_guardrail(prompt, threshold)

            predicted = result["Final_verdict"]
            confidence = result["AI_confidence"]
            category = result["category"]

            writer.writerow([prompt, actual, predicted, confidence, category])

    print("✅ results.csv generated successfully!")


if __name__ == "__main__":
    generate_results()