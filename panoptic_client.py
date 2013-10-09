#!/usr/bin/env python

import sys, os
import time
import subprocess
import json
import urllib2
import argparse
import importlib
import inspect
from panoptic.modules.base import PanopticStatPlugin

def submit_stats(stats, url):
    req = urllib2.Request(COLLECTOR_URL)
    req.add_header('Content-Type', 'application/json')
    return urllib2.urlopen(req, json.dumps(stats))

def collect_stat(plugin):
    p = plugin()
    try:
        return p.sample()
    except:
        return {}

def collect(plugins):
    stats = {}
    for p in plugins:
        stats[p] = collect_stat(plugin)
    return stats

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url', metavar='collector_url', help="URL of the collector server.")
    parser.add_argument('plugin', nargs='+')
    parser.add_argument('--interface', metavar='interface', help="Network interface to collect data from.")
    parser.add_argument('--timeout', metavar='timeout', help="Number of seconds to collect data.", default=0)
    parser.add_argument('--sample-rate', metavar='rate', help="Number of seconds between data points.", default=1)
    args = parser.parse_args()
    
    loaded_plugins = []
    for plugin in args.plugin:
        try:
            m = importlib.import_module('panoptic.modules.%s' % plugin)
            # WTF HAX
            for i in m.__dict__:
                if i == 'PanopticStatPlugin': continue
                if inspect.isclass(m.__dict__[i]):
                    if issubclass(m.__dict__[i], PanopticStatPlugin):
                        loaded_plugins.append(m.__dict__[i])
        except ImportError:
            print "Plugin %s not found." % plugin
            sys.exit(1)

    for p in loaded_plugins:
        if p.needs_root and os.geteuid():
            print "Plugin %s needs root and you are not root." % p.__name__
            sys.exit(1)

    stats = collect(loaded_plugins)

    print stats
    
