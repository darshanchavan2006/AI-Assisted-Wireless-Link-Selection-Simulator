import subprocess
import sys

commands = [
    [sys.executable, "src/generate_dataset.py"],
    [sys.executable, "src/train_model.py"],
    [sys.executable, "src/simulate_network.py"],
]

for cmd in commands:
    print("\n>>>", " ".join(cmd))
    subprocess.run(cmd, check=True)

print("\nComplete project pipeline finished.")
