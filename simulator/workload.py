import math
import random


class WorkloadGenerator:

    def __init__(self):

        self.step = 0

        self.base_users = 150

        self.max_users = 600
        self.min_users = 10


    # =========================
    # Main function
    # =========================
    def get_users(self):

        self.step += 1

        daily = self.daily_pattern()
        weekly = self.weekly_pattern()
        noise = self.random_noise()
        spike = self.spike()
        attack = self.attack()
        failure = self.failure()

        users = (
            self.base_users
            + daily
            + weekly
            + noise
            + spike
            + attack
            + failure
        )

        # limit users
        users = max(self.min_users, users)
        users = min(self.max_users, users)

        return int(users)


    # =========================
    # Daily pattern (peak hours)
    # =========================
    def daily_pattern(self):

        # sine wave cycle
        return 80 * math.sin(self.step / 6)


    # =========================
    # Weekly pattern (slow change)
    # =========================
    def weekly_pattern(self):

        return 40 * math.sin(self.step / 40)


    # =========================
    # Random noise
    # =========================
    def random_noise(self):

        return random.randint(-15, 15)


    # =========================
    # Traffic spike (burst)
    # =========================
    def spike(self):

        if random.random() < 0.04:
            return random.randint(80, 200)

        return 0


    # =========================
    # Attack / sudden surge
    # =========================
    def attack(self):

        if random.random() < 0.01:
            return random.randint(200, 350)

        return 0


    # =========================
    # Failure / drop
    # =========================
    def failure(self):

        if random.random() < 0.02:
            return -random.randint(50, 120)

        return 0