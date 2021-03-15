# -*- coding: utf-8 -*-
"""
@author: hswalsh
Test code for preprocessing and related functions.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")

import unittest

from topic_model_plus_class import Topic_Model_plus

class test_preprocessing_methods(unittest.TestCase):
    def test_tokenize_texts(self):
        test_class = Topic_Model_plus()
        test_tokenize_texts_result = test_class._Topic_Model_plus__tokenize_texts(['the quick brown fox jumps over the lazy dog'])
        correct_tokenization = [['the','quick','brown','fox','jumps','over','the','lazy','dog']]
        self.assertEqual(test_tokenize_texts_result,correct_tokenization)
    def test_quot_normalize(self):
        test_class = Topic_Model_plus()
        test_quot_normalize_result = test_class._Topic_Model_plus__quot_normalize([['quotation','devicequot','quotring','adaquotpt']])
        correct_quot_normalization = [['quotation','device','ring','adapt']]
        self.assertEqual(test_quot_normalize_result,correct_quot_normalization)
    def test_spellchecker(self):
        test_class = Topic_Model_plus()
        test_spellchecker_result = test_class._Topic_Model_plus__spellchecker([['strted','nasa','NASA','CalTech','pyrolitic']])
        correct_spellcheck = [['started','casa','NASA','CaTch','pyrolytic']]
        self.assertEqual(test_spellchecker_result,correct_spellcheck)
    def test_segment_text(self):
        test_class = Topic_Model_plus()
        test_segment_text_result = test_class._Topic_Model_plus__segment_text([['devicesthe','nasa','correct']])
        correct_segmentation = [['devices','the','as','a','correct']]
        self.assertEqual(test_segment_text_result,correct_segmentation)

if __name__ == '__main__':
    unittest.main()
