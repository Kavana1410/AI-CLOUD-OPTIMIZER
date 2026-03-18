class ThresholdStrategy:

    def __init__(self,
                 high=0.8,
                 low=0.3,
                 max_servers=10,
                 min_servers=1):

        self.high = high
        self.low = low

        self.max_servers = max_servers
        self.min_servers = min_servers


    def get_action(self, env):

        cpu = env.cpu
        servers = env.servers

        # scale up
        if cpu > self.high:

            if servers < self.max_servers:
                return 1

        # scale down
        if cpu < self.low:

            if servers > self.min_servers:
                return -1

        # no change
        return 0