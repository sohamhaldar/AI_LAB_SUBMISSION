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


def eGreedy_modified(bandit, epsilon, max_iterations, alpha):
    # Initialization
    Q = [0] * bandit.N
    counts = [0] * bandit.N
    rewards_per_iter = []
    avg_rewards = [0]
    mse = 0  # Initialize MSE

    # Incremental Implementation
    for t in range(1, max_iterations):
        # Epsilon-greedy action selection
        if random.random() > epsilon:
            action = Q.index(max(Q))  # Exploit
        else:
            action = random.choice(bandit.actions())  # Explore
        
        # Get reward and update statistics
        reward = bandit.reward(action)
        rewards_per_iter.append(reward)
        counts[action] += 1
        Q[action] += alpha * (reward - Q[action])  # Update action-value estimate
        avg_rewards.append(avg_rewards[-1] + (reward - avg_rewards[-1]) / t)

        # Calculate MSE
        mse = sum((bandit.expRewards[i] - Q[i]) ** 2 for i in range(bandit.N)) / bandit.N

    return Q, avg_rewards, rewards_per_iter, mse


# Run the simulation
random.seed(43)
bandit = Bandit(N=10)
Q, avg_rewards, rewards, mse = eGreedy_modified(bandit, 0.4, 10000, 0.01)

# Print comparison between actual and recovered rewards
print("Actual\tRecovered")
for actual, recovered in zip(bandit.expRewards, Q):
    print(f"{actual:.3f} \t {recovered:.3f}")

# Calculate mean squared error (MSE) again for clarity
mse_calculated = sum((actual - recovered) ** 2 for actual, recovered in zip(bandit.expRewards, Q)) / bandit.N
print("MSE for Modified Epsilon Greedy: ", mse_calculated)

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

fig.suptitle("Modified Epsilon Greedy Policy")
plt.show()
