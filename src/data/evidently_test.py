import pandas as pd
import os
from evidently.test_suite import TestSuite
from evidently.tests import *
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
import json

def load_data(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    data_frames = []
    for file in files:
        df = pd.read_csv(os.path.join(directory, file))
        if 'Datetime' in df.columns:
            df['Datetime'] = pd.to_datetime(df['Datetime'])
        data_frames.append(df)
    return pd.concat(data_frames, ignore_index=True)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, '..', '..', 'data')
current_data = load_data(os.path.join(DATA_DIR, "processed"))
reference_data = load_data(os.path.join(DATA_DIR, "reference_data"))

report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=reference_data, current_data=current_data)
report.save_html('../../reports/report.html')

tests = TestSuite(tests=[
    TestNumberOfColumnsWithMissingValues(),
    TestNumberOfRowsWithMissingValues(),
    TestNumberOfConstantColumns(),
    TestNumberOfDuplicatedRows(),
    TestNumberOfDuplicatedColumns(),
    TestColumnsType(),
    TestNumberOfDriftedColumns(),
])

tests.run(reference_data=reference_data, current_data=current_data)

test_results = tests.json()
parsed_results = json.loads(test_results)

print(json.dumps(parsed_results, indent=4))