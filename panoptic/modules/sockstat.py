from base import PanopticStatPlugin

class PanopticSockstat(PanopticStatPlugin):

    diffable = False

    def sample(self):
        """
        Example file contents:
        sockets: used 786
        TCP: inuse 149 orphan 0 tw 25 alloc 152 mem 34
        UDP: inuse 124 mem 8230
        UDPLITE: inuse 0
        RAW: inuse 8
        FRAG: inuse 0 memory 0
        """
        r = open('/proc/net/sockstat').read().split()
        self.stats = {'tcp_inuse': r[2],
                'tcp_orphan': r[4],
                'tcp_tw': r[6],
                'tcp_alloc': r[8],
                'tcp_mem': r[10],
                'udp_inuse': r[13],
                'udp_mem': r[15],
                'udplite_inuse': r[18],
                'raw_inuse': r[21],
                'frag_inuse': r[24],
                'frag_mem': r[26]
        }


