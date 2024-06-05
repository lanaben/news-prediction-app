import os
import subprocess
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, '..', '..')
output_file = os.path.join(DATA_DIR, "reports", "validation_report.txt")

current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

result = subprocess.run(
    "great_expectations checkpoint run test_checkpoint",
    shell=True,
    capture_output=True,
    text=True,
    encoding="utf-8"
)

output_info = f"\n --- \n Date and Time: {current_datetime}\n\n{result.stdout}"

with open(output_file, 'a', encoding="utf-8") as f:
    f.write(output_info)
