import random


class MLStrategy:

    def __init__(self):
        pass


    def predict_users(self, env):

        # simple prediction (moving average style)

        noise = random.randint(-20, 20)

        predicted = env.users + noise

        if predicted < 0:
            predicted = 0

        return predicted


    def get_action(self, env):

        predicted_users = self.predict_users(env)

        capacity = env.servers * env.server_capacity

        # if predicted load exceeds capacity → scale up
        if predicted_users > capacity:

            return 1

        # if capacity too large → scale down
        if capacity > predicted_users * 2:

            return -1

        return 0