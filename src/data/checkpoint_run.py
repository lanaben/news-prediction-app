import subprocess
from datetime import datetime

#TODO: run in worflow, paths for workflow

current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

result = subprocess.run(
    "great_expectations checkpoint run test_checkpoint",
    shell=True,
    capture_output=True,
    text=True,
    encoding="utf-8"
)

output_info = f"\n --- \n Date and Time: {current_datetime}\n\n{result.stdout}"

with open('../../reports/validation_report.txt', 'a', encoding="utf-8") as f:
    f.write(output_info)
