# -*- coding:utf-8 -*-

import csv

from arqmathcode.post_reader_record import DataReaderRecord
from tqdm import tqdm

from .configuration import CSV_PARAMETERS, ARQMATH_COLLECTION_INPUT_DATA_DIRNAME, ARQMATH_COLLECTION_QRELS_FILENAME


if __name__ == '__main__':
    xml_reader = DataReaderRecord(ARQMATH_COLLECTION_INPUT_DATA_DIRNAME)
    with open(ARQMATH_COLLECTION_QRELS_FILENAME, 'wt') as f:
        csv_writer = csv.writer(f, **CSV_PARAMETERS)
        questions = tqdm(
            sorted(
                xml_reader.post_parser.map_questions.values(),
                key=lambda question: question.post_id
            ),
            desc='Converting',
        )
        for question in questions:
            for answer in (question.answers or []):
                positive_votes = sum(1 for vote in (answer.votes or []) if vote.vote_type_id == 2)
                negative_votes = sum(1 for vote in (answer.votes or []) if vote.vote_type_id == 3)
                judgement = max(0, positive_votes - negative_votes)
                row = (question.post_id, 'xxx', answer.post_id, judgement)
                csv_writer.writerow(row)
