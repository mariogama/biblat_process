# coding: utf-8
import os
import gzip
import unittest
import json
from biblat_process.marc2dict import Marc2Dict


class TestMarc2Dict(unittest.TestCase):

    def setUp(self):
        self.test_path = os.path.dirname(os.path.realpath(__file__))
        self.test_files_path = os.path.join(self.test_path, 'test_files')
        self.config = {
            'local_path': self.test_files_path,
        }

        for root, paths, files in os.walk(self.test_files_path):
            for file in files:
                if file.endswith('.txt'):
                    with open(os.path.join(root, file), mode='rb') as f_in, \
                            gzip.open(os.path.join(root, file + '.gz'),
                                      'wb') as f_out:
                        f_out.writelines(f_in)

    def tearDown(self):
        for root, paths, files in os.walk(self.test_files_path):
            for file in files:
                if file.endswith('.gz'):
                    os.unlink(os.path.join(root, file))

    def test_cla01_basic(self):
        self.maxDiff = None
        self.config['db_files'] = 'test_cla01.txt.gz'
        marc2dict = Marc2Dict(self.config)
        marc_dicts = []

        for marc_dict in marc2dict.get_dict():
            marc_dicts.append(marc_dict)

        with open(os.path.join(self.test_files_path, 'test_cla01.json'),
                  encoding='utf-8') as cla01_json:
            marc_dict_expected = json.load(cla01_json)

        self.assertDictEqual(marc_dict_expected, marc_dicts[0])
        self.assertEqual(1, len(marc_dicts))

    def test_per01_basic(self):
        self.maxDiff = None
        self.config['db_files'] = 'test_per01.txt.gz'
        marc2dict = Marc2Dict(self.config)
        marc_dicts = []

        for marc_dict in marc2dict.get_dict():
            marc_dicts.append(marc_dict)
        with open(os.path.join(self.test_files_path, 'test_per01.json'),
                  encoding='utf-8') as per01_json:
            marc_dict_expected = json.load(per01_json)

        self.assertDictEqual(marc_dict_expected, marc_dicts[0])
        self.assertEqual(1, len(marc_dicts))

    def test_claper_length(self):
        self.maxDiff = None
        self.config['db_files'] = 'test_cla01.txt.gz,test_per01.txt.gz'
        marc2dict = Marc2Dict(self.config)
        marc_dicts = []

        for marc_dict in marc2dict.get_dict():
            marc_dicts.append(marc_dict)

        with open(os.path.join(self.test_files_path, 'test_per01.json'),
                  encoding='utf-8') as per01_json, \
                open(os.path.join(self.test_files_path, 'test_cla01.json'),
                     encoding='utf-8') as cla01_json:
            cla01_dict = json.load(cla01_json)
            per01_dict = json.load(per01_json)

            self.assertEqual(2, len(marc_dicts))
            self.assertDictEqual(cla01_dict, marc_dicts[0])
            self.assertDictEqual(per01_dict, marc_dicts[1])
