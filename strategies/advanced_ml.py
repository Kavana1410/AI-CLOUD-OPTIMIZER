import math


class AdvancedML:

    def __init__(self):
        pass

    def get_action(self, env):

        best_servers = env.servers
        best_score = 999999

        users = env.users

        for s in range(1, env.max_servers + 1):

            cpu = users / (s * env.server_capacity)

            latency = cpu * 50

            energy = s * 5

            cost = s * 10 + energy

            sla = 1 if latency > 100 else 0

            score = cost + latency + energy + sla * 100

            if score < best_score:
                best_score = score
                best_servers = s

        action = best_servers - env.servers

        return action