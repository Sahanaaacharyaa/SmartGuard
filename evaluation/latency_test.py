import json
import time
from main import final_guardrail

INPUT_FILE = "data/redteam.json"

def measure_latency(threshold=0.7):
    
    with open(INPUT_FILE, "r") as f:
        data = json.load(f)

    times = []

    for item in data:
        prompt = item["prompt"]

        start = time.time()
        final_guardrail(prompt, threshold)
        end = time.time()

        times.append(end - start)

    times.sort()

    p95 = times[int(0.95 * len(times))]
    avg = sum(times) / len(times)

    print(f"Average Latency: {round(avg, 4)} sec")
    print(f"P95 Latency: {round(p95, 4)} sec")


if __name__ == "__main__":
    measure_latency()