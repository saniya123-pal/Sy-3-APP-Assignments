# 0/1 Knapsack - Dynamic Programming

def knapsack_memo(weights, values, n, capacity, memo):

    if n == 0 or capacity == 0:
        return 0

    if memo[n][capacity] != -1:
        return memo[n][capacity]

    if weights[n - 1] <= capacity:

        take = values[n - 1] + knapsack_memo(
            weights, values, n - 1,
            capacity - weights[n - 1], memo
        )

        not_take = knapsack_memo(
            weights, values, n - 1,
            capacity, memo
        )

        memo[n][capacity] = max(take, not_take)

    else:
        memo[n][capacity] = knapsack_memo(
            weights, values, n - 1,
            capacity, memo
        )

    return memo[n][capacity]


def knapsack_tabulation(weights, values, capacity):

    n = len(weights)

    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):

        for w in range(1, capacity + 1):

            if weights[i - 1] <= w:

                take = values[i - 1] + dp[i - 1][w - weights[i - 1]]
                not_take = dp[i - 1][w]

                dp[i][w] = max(take, not_take)

            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity]


# ---------- INPUT ----------

n = int(input("Enter number of items: "))

weights = []
values = []

for i in range(n):
    w = int(input(f"Enter weight of item {i + 1}: "))
    v = int(input(f"Enter value of item {i + 1}: "))

    weights.append(w)
    values.append(v)

capacity = int(input("Enter knapsack capacity: "))


# ---------- MEMOIZATION ----------

memo = [[-1] * (capacity + 1) for _ in range(n + 1)]

result_memo = knapsack_memo(
    weights, values, n, capacity, memo
)


# ---------- TABULATION ----------

result_tab = knapsack_tabulation(
    weights, values, capacity
)


# ---------- OUTPUT ----------

print("\nUsing Memoization:", result_memo)
print("Using Tabulation:", result_tab)