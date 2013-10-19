from base import PanopticStatPlugin

class PanopticIFStats(PanopticStatPlugin):
    interface = 'eth0'
    diffable = True

    def __init__(self, *args, **kwargs):
        if 'interface' in kwargs:
            self.interface = kwargs['interface']
            del kwargs['interface']
        self.kwargs = kwargs
        return super(PanopticIFStats, self).__init__(*args, **kwargs)

    def sample(self):
        raw_dev_stats = open('/proc/net/dev', 'r').readlines()
        for line in raw_dev_stats:
            if not line.count(self.interface): continue
            r = line.split()
            self.stats = {'pkt_in': r[2],
                'pkt_out': r[10],
                'err_in': r[3],
                'err_out': r[11],
                'drop_in': r[4],
                'drop_out': r[12],
                'bandwidth_in': r[1],
                'bandwidth_out': r[9]
                }
