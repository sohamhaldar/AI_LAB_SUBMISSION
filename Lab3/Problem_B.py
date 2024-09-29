import random

def generate_clause(k, n):
    # Generate a random clause of length k
    clause = []
    while len(clause) < k:
        variable = random.randint(1, n)
        # Randomly decide whether to negate the variable
        if random.choice([True, False]):
            variable = -variable
        if variable not in clause:
            clause.append(variable)
    return clause

def generate_k_sat(k, m, n):
    # Generate m clauses of length k
    sat_problem = []
    for _ in range(m):
        clause = generate_clause(k, n)
        sat_problem.append(clause)
    return sat_problem

def main():
    k = int(input("Enter the value of k: "))
    m = int(input("Enter the number of clauses (m): "))
    n = int(input("Enter the number of variables (n): "))
    
    k_sat_problem = generate_k_sat(k, m, n)
    print("Generated k-SAT problem:")
    for clause in k_sat_problem:
        print(clause)

if __name__ == "__main__":
    main()
