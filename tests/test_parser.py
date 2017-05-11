#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import json
import re
from datetime import datetime
from pkg_resources import resource_string, resource_stream
from kgschart import KgsChart


class TestParser(unittest.TestCase):

    def helper(self, file, rank_range, time_range):
        k = KgsChart(file)
        k.parse()
        if rank_range[0] == 'None': rank_range = []  
        rank_range = tuple(rank_range)
        def format_time(a):
            reg1 = re.compile(r'\d{4}\-\d{1,2}\-\d{1,2} \d{1,2}:\d{1,2}')
            reg2 = re.compile(r'\d{4}\-\d{1,2}\-\d{1,2}')
            if reg1.match(a) is not None:
                return datetime.strptime(a, '%Y-%m-%d %H:%M')
            elif reg2.match(a) is not None:
                return datetime.strptime(a, '%Y-%m-%d')
            else:
                return None
        if time_range[0] == 'None': time_range = []
        time_range = [format_time(a) for a in time_range]
        time_range = tuple(time_range)
        #print(time_range)
        #print(k.time_range)
        self.assertEqual(k.rank_range, rank_range)
        self.assertEqual(k.time_range, time_range)

    def test_all_cases(self):
        cases = json.loads( \
            resource_string(__name__, 'data/answers.json').decode())
        print('')
        for case in cases:
            print('*', case['file'], '...')
            with resource_stream(__name__, os.path.join('data', case['file'])) as f:
                self.helper(f, case['rank_range'], case['time_range']) 


if __name__ == '__main__':
    unittest.main()

