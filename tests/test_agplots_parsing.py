#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2013, The American Gut Project"
__credits__ = ["Sam Way"]
__license__ = "BSD"
__version__ = "unversioned"
__maintainer__ = "Sam Way"
__email__ = "samuel.way@colorado.edu"

from americangut.agplots_parse import (parse_mapping_file_to_dict,
                                       get_filtered_taxa_summary)
from numpy import array, array_equal
import numpy.testing as npt
from unittest import TestCase, main


TEST_MAPPING_FILE = './files/test_mapping.txt'
TEST_TAXA_FILE = './files/test_taxa.txt'


class test_mapping_file_parse(TestCase):
    def setUp(self):
        self.categories = ['TEST_CATEGORY', 'AWESOME_CATEGORY']
        self.sample_ids = ['sample_a', 'sample_b']
        self.metadata_dict = {'sample_a': {'TEST_CATEGORY': '1',
                                           'AWESOME_CATEGORY': 'super'},
                              'sample_b': {'TEST_CATEGORY': '2',
                                           'AWESOME_CATEGORY': 'totally'}}

    def test_mapping_file(self):
        with open(TEST_MAPPING_FILE) as f:
            mapping_dict, comments = parse_mapping_file_to_dict(f)

        for sample_id, sample_dict in mapping_dict.iteritems():
            # Does the sample dictionary contain all of the metadata
            # categories?
            self.assertEqual(set(sample_dict.keys()), set(self.categories))

            # Are all metadata values correct?
            for category in sample_dict:
                self.assertEqual(sample_dict[category],
                                 self.metadata_dict[sample_id][category])


class test_taxa_summary_file_parse(TestCase):
    def setUp(self):
        self.sample_ids = ['sample_a', 'sample_b']
        self.table = array([[0.11, 0.15],
                            [0.12, 0.14],
                            [0.13, 0.13],
                            [0.14, 0.12],
                            [0.15, 0.11],
                            [0.16, 0.10],
                            [0.09, 0.09],
                            [0.10, 0.16]])
        self.taxa_ids = ['Firmicutes', 'Bacteroidetes',
                         'Proteobacteria', 'Verrucomicrobia', 'Actinobacteria',
                         'Tenericutes', 'Cyanobacteria']
        self.taxa_labels = self.taxa_ids + ['Other']
        self.metadata_category = 'TEST_CATEGORY'
        self.metadata_value = '1'

    def test_taxa_file(self):
        filtered_sample_ids, taxa_labels, collapsed_taxa_table = \
            get_filtered_taxa_summary(TEST_MAPPING_FILE, TEST_TAXA_FILE,
                                      self.metadata_category,
                                      self.metadata_value,
                                      select_taxa=self.taxa_ids)

        # Make sure we only get out the matching sample
        self.assertEqual(len(filtered_sample_ids), 1)
        self.assertEqual(filtered_sample_ids[0], 'sample_a')

        # Should get back our desired labels + "Others"
        self.assertEqual(set(self.taxa_labels), set(taxa_labels))

        # Should get the slide of the table corresponding to the matching
        # sample
        npt.assert_equal(collapsed_taxa_table, self.table[:, 0, None])

if __name__ == '__main__':
    main()

