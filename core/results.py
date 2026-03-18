import csv
import os
import time

RESULTS_DIR = os.getenv("RESULTS_DIR", "logs")
FILE = os.path.join(RESULTS_DIR, "results.csv")


def save_results(results):

    os.makedirs(RESULTS_DIR, exist_ok=True)

    temp_file = f"{FILE}.tmp"

    with open(temp_file, "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "strategy",
            "reward",
            "cost",
            "latency",
            "energy",
            "sla",
            "carbon",
            "servers",
            "resources",
            "memory",
            "max_servers",
            "cloud_resource_capacity",
            "cloud_memory_capacity",
            "users"
        ])

        for r in results:

            writer.writerow([
                r["strategy"],
                r["reward"],
                r["cost"],
                r["latency"],
                r["energy"],
                r["sla"],
                r["carbon"],
                r["servers"],
                r["resources"],
                r["memory"],
                r["max_servers"],
                r["cloud_resource_capacity"],
                r["cloud_memory_capacity"],
                r["users"],
            ])

    for _ in range(10):
        try:
            os.replace(temp_file, FILE)
            return
        except PermissionError:
            time.sleep(0.05)

    # Last retry without swallowing the error.
    os.replace(temp_file, FILE)