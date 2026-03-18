class StaticStrategy:

    def __init__(self, servers=3):
        self.servers = servers


    def get_action(self, env):

        current = env.servers

        # difference from desired servers
        diff = self.servers - current

        # limit action to -2 to +2
        if diff > 2:
            return 2

        if diff < -2:
            return -2

        return diff