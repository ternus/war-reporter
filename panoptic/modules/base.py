class PanopticStatPlugin(object):
    needs_root = False
    name = 'PanopticStatPlugin'
    stats = {}
    kwargs = {}

    def __init__(self, *args, **kwargs):
        self.stats = {}
        if len(args):
            self.stats = args[0]
        self.kwargs = kwargs # hax, I know

    def sample(self, *args):
        pass


    def as_json(self):
        return json.dumps(self.stats)

    def __sub__(self, other):
        nstats = {}
        for k in self.stats.keys():
            nstats[k] = float(stats_new[k]) - float(self.stats[k])
        return self.__class__(nstats, self.kwargs)
