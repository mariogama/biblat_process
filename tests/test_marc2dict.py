# coding: utf-8
import os
import gzip
import unittest
import json
from biblat_process.marc2dict import Marc2Dict
from biblat_process.settings import config


class TestMarc2Dict(unittest.TestCase):

    def setUp(self):
        self.test_path = os.path.dirname(os.path.realpath(__file__))
        self.test_files_path = os.path.join(self.test_path, 'test_files')

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
        config.DB_FILES = ['test_cla01.txt.gz']
        marc2dict = Marc2Dict()
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
        config.DB_FILES = ['test_per01.txt.gz']
        marc2dict = Marc2Dict()
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
        config.DB_FILES = ['test_cla01.txt.gz', 'test_per01.txt.gz']
        marc2dict = Marc2Dict()
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

    def test_cla01_length(self):
        self.maxDiff = None
        config.DB_FILES = ['test_cla01_length.txt.gz']
        marc2dict = Marc2Dict()
        marc_dicts = []

        for marc_dict in marc2dict.get_dict():
            marc_dicts.append(marc_dict)

        with open(os.path.join(self.test_files_path, 'test_cla01_length.json'),
                  encoding='utf-8') as cla01_length_json:
            marc_dicts_expected = json.load(cla01_length_json)

            self.assertEqual(2, len(marc_dicts))
            self.assertDictEqual(marc_dicts_expected[0], marc_dicts[0])
            self.assertDictEqual(marc_dicts_expected[1], marc_dicts[1])

    def test_120_as_100(self):
        """Prueba para verificar etiqueta 120 como 100"""
        self.maxDiff = None
        config.DB_FILES = ['test_120_as_100.txt.gz']
        marc2dict = Marc2Dict()
        marc_dicts = []

        for marc_dict in marc2dict.get_dict():
            marc_dicts.append(marc_dict)

        with open(os.path.join(self.test_files_path, 'test_120_as_100.json'),
                  encoding='utf-8') as json_120_as_100:
            marc_dict_expected = json.load(json_120_as_100)

        self.assertDictEqual(marc_dict_expected, marc_dicts[0])
        self.assertEqual(1, len(marc_dicts))

    def test_120_in_100(self):
        """Prueba para verificar etiqueta 120 en 100"""
        self.maxDiff = None
        config.DB_FILES = ['test_120_in_100.txt.gz']
        marc2dict = Marc2Dict()
        marc_dicts = []

        for marc_dict in marc2dict.get_dict():
            marc_dicts.append(marc_dict)

        with open(os.path.join(self.test_files_path, 'test_120_in_100.json'),
                  encoding='utf-8') as json_120_in_100:
            marc_dict_expected = json.load(json_120_in_100)

        self.assertDictEqual(marc_dict_expected, marc_dicts[0])
        self.assertEqual(1, len(marc_dicts))

    def test_fix_100z(self):
        """"Prueba para verificar la corrección del sub-campo 100z encontrado
        como otro sub-campo"""
        self.maxDiff = None
        config.DB_FILES = ['test_fix_100z.txt.gz']
        marc2dict = Marc2Dict()
        marc_dicts = []

        for marc_dict in marc2dict.get_dict():
            marc_dicts.append(marc_dict)

        with open(os.path.join(self.test_files_path, 'test_fix_100z.json'),
                  encoding='utf-8') as fix_100z_json:
            marc_dict_expected = json.load(fix_100z_json)

        self.assertDictEqual(marc_dict_expected, marc_dicts[0])
        self.assertEqual(1, len(marc_dicts))

    def test_subfield_dup(self):
        """Prueba para verificar cuando un sub-campo esta duplicado"""
        self.maxDiff = None
        config.DB_FILES = ['test_subfield_dup.txt.gz']
        marc2dict = Marc2Dict()
        marc_dicts = []

        for marc_dict in marc2dict.get_dict():
            marc_dicts.append(marc_dict)

        with open(os.path.join(self.test_files_path, 'test_subfield_dup.json'),
                  encoding='utf-8') as subfield_dup_json:
            marc_dict_expected = json.load(subfield_dup_json)

        self.assertDictEqual(marc_dict_expected, marc_dicts[0])
        self.assertEqual(1, len(marc_dicts))

    def test_field_ind(self):
        self.maxDiff = None
        config.DB_FILES = ['test_field_ind.txt.gz']
        marc2dict = Marc2Dict()
        marc_dicts = []

        for marc_dict in marc2dict.get_dict():
            marc_dicts.append(marc_dict)

        with open(os.path.join(self.test_files_path, 'test_field_ind.json'),
                  encoding='utf-8') as field_ind_json:
            marc_dict_expected = json.load(field_ind_json)

        self.assertDictEqual(marc_dict_expected, marc_dicts[0])
        self.assertEqual(1, len(marc_dicts))
