import random
from simulator.workload import WorkloadGenerator


class Environment:

    def __init__(self, config=None):

        # ----- Config -----
        self.config = config

        # ----- Workload generator -----
        self.workload = WorkloadGenerator()

        # ----- State -----
        self.users = 0
        self.servers = 1
        self.cpu = 0
        self.memory = 0
        self.resources = 0
        self.latency = 0
        self.energy = 0
        self.cost = 0
        self.temperature = 0
        self.carbon = 0
        self.sla = 0

        self.step_count = 0
        self.mode = "Balanced"
        self.strategy = "Static"

        # ----- Logs -----
        self.history = []

        # ----- Scaling settings -----
        self.max_servers = 10
        self.min_servers = 1

        self.scaling_delay = 1
        self.delay_counter = 0

        self.last_action = 0
        self.instability = 0

        self.server_capacity = 50
        self.server_memory_gb = 16


    # =========================
    # Reset
    # =========================
    def reset(self):

        self.users = 50
        self.servers = 3

        self.cpu = 0
        self.memory = 0
        self.resources = 0
        self.latency = 0
        self.energy = 0
        self.cost = 0
        self.temperature = 0
        self.carbon = 0
        self.sla = 0

        self.step_count = 0
        self.history = []

        self.delay_counter = 0
        self.last_action = 0
        self.instability = 0

        return self.get_state()


    # =========================
    # Step (AWS-like)
    # =========================
    def step(self, action, users_override=None):

        # scaling with delay
        self.apply_scaling(action)

        # realistic workload (or shared external workload for fair comparisons)
        self.generate_workload(users_override)

        # metrics
        self.compute_cpu()
        self.compute_resources()
        self.compute_memory()
        self.compute_latency()
        self.compute_energy()
        self.compute_temperature()
        self.compute_carbon()
        self.compute_cost()
        self.check_sla()

        # reward
        reward = self.compute_reward()

        self.step_count += 1

        self.log_step()

        return reward


    # =========================
    # Workload
    # =========================
    def generate_workload(self, users_override=None):

        if users_override is None:
            self.users = self.workload.get_users()
        else:
            self.users = int(users_override)


    # =========================
    # Scaling
    # =========================
    def apply_scaling(self, action):

        # delay like AWS cooldown
        if self.delay_counter > 0:
            self.delay_counter -= 1
            action = 0
        else:
            if action != 0:
                self.delay_counter = self.scaling_delay

        # instability penalty
        if action != self.last_action:
            self.instability += 1

        self.last_action = action

        self.servers += action

        if self.servers > self.max_servers:
            self.servers = self.max_servers

        if self.servers < self.min_servers:
            self.servers = self.min_servers


    # =========================
    # Metrics
    # =========================
    def compute_cpu(self):

        total_capacity = self.servers * self.server_capacity

        if total_capacity == 0:
            self.cpu = 0
        else:
            self.cpu = self.users / total_capacity


    def compute_resources(self):

        # Total compute resource capacity available in the cloud.
        self.resources = self.servers * self.server_capacity


    def compute_memory(self):

        # Total memory capacity available across all running servers (GB).
        self.memory = self.servers * self.server_memory_gb


    def compute_latency(self):

        self.latency = self.cpu * 0.5


    def compute_energy(self):

        self.energy = self.servers * 5


    def compute_temperature(self):

        self.temperature = 20 + self.cpu * 2


    def compute_carbon(self):

        self.carbon = self.energy * 0.2


    def compute_cost(self):

        self.cost = self.servers * 10 + self.energy


    def check_sla(self):

        if self.latency > 1:
            self.sla = 1
        else:
            self.sla = 0


    # =========================
    # Reward (REALISTIC)
    # =========================
    def compute_reward(self):

        overload_penalty = 0
        under_penalty = 0

        if self.cpu > 1:
            overload_penalty = 100

        if self.cpu < 0.2:
            under_penalty = 10

        reward = -(
            self.cost
            + self.energy
            + self.latency * 5
            + self.sla * 50
            + self.instability * 5
            + overload_penalty
            + under_penalty
        )

        return reward


    # =========================
    # State
    # =========================
    def get_state(self):

        return {
            "users": self.users,
            "servers": self.servers,
            "cpu": self.cpu,
            "resources": self.resources,
            "memory": self.memory,
            "latency": self.latency,
            "energy": self.energy,
            "cost": self.cost,
            "temperature": self.temperature,
            "carbon": self.carbon,
            "sla": self.sla,
            "step": self.step_count,
        }


    # =========================
    # Log
    # =========================
    def log_step(self):

        self.history.append(
            {
                "users": self.users,
                "servers": self.servers,
                "cpu": self.cpu,
                "resources": self.resources,
                "memory": self.memory,
                "latency": self.latency,
                "energy": self.energy,
                "cost": self.cost,
                "sla": self.sla,
                "step": self.step_count,
            }
        )