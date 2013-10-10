from base import PanopticStatPlugin
import subprocess

class PanopticProcStat(PanopticStatPlugin):
    diffable = True

    """
    cpu  21226 4020 59518 575726459 15891 12 7163 0 0 0
    cpu0 2369 835 3199 71946204 15357 2 1032 0 0 0
    cpu1 2380 637 2901 71967444 214 0 821 0 0 0
    cpu2 1364 906 4291 71971861 52 2 1268 0 0 0
    cpu3 1824 558 5144 71967775 27 1 1580 0 0 0
    cpu4 3668 246 3595 71976039 51 1 277 0 0 0
    cpu5 3431 237 3196 71970559 48 0 236 0 0 0
    cpu6 3235 198 30384 71961610 75 0 176 0 0 0
    cpu7 2951 400 6806 71964963 64 3 1770 0 0 0
    intr 70636869 2441 0 0 0 0 0 0 0 1 0 0 0 0 0 [...etc]
    ctxt 14402348
    btime 1380654314
    processes 141751
    procs_running 1
    procs_blocked 0
    softirq 73860616 0 4117551 287958 60828318 60012 0 4 3506639 540 5059594
    """

    def sample(self):

        raw_stats = [l.split() for l in open('/proc/stat', 'r').readlines()]
        stats = {}

        def get_cpu(line):
            c = {}
            for i,v in enumerate(['user', 'nice', 'system', 'idle', 'iowait', 'irq', 'softirq']):
                c[v] = int(line[i+1])
            return c
        
        stats['cpu'] = {}
        stats['cpu']['total'] = get_cpu(raw_stats[0])
        for line in raw_stats[1:]:
            if not line[0].startswith('cpu'): break
            stats['cpu'][int(line[0][-1])] = get_cpu(line)

        
        self.stats = stats

    def __sub__(self, other):
        rstats = {'cpu': {}}
        for cpu in self.stats['cpu'].keys():
            rstats['cpu'][cpu] = {}
            for k in self.stats['cpu'][cpu].keys():
                rstats['cpu'][cpu][k] = self.stats['cpu'][cpu][k] - other.stats['cpu'][cpu][k]
        c = PanopticProcStat()
        c.set_stats(rstats)
        return c
