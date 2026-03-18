import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from simulator.environment import Environment
from strategies.rl_agent import RLAgent


def train():

    env = Environment()

    agent = RLAgent()

    episodes = 30

    for ep in range(episodes):

        state = env.reset()

        total_reward = 0

        for step in range(50):

            action = agent.get_action(env)

            next_state, reward = env.step(action)

            agent.learn(env, action, reward)

            total_reward += reward

        print("Episode", ep, "Reward:", total_reward)


if __name__ == "__main__":
    train()