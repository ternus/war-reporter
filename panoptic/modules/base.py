import json

class PanopticStatPlugin(object):
    needs_root = False
    name = 'PanopticStatPlugin'
    stats = {}
    kwargs = {}
    
    def __init__(self, *args, **kwargs):
        pass

    def sample(self, *args):
        pass

    def set_stats(self, stats):
        self.stats = stats

    def as_json(self):
        return json.dumps(self.stats)

    def __sub__(self, other):
        nstats = {}
        for k in self.stats.keys():
            nstats[k] = float(self.stats[k]) - float(other.stats[k])
        c = self.__class__(**self.kwargs)
        c.set_stats(nstats)
        
        return c
        
