from simulator.environment import Environment
import argparse
import time

from strategies.static import StaticStrategy
from strategies.threshold import ThresholdStrategy
from strategies.ml_strategy import MLStrategy
from strategies.rl_agent import RLAgent
from strategies.advanced_ml import AdvancedML

from core.results import save_results
from simulator.workload import WorkloadGenerator


def _load_deep_rl_class():

    try:
        from strategies.deep_rl import DeepRL
        return DeepRL
    except Exception:
        return None


# ----------------------
# run one strategy
# ----------------------

def run_strategy(name, strategy, workload_trace=None, steps=50):

    env = Environment()

    env.reset()

    total_reward = 0

    for step_idx in range(steps):

        action = strategy.get_action(env)

        users_override = None
        if workload_trace is not None and step_idx < len(workload_trace):
            users_override = workload_trace[step_idx]

        reward = env.step(action, users_override=users_override)

        if not isinstance(reward, (int, float)):
            reward = 0

        total_reward += reward

    # return FULL metrics

    return {
        "strategy": name,
        "reward": total_reward,
        "cost": env.cost,
        "latency": env.latency,
        "energy": env.energy,
        "sla": env.sla,
        "carbon": env.carbon,
        "servers": env.servers,
        "resources": env.resources,
        "memory": env.memory,
        "max_servers": env.max_servers,
        "cloud_resource_capacity": env.max_servers * env.server_capacity,
        "cloud_memory_capacity": env.max_servers * env.server_memory_gb,
        "users": env.users,
    }


# ----------------------
# run all
# ----------------------

def run_all():

    steps = 50
    workload = WorkloadGenerator()
    shared_workload = [workload.get_users() for _ in range(steps)]

    results = []

    results.append(
        run_strategy("STATIC", StaticStrategy(), workload_trace=shared_workload, steps=steps)
    )

    results.append(
        run_strategy("THRESHOLD", ThresholdStrategy(), workload_trace=shared_workload, steps=steps)
    )

    results.append(
        run_strategy("ML", MLStrategy(), workload_trace=shared_workload, steps=steps)
    )

    results.append(
        run_strategy("RL", RLAgent(), workload_trace=shared_workload, steps=steps)
    )

    results.append(
        run_strategy("ADVANCED", AdvancedML(), workload_trace=shared_workload, steps=steps)
    )

    deep_rl_class = _load_deep_rl_class()
    if deep_rl_class is not None:
        results.append(
            run_strategy("DEEP_RL", deep_rl_class(), workload_trace=shared_workload, steps=steps)
        )

    return results


# ----------------------
# run one
# ----------------------

def run_one(name):

    mapping = {
        "STATIC": StaticStrategy,
        "THRESHOLD": ThresholdStrategy,
        "ML": MLStrategy,
        "RL": RLAgent,
        "ADVANCED": AdvancedML,
    }

    deep_rl_class = _load_deep_rl_class()
    if deep_rl_class is not None:
        mapping["DEEP_RL"] = deep_rl_class

    if name not in mapping:
        return None

    return run_strategy(name, mapping[name]())


def run_and_save_once():

    results = run_all()
    save_results(results)

    return results


def run_continuous(interval_seconds=3.0):

    print("Starting continuous backend simulation. Press Ctrl+C to stop.\n")

    iteration = 0

    while True:

        iteration += 1
        results = run_and_save_once()

        print(f"[tick {iteration}] results updated")

        for result in results:
            print(
                f"  {result['strategy']}: users={result['users']} servers={result['servers']} latency={result['latency']:.3f}"
            )

        print()
        time.sleep(interval_seconds)


# ----------------------
# main
# ----------------------

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="AI Cloud Optimizer simulation runner")
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run only one simulation cycle and exit",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=3.0,
        help="Seconds between simulation cycles in continuous mode",
    )
    args = parser.parse_args()

    if args.once:
        results = run_and_save_once()

        print("\nFINAL RESULTS\n")
        for r in results:
            print(r)
    else:
        try:
            run_continuous(interval_seconds=max(0.5, args.interval))
        except KeyboardInterrupt:
            print("\nSimulation stopped by user.")