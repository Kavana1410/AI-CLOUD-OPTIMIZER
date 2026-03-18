import torch
import torch.nn as nn
import torch.optim as optim
import random


class DQN(nn.Module):

    def __init__(self):

        super().__init__()

        self.model = nn.Sequential(
            nn.Linear(2, 16),
            nn.ReLU(),
            nn.Linear(16, 3)
        )

    def forward(self, x):
        return self.model(x)


class DeepRL:

    def __init__(self):

        self.net = DQN()

        self.optimizer = optim.Adam(self.net.parameters(), lr=0.01)

        self.loss_fn = nn.MSELoss()

        self.actions = [-1, 0, 1]

    def get_state(self, env):

        return torch.tensor(
            [env.users, env.servers],
            dtype=torch.float32
        )

    def get_action(self, env):

        state = self.get_state(env)

        with torch.no_grad():
            q = self.net(state)

        action_index = torch.argmax(q).item()

        return self.actions[action_index]

    def learn(self, env, action, reward):

        state = self.get_state(env)

        q_values = self.net(state)

        target = q_values.clone().detach()

        index = self.actions.index(action)

        target[index] = reward

        loss = self.loss_fn(q_values, target)

        self.optimizer.zero_grad()

        loss.backward()

        self.optimizer.step()