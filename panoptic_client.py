#!/usr/bin/env python
import sys, os
import copy
import time
import subprocess
import json
import urllib2
import argparse
import importlib
import inspect
from panoptic.modules.base import PanopticStatPlugin

def submit_stats(stats, url):
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    print "submitting..."
    return urllib2.urlopen(req, serialize(stats))

def collect(plugins, kwargs):
    stats = {}
    for plugin in plugins:
        p = plugin(**kwargs)
        p.sample()
        stats[plugin.replace('Panoptic', '')] = p
    return stats

def serialize(stats):
    json_stats = {}
    json_stats['time'] = time.time()
    json_stats['hostname'] = open('/etc/hostname').read().strip()

    for s in stats:
        if inspect.isclass(s):
            json_stats[s.__name__] = stats[s].stats
    return json.dumps(json_stats)

def collect_and_submit(stats, kwargs):
    new_stats = collect(loaded_plugins, kwargs)
    sub_stats = copy.deepcopy(new_stats)
    for p in loaded_plugins:
        if p.diffable:
            sub_stats[p] = new_stats[p] - stats[p]
    submit_stats(sub_stats, args.url)
    return new_stats

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url', metavar='collector_url', help="URL of the collector server.")
    parser.add_argument('plugin', nargs='+')
    parser.add_argument('--interface', metavar='interface', help="Network interface to collect data from.")
    parser.add_argument('--timeout', metavar='timeout', help="Number of seconds to collect data.", default=0)
    parser.add_argument('--sample-rate', metavar='rate', help="Number of seconds between data points.", default=1)
    args = parser.parse_args()

    kwargs = {}
    if args.interface:
        kwargs['interface'] = args.interface
    
    loaded_plugins = []
    for plugin in args.plugin:
        try:
            m = importlib.import_module('panoptic.modules.%s' % plugin)
            # dynamic module loading
            # also known as "WTF HAX"
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

    stats = collect(loaded_plugins, kwargs)
    start_time = time.time()
    timeout = int(args.timeout)
    print "Running..."
    while (timeout == 0 or time.time() < start_time + timeout):
        stats = collect_and_submit(stats, kwargs)
        time.sleep(args.sample_rate)
    print "Done."
