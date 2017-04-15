# -*- coding: utf-8 -*-

import sys
import re
from datetime import datetime
from argparse import ArgumentParser
from kgschart import KgsChart

# for python2 compatibility
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

    
def main():
    parser = ArgumentParser(description='Parse KGS rank graphs into data')
    parser.add_argument('x', type=str, 
                        help='KGS ID or file path. \
                              If a KGS ID is given, then the recent rank graph is downloaded \
                              from the online archive (internet connection required). \
                              Alternatively, give a path to a local file and set "--local".')
    parser.add_argument('-l', '--local', action='store_true', help='indicates "x" is a local file')
    parser.add_argument('-o', '--outfile', type=str, default=sys.stdout, help='output file path')
    parser.add_argument('-p', '--plot', action='store_true', help='plot image')
    parser.add_argument('--rank-range', type=str, default=None, 
                        help='manually assign rank range of the graph.\
                              Provide comma-separated strings such as: "2k,3d"')
    parser.add_argument('--time-range', type=str, default=None, 
                        help='manually assign date/time range of the graph.\
                              Required format: "%%Y-%%m-%%d [%%H:%%M],%%Y-%%m-%%d [%%H:%%M]"')
    args = parser.parse_args()
    
    if args.local:
        image_file = args.x
    else:
        url = 'http://www.gokgs.com/servlet/graph/%s-ja_JP.png' % args.x
        #print(url)
        image_file = urlopen(url)
    k = KgsChart(image_file)
    k.parse()
    
    
    # manual assignment of rank and/or time
    if args.rank_range is not None:
        r = re.match(r'(\d+[kd]),(\d+[kd])', args.rank_range)
        if r is not None:
            k.set_rank_range(r.groups())
    if args.time_range is not None:
        r = re.match(r'(\d{4}\-\d{1,2}\-\d{1,2})( \d{1,2}:\d{1,2}){0,1},(\d{4}\-\d{1,2}\-\d{1,2})( \d{1,2}:\d{1,2}){0,1}', args.time_range)
        if r is not None:
            g = list(r.groups())
            if g[1] is None: g[1] = '0:00'
            if g[3] is None: g[3] = '0:00'
            d1 = datetime.strptime(g[0] + ' ' + g[1].strip(), '%Y-%m-%d %H:%M')
            d2 = datetime.strptime(g[2] + ' ' + g[3].strip(), '%Y-%m-%d %H:%M')
            k.set_time_range((d1, d2))

    if args.rank_range is not None or args.time_range is not None:
        k.update_data()
        
    if args.plot:
        k.plot_data()
    k.data.to_csv(args.outfile, sep='\t', index=False)

