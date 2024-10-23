import random
random.seed(43)

# --- Bandit ---
class BinaryBandit:
    def __init__(self):
        self.N = 2  # Number of arms
    def actions(self):
        return list(range(self.N))  # Returns available actions as [0, 1]
    
    def reward1(self, action):
        probabilities = [0.1, 0.2]
        return 1 if random.random() < probabilities[action] else 0

    def reward2(self, action):
        probabilities = [0.8, 0.9]
        return 1 if random.random() < probabilities[action] else 0


# Epsilon-Greedy algorithm
def eGreedy_binary(bandit, epsilon, max_iterations):
    # Initialize estimates and counters
    Q = [0] * bandit.N
    counts = [0] * bandit.N
    total_rewards = []
    avg_rewards = [0]

    # Loop through iterations
    for t in range(1, max_iterations):
        # Select action based on epsilon-greedy strategy
        if random.random() > epsilon:
            action = Q.index(max(Q))  # Exploit
        else:
            action = random.choice(bandit.actions())  # Explore

        # Get reward and update statistics
        reward = bandit.reward2(action)
        total_rewards.append(reward)
        counts[action] += 1
        Q[action] += (reward - Q[action]) / counts[action]
        avg_rewards.append(avg_rewards[-1] + (reward - avg_rewards[-1]) / t)

    return Q, avg_rewards, total_rewards


# Run the simulation
random.seed(43)
bandit = BinaryBandit()
Q_values, avg_rewards, rewards = eGreedy_binary(bandit, 0.2, 2000)

# Plotting the results
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

ax1.plot(avg_rewards)
ax1.set_title("Average Rewards vs Iterations")
ax1.set_xlabel("Iteration")
ax1.set_ylabel("Average Reward")

ax2.plot(rewards)
ax2.set_title("Reward per Iteration")
ax2.set_xlabel("Iteration")
ax2.set_ylabel("Reward")

plt.show()
