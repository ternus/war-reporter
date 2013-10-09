from base import PanopticStatPlugin
import subprocess

class PanopticNfqueue(PanopticStatPlugin):
    needs_root = True
    diffable = True

    def sample(self):
        
        """
        Get NFQUEUE statistics.
        """
        raw_stats = subprocess.check_output(['iptables', '-xnvL']).split('\n')
        stats = {}
        for line in raw_stats:
            if not line.count('NFQUEUE'): continue
            r = line.split()
            q_num = r[-1]
            if not q_num in stats:
                stats[q_num] = {
                    'packets': int(r[0]),
                    'bandwidth': int(r[1])
                }
            else:
                stats[q_num] = {
                    'packets': int(r[0]) + stats[q_num]['packets'],
                    'bandwidth': int(r[1]) + stats[q_num]['bandwidth']
                }
        self.stats = stats

    def __sub__(self, other):
        rstats = {}
        for nfq in self.stats.keys():
            rstats[nfq] = {}
            for k in self.stats[nfq].keys():
                rstats[nfq][k] = float(self.stats[nfq][k]) - float(other.stats[nfq][k])
        return PanopticNfqueue(rstats)
