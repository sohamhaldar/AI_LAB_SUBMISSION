import random

# --- Bandit ---
class Bandit:
    def __init__(self, N):
        # N = number of arms
        self.N = N
        self.expRewards = [10] * N  # Initial expected rewards for each arm

    def actions(self):
        return list(range(self.N))  # Return available actions as [0, 1, ..., N-1]

    def reward(self, action):
        # Update expected rewards for all arms with some noise
        for i in range(self.N):
            self.expRewards[i] += random.gauss(0, 0.1)
        
        # Add noise to the reward of the chosen action
        return self.expRewards[action] + random.gauss(0, 0.01)


# Epsilon-Greedy algorithm
def eGreedy(bandit, epsilon, max_iterations):
    # Initialize action-value estimates and action counts
    Q = [0] * bandit.N
    counts = [0] * bandit.N
    rewards_per_iter = []
    avg_rewards = [0]

    # Loop through iterations
    for t in range(1, max_iterations):
        # Epsilon-greedy action selection
        if random.random() > epsilon:
            action = Q.index(max(Q))  # Exploit
        else:
            action = random.choice(bandit.actions())  # Explore

        # Get the reward and update statistics
        reward = bandit.reward(action)
        rewards_per_iter.append(reward)
        counts[action] += 1
        Q[action] += (reward - Q[action]) / counts[action]  # Incremental update of Q values
        avg_rewards.append(avg_rewards[-1] + (reward - avg_rewards[-1]) / t)

    return Q, avg_rewards, rewards_per_iter


# Run the simulation
random.seed(10)
bandit = Bandit(10)
Q_values, avg_rewards, rewards = eGreedy(bandit, 0.3, 10000)

# Print comparison between actual and recovered rewards
print("Actual\tRecovered")
for actual, recovered in zip(bandit.expRewards, Q_values):
    print(f"{actual:.3f} \t {recovered:.3f}")

# Calculate mean squared error (MSE)
mse = sum((actual - recovered) ** 2 for actual, recovered in zip(bandit.expRewards, Q_values))
print("MSE for Unmodified Epsilon Greedy: ", mse)

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

fig.suptitle("Unmodified Epsilon Greedy Policy")
plt.show()
