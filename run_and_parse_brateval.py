""" Run brateval.jar and parse its output into a dataframe.
Inputs:
    Ground truth dataset in brat format
    Predictions in brat format
    path to brateval.jar executable

Examples:

# event_extraction and entity extraction run and parse BRATEval into a dataframe .
ee_results = event_extraction(
    ee_gold_folder=test_dataset_path.resolve(),
    ee_pred_folder=test_output_path.resolve(),
    brat_eval_path='evaluation/BRATEval.jar')

"""

import subprocess
from pathlib import Path

import pandas as pd


def entity_extraction(ner_gold_folder=None,
                      ner_pred_folder=None,
                      brat_eval_path=None):
    print('Entity Extraction')
    if not Path(ner_gold_folder).exists():
        raise NotADirectoryError('Ground truth directory not found')
    if not Path(ner_pred_folder):
        raise NotADirectoryError('Predictions directory not found')

    ner = 'au.com.nicta.csp.brateval.CompareEntities'

    # print('EXACT match')
    brat_exact = subprocess.run(['java', '-cp', brat_eval_path, ner, ner_pred_folder, ner_gold_folder, '-s', 'exact'],
                                capture_output=True)
    exact = dataframe_from_brateval_ner(brat_exact, header=True)

    # print('RELAX match')
    brat_relax = subprocess.run(['java', '-cp', brat_eval_path, ner, ner_pred_folder, ner_gold_folder, '-s', 'overlap'],
                                capture_output=True)
    relax = dataframe_from_brateval_ner(brat_relax, header=True)
    return {'exact': exact, 'relax': relax}


def dataframe_from_brateval_ner(brateval_results, header=False):
    brateval_results = brateval_results.stdout.decode().strip().splitlines()
    brateval_results = brateval_results[brateval_results.index('Summary:') + 1:]
    df = pd.DataFrame([row.split('|') for row in brateval_results])
    if header:
        df.columns = df.iloc[0]
        df = df.iloc[1:].reset_index(drop=True)
    return df


def event_extraction(ee_gold_folder=None,
                     ee_pred_folder=None,
                     brat_eval_path=None,
                     ):
    print('Event Extraction')
    if not Path(ee_pred_folder).exists():
        raise NotADirectoryError('Ground truth directory not found')
    if not Path(ee_gold_folder):
        raise NotADirectoryError('Predictions directory not found')
    rel = 'au.com.nicta.csp.brateval.CompareRelations'

    # print('EXACT match')
    brat_exact = subprocess.run(['java', '-cp', brat_eval_path, rel, ee_pred_folder, ee_gold_folder, '-s', 'exact_df'],
                                capture_output=True)
    brat_exact = brat_exact.stdout.decode().strip().splitlines()
    brat_exact = brat_exact[brat_exact.index('Summary:') + 1:]
    exact_df = brat_to_dataframe_ee(brat_exact)

    # print('RELAX match')
    brat_relax = subprocess.run(['java', '-cp', brat_eval_path, rel, ee_pred_folder, ee_gold_folder, '-s', 'overlap'],
                                capture_output=True)
    brat_relax = brat_relax.stdout.decode().strip().splitlines()
    brat_relax = brat_relax[brat_relax.index('Summary:') + 1:]
    relax_df = brat_to_dataframe_ee(brat_relax)
    return {'exact': exact_df, 'relax': relax_df}


def brat_to_dataframe_ee(brateval_results):
    records = []
    for line in brateval_results:
        record = {}
        line = line.split('|')
        if line[0] != 'all':
            record['label'] = line[0]
            record['arg1'] = line[1]
            record['arg2'] = line[2]
            record.update((tuple(value.split(':')) for value in line[3:]))
        else:
            record['label'] = line[0]
            record.update({value.split(':')[0]: value.split(':')[1] for value in line[1:]})

        records.append(record)
    df = pd.DataFrame.from_records(records)
    return df
