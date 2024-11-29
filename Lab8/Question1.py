class GridWorld:
    def __init__(self, rows=3, cols=4, walls=None, terminal_states=None):
        self.rows = rows
        self.cols = cols
        self.walls = walls if walls else [(1, 1)]
        self.terminal_states = terminal_states if terminal_states else [(1, 3), (2, 3)]
        self.environment_left = {'L': 'D', 'R': 'U', 'U': 'L', 'D': 'R'}
        self.environment_right = {'L': 'U', 'R': 'D', 'U': 'R', 'D': 'L'}
    
    def is_valid(self, i, j):
        return (i, j) not in self.walls and 0 <= i < self.rows and 0 <= j < self.cols
    
    def transition(self, action, i, j):
        if action == 'L':
            return (i, j - 1)
        elif action == 'R':
            return (i, j + 1)
        elif action == 'U':
            return (i + 1, j)
        elif action == 'D':
            return (i - 1, j)
        else:
            return (-1, -1)


class PolicyEvaluator:
    def __init__(self, grid_world, discount_factor=1.0):
        self.grid_world = grid_world
        self.discount_factor = discount_factor

    def initialize_value_matrix(self):
        return [[0 for _ in range(self.grid_world.cols)] for _ in range(self.grid_world.rows)]

    def update_reward_matrix(self, reward):
        reward_matrix = [[reward for _ in range(self.grid_world.cols)] for _ in range(self.grid_world.rows)]
        reward_matrix[2][3] = 1
        reward_matrix[1][3] = -1
        return reward_matrix

    def value_function(self, i, j, reward_matrix, V_pie):
        value = 0
        actions = ['L', 'R', 'U', 'D']
        for action in actions:
            # Desired action
            state_x, state_y = self.grid_world.transition(action, i, j)
            desired_value = (reward_matrix[state_x][state_y] + self.discount_factor * V_pie[state_x][state_y]) \
                if self.grid_world.is_valid(state_x, state_y) else \
                (reward_matrix[i][j] + self.discount_factor * V_pie[i][j])

            # Environment left
            state_x, state_y = self.grid_world.transition(self.grid_world.environment_left[action], i, j)
            left_value = (reward_matrix[state_x][state_y] + self.discount_factor * V_pie[state_x][state_y]) \
                if self.grid_world.is_valid(state_x, state_y) else \
                (reward_matrix[i][j] + self.discount_factor * V_pie[i][j])

            # Environment right
            state_x, state_y = self.grid_world.transition(self.grid_world.environment_right[action], i, j)
            right_value = (reward_matrix[state_x][state_y] + self.discount_factor * V_pie[state_x][state_y]) \
                if self.grid_world.is_valid(state_x, state_y) else \
                (reward_matrix[i][j] + self.discount_factor * V_pie[i][j])

            # Combine action values
            value_to_action = 0.8 * desired_value + 0.1 * left_value + 0.1 * right_value
            value += value_to_action * 0.25  # Equal probability for each action
        return value

    def iterative_policy_evaluation(self, reward, epsilon=1e-8):
        reward_matrix = self.update_reward_matrix(reward)
        V_pie = self.initialize_value_matrix()
        iterations = 0

        while True:
            delta = 0
            for i in range(self.grid_world.rows):
                for j in range(self.grid_world.cols):
                    state = (i, j)
                    if state in self.grid_world.terminal_states or state in self.grid_world.walls:
                        continue
                    v = V_pie[i][j]
                    V_pie[i][j] = self.value_function(i, j, reward_matrix, V_pie)
                    delta = max(delta, abs(v - V_pie[i][j]))
            iterations += 1
            if delta < epsilon:
                print(f"Converged in {iterations} iterations for r(S) = {reward}")
                break
        self.print_values(V_pie)

    def print_values(self, V):
        for i in range(self.grid_world.rows - 1, -1, -1):
            print(" ")
            for j in range(self.grid_world.cols):
                print(f" {V[i][j]:.2f}|", end="")
            print("")


if __name__ == "__main__":
    # Create the GridWorld environment
    grid_world = GridWorld()

    # Create the Policy Evaluator
    policy_evaluator = PolicyEvaluator(grid_world)

    # Test with multiple rewards
    rewards = [-0.04, -2, 0.1, 0.02, 1]
    print("Value Functions corresponding to optimal policy\n")
    for reward in rewards:
        print(f"For r(S) = {reward}")
        policy_evaluator.iterative_policy_evaluation(reward)
        print("\n")
