""" CLI for the Python Brat wrapper 

About:
Designed to be a friendly easy to use wrapper for Brat,
that allows the user to forget the specific commandline details,
checks for common mistakes, and save the command output for future referance.

!!! Before usage make sure brateval and other thing is correct for your system

Inputs:
    Path to ground truth dataset
    Path to predictions dataset

Examples:

python runbrat.py ./groundTruth ./Predictions

python runbrat.py ./groundTruth ./Predictions ./myOutput.csv

"""

from pathlib import Path
import sys
import filecmp

import pandas as pd

from run_and_parse_brateval import *

# !!! Will be specific to your system
brat_eval_path = Path(f"{Path.home().resolve()}/packages/brateval/brateval.jar")

assert brat_eval_path.exists(), f"brateval not found at {str(brat_eval_path)}"

def main(groundTruth, predictions):
    groundTruth = Path(groundTruth)
    predictions = Path(predictions)
    assert groundTruth.exists(), f"{str(groundTruth)} Not Found!"
    assert predictions.exists(), f"{str(predictions)} Not Found!"

    filediff = filecmp.dircmp(groundTruth, predictions)
    if filediff.left_only:
        print(f"Extra files in {groundTruth}:\n{filediff.left_only}")
    if filediff.right_only:
        print(f"Extra files in {predictions}:\n{filediff.right_only}")
    if filediff.left_only or filediff.right_only:
        print("Cannot run program until files are even...")
        exit(0)

    print(f"Comparing {len([x for x in filediff.common if x[-4:] == '.ann'])} files...")

    ee_results = entity_extraction(
        ner_gold_folder=str(groundTruth),
        ner_pred_folder=str(predictions),
        brat_eval_path=str(brat_eval_path))

    return(ee_results)

if __name__ == "__main__":
    
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Expected formats:")
        print("python runbrat.py ./groundTruth ./Predictions")
        print("python runbrat.py ./groundTruth ./Predictions ./myOutput.csv")

    groundTruth = sys.argv[1]
    predictions = sys.argv[2]

    ee_results = main(groundTruth, predictions)

    print(ee_results)

    if len(sys.argv) == 4:
        savefolder = Path(sys.argv[3])
        ee_results['exact'].to_csv(savefolder)
