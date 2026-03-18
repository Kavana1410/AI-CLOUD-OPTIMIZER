import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from simulator.environment import Environment
from strategies.deep_rl import DeepRL


def train():

    env = Environment()

    agent = DeepRL()

    episodes = 500

    for ep in range(episodes):

        env.reset()

        total = 0

        for step in range(50):

            action = agent.get_action(env)

            reward = env.step(action)

            if isinstance(reward, tuple):
                reward = reward[0]

            if isinstance(reward, dict):
                reward = 0

            agent.learn(env, action, reward)

            total += reward

        print("Episode", ep, "Reward:", total)


if __name__ == "__main__":
    train()
