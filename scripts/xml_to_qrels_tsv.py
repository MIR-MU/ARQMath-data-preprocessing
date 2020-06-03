# -*- coding:utf-8 -*-

import csv
import sys

from arqmathcode.post_reader_record import DataReaderRecord
from arqmathcode.topic_file_reader import TopicReader
from tqdm import tqdm

from .configuration import CSV_PARAMETERS, ARQMATH_COLLECTION_INPUT_DATA_DIRNAME, ARQMATH_COLLECTION_QRELS_FILENAME, ARQMATH_TASK2_QRELS_FILENAME, ARQMATH_TASK2_TEST_INPUT_POSTS_FILENAME


assert sys.argv[1] in ('collection', 'task2-topics-formula_ids')
if sys.argv[1] == 'collection':
    ARQMATH_QRELS_FILENAME = ARQMATH_COLLECTION_QRELS_FILENAME
elif sys.argv[1] == 'task2-topics-formula_ids':
    ARQMATH_QRELS_FILENAME = ARQMATH_TASK2_QRELS_FILENAME


if __name__ == '__main__':
    if sys.argv[1] == 'collection':
        xml_reader = DataReaderRecord(ARQMATH_COLLECTION_INPUT_DATA_DIRNAME)
        questions = xml_reader.post_parser.map_questions.values()
        questions = sorted(questions, key=lambda question: question.post_id)
    elif sys.argv[1] == 'task2-topics-formula_ids':
        xml_reader = TopicReader(ARQMATH_TASK2_TEST_INPUT_POSTS_FILENAME)
        questions = xml_reader._TopicReader__map_topics.values()
        questions = sorted(questions, key=lambda question: question.topic_id)
    with open(ARQMATH_QRELS_FILENAME, 'wt') as f:
        csv_writer = csv.writer(f, **CSV_PARAMETERS)
        questions = tqdm(questions, desc='Converting')
        for question in questions:
            if sys.argv[1] == 'collection':
                for answer in (question.answers or []):
                    positive_votes = sum(1 for vote in (answer.votes or []) if vote.vote_type_id == 2)
                    negative_votes = sum(1 for vote in (answer.votes or []) if vote.vote_type_id == 3)
                    judgement = max(0, positive_votes - negative_votes)
                    row = (question.post_id, 'xxx', answer.post_id, judgement)
                    csv_writer.writerow(row)
            elif sys.argv[1] == 'task2-topics-formula_ids':
                answer = question.title
                row = (answer, 'xxx', question.topic_id, 0)
                csv_writer.writerow(row)
