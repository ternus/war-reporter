from base import PanopticStatPlugin

class PanopticNetstat(PanopticStatPlugin):

    diffable = False

    def sample(self):
        netstat_lines = [l.split() for l in open('/proc/net/netstat').readlines()]
        netstat = {'tcp_ext': {}, 'ip_ext': {}}
        for i in xrange(1, len(netstat_lines[0]) - 1):
            netstat['tcp_ext'][netstat_lines[0][i]] = netstat_lines[1][i]
        for i in xrange(1, len(netstat_lines[2]) - 1):
            netstat['ip_ext'][netstat_lines[2][i]] = netstat_lines[3][i]
        self.stats = netstat
