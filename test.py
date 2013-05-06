#! /usr/bin/python
# -*- coding: utf-8 -*-

import pickle, unittest
import cluster

class TestSequenceFunctions(unittest.TestCase):
    def test_full_cluster(self):
        cluster.main(["data/jeans.pkl"])

if __name__ == '__main__':
    unittest.main()

