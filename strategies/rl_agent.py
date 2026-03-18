import random


class RLAgent:

    def __init__(self):

        self.actions = [-2, -1, 0, 1, 2]

        self.q_table = {}

        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.2


    # =========================
    # State (IMPROVED)
    # =========================
    def get_state_key(self, env):

        users = int(env.users / 20)   # reduce range
        servers = env.servers
        cpu = int(env.cpu * 10)
        latency = int(env.latency * 10)

        return (users, servers, cpu, latency)


    # =========================
    # Action
    # =========================
    def get_action(self, env):

        state = self.get_state_key(env)

        if state not in self.q_table:
            self.q_table[state] = {a: 0 for a in self.actions}

        # exploration
        if random.random() < self.epsilon:
            return random.choice(self.actions)

        # exploitation
        return max(self.q_table[state], key=self.q_table[state].get)


    # =========================
    # Learn
    # =========================
    def learn(self, env, action, reward):

        state = self.get_state_key(env)

        if state not in self.q_table:
            self.q_table[state] = {a: 0 for a in self.actions}

        old_value = self.q_table[state][action]

        # simple Q update
        new_value = old_value + self.alpha * (reward - old_value)

        self.q_table[state][action] = new_value