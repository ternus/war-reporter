from base import PanopticStatPlugin
import subprocess

class PanopticIOStat(PanopticStatPlugin):
    diffable = False

    """
    Example output of iostat command:
    
    Linux 3.2.44-3.2.1.3-amd64-10875514 (foo.bar.com) 	10/10/13

    avg-cpu:  %user   %nice %system %iowait  %steal   %idle
               0.29    0.00    0.91    0.00    0.00   98.79

    Device:            tps   Blk_read/s   Blk_wrtn/s   Blk_read   Blk_wrtn
    sdb               1.97         0.09        43.69      61998   31801992
    sdb1              1.79         0.08        41.81      56712   30438680
    sdb2              0.19         0.00         1.87       1586    1363304
    sdb3              0.00         0.00         0.00       1176          0
    sdb4              0.00         0.00         0.00       2140          8
    sda               2.02         0.85        22.57     618914   16430648
    sda1              0.42         0.14         3.60     104520    2621888
    sda2              0.11         0.14         1.43     101050    1043720
    sda3              1.11         0.52        11.38     377394    8283576
    sda4              0.38         0.05         6.16      35558    4481464
    """

    def sample(self):
        raw_stats = [l.split() for l in subprocess.check_output(['iostat']).split('\n')]
        stats = {}

        host_data = raw_stats[0]
        stats['sys_type'] = host_data[0]
        stats['kernel'] = host_data[1]
        stats['hostname'] = host_data[2][1:-1]
        
        cpu_data = raw_stats[3]
        stats['user_cpu'] = cpu_data[0]
        stats['nice_cpu'] = cpu_data[1]
        stats['system_cpu'] = cpu_data[2]
        stats['iowait_cpu'] = cpu_data[3]
        stats['steal_cpu'] = cpu_data[4]
        stats['idle_cpu'] = cpu_data[5]

        self.stats = stats
