"""
Official evaluation script for Qur'an QA 2022 Shared Task on QRCD v1.1 dataset
"""

from __future__ import print_function
from farasa.segmenter import FarasaSegmenter
from collections import Counter
import string
import argparse
import json
import sys
import re
import quranqa22_submission_checker

def normalize_text(s):
    """remove punctuation, some stopwords and extra whitespace."""
    def remove_stopWords(text):
        terms = []
        stopWords = {'من', 'الى', 'إلى', 'عن', 'على', 'في', 'حتى'}
        for term in text.split():
            if term not in stopWords:
                terms.append(term)
        return " ".join(terms)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        # Arabic punctuation
        exclude.add('،')
        exclude.add('؛')
        exclude.add('؟')
        return ''.join(ch for ch in text if ch not in exclude)

    return white_space_fix(remove_stopWords(remove_punc(s)))

def remove_prefixes(text):
    text_tokens = farasa_segmenter.segment(text).split()
    tokens = []
    for token in text_tokens:
        token = re.sub(r'^و[+]', '', token)  # only begining of words
        token = re.sub(r'^ف[+]', '', token)
        token = re.sub(r'^ب[+]', '', token)
        token = re.sub(r'^ك[+]', '', token)
        token = re.sub(r'^ل[+]', '', token)
        token = re.sub(r'^لل[+]', '', token)
        token = re.sub(r'^ال[+]', '', token)

        # defragment by removing pluses
        token = re.sub(r'[+]', '', token)
        tokens.append(token)
    return " ".join(tokens)

def find_all_occurences(passage, answer):
    start_char_list = []
    if len(answer) == 0:
        return start_char_list
    passage = normalize_text(passage)
    answer = normalize_text(answer)
    index = 0
    while True:
        index = passage.find(answer, index) # get the index of first matching substring
        if index == -1:  # if no match, return
            return start_char_list 
        start_char_list.append(index) 
        index += 1 # find next matching substring

def is_answer_from_passage(prediction_start_char_occurences):
    # Ensure that prediction is a span from the passage
    if len(prediction_start_char_occurences) > 0:
        return True
    else:
        return False

def exact_match_score(prediction, prediction_start_char_occurences, ground_truth,):
    if len(prediction) == 0: 
        # there is no prediction
        return 0
    
    if is_answer_from_passage(prediction_start_char_occurences) is False:
        return 0 # return 0 if the predicted answer is not a span from the passage

    return (normalize_text(remove_prefixes(prediction)) == normalize_text(remove_prefixes(ground_truth)))

def f1_score(prediction, prediction_start_char_occurences, ground_truth,):
    if len(prediction) == 0:
    # there is no prediction
        return 0

    if is_answer_from_passage(prediction_start_char_occurences) is False:
        return 0 # return 0 if the predicted answer is not a span from the passage

    prediction_tokens = normalize_text(remove_prefixes(prediction)).split()
    ground_truth_tokens = normalize_text(remove_prefixes(ground_truth)).split()
    common = Counter(prediction_tokens) & Counter(ground_truth_tokens)
    num_same = sum(common.values())
    if num_same == 0:
        return 0
    precision = 1.0 * num_same / len(prediction_tokens)
    recall = 1.0 * num_same / len(ground_truth_tokens)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1

def metric_max_over_ground_truths(metric_fn, prediction, prediction_start_char_list, ground_truths):
            
    scores_for_ground_truths = []
    for ground_truth in ground_truths:
        score = metric_fn(prediction, prediction_start_char_list, ground_truth["text"],)
        scores_for_ground_truths.append(score)
    return max(scores_for_ground_truths)

def pRR_max_over_ground_truths(predictions, start_chars, ground_truths):
    pRR = 0
    while len(predictions)>5:
        predictions.pop()
    for i, prediction in enumerate(predictions):
        rank = i + 1
        f1_scores_for_ground_truths = []
        for ground_truth in ground_truths:
            score = f1_score(prediction, start_chars[i], ground_truth["text"],)
            f1_scores_for_ground_truths.append(score)
        if max(f1_scores_for_ground_truths)!=0:
            pRR = 1.0 * max(f1_scores_for_ground_truths)/rank
            return pRR
    return pRR

def evaluate(dataset_jsonl, ntop_predictions):
    total = 0
    pRR_scores = []
    f1_scores = []
    exact_match_scores = []

    for pq_dict in dataset_jsonl:
        total += 1
        pq_id = pq_dict['pq_id']

        if pq_id not in ntop_predictions:
            message = 'Unanswered question ' + pq_id + \
                      ' will receive score 0.'
            print(message, file=sys.stderr)
            continue
        ground_truths = pq_dict['answers']
        passage = pq_dict['passage']

        ntop_predictions_4pq = ntop_predictions[pq_id]
        predictions = []
        all_predictions_start_char_list = [] # contains the start_char occurences for each predicted answer
        for i in range(len(ntop_predictions_4pq)):
            answer = ntop_predictions_4pq[i]['answer']
            predictions.append(answer)
            start_char_occurences = find_all_occurences(passage, answer)
            all_predictions_start_char_list.append(start_char_occurences)

        first_prediction = predictions[0]
        first_prediction_start_char_list = all_predictions_start_char_list[0]

        pRR = pRR_max_over_ground_truths(predictions, all_predictions_start_char_list, ground_truths)
        exact_match = metric_max_over_ground_truths(
                            exact_match_score, first_prediction, first_prediction_start_char_list, ground_truths)

        f1 = metric_max_over_ground_truths(
                            f1_score, first_prediction, first_prediction_start_char_list, ground_truths)
        
        pRR_scores.append(pRR)
        exact_match_scores.append(exact_match)
        f1_scores.append(f1)

    all_pRR = 1.0 * sum(pRR_scores) / total
    all_exact_match = 1.0 * sum(exact_match_scores) / total
    all_f1 = 1.0 * sum(f1_scores) / total

    return {'pRR': all_pRR, 'exact_match': all_exact_match, 'f1': all_f1}

def load_jsonl(input_path) -> list:
    data = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line.rstrip('\n|\r')))
    print('Loaded {} records from {}'.format(len(data), input_path))
    return data

if __name__ == '__main__':
    version = '1.1'
    parser = argparse.ArgumentParser(
        description='Evaluation for QRCD ' + version)
    parser.add_argument('--run_file', required=True, help='Run file should adopt this naming formt <TeamID_RunID.json>')
    parser.add_argument('--gold_answers_file', help=" Gold JSONL file")
    
    args = parser.parse_args()

    # farasa needed to remove prefixes
    farasa_segmenter = FarasaSegmenter(interactive=True)

    dataset_jsonl = load_jsonl(args.gold_answers_file)

    # check the run file first
    run_file = args.run_file

    if quranqa22_submission_checker.check_submission(run_file) is False:
        print("Please review the above warning(s) or error message(s) related to this run file.")
    else:
        with open(run_file, 'r', encoding='utf-8') as run_file:
            ntop_predictions = json.load(run_file)
        print(json.dumps(evaluate(dataset_jsonl, ntop_predictions)))
