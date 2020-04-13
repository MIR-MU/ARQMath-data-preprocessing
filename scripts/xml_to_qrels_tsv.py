#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .common import ARQMATH_COLLECTION_INPUT_DATA_DIRNAME, ARQMATH_COLLECTION_QRELS_FILENAME

from arqmathcode.post_reader_record import DataReaderRecord
from tqdm import tqdm


if __name__ == '__main__':
    xml_reader = DataReaderRecord(ARQMATH_COLLECTION_INPUT_DATA_DIRNAME)
    with open(ARQMATH_COLLECTION_QRELS_FILENAME, 'wt') as f:
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
                print('{}\txxx\t{}\t{}'.format(question.post_id, answer.post_id, judgement), file=f)
