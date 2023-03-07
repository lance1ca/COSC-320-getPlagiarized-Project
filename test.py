import time
import matplotlib.pyplot as plt

def double_for_loop(n):
    start_time = time.perf_counter()
    for i in range(n):
        for j in range(n):
            # Your double for loop code goes here
            pass
    end_time = time.perf_counter()
    return end_time - start_time

# Test the function for different values of n
n_values = [10, 20, 30, 40, 50]
runtimes = []
for n in n_values:
    runtime = double_for_loop(n)
    runtimes.append(runtime)

# Plot the results
plt.plot(n_values, runtimes, 'bo-')
plt.xlabel('n')
plt.ylabel('Runtime (seconds)')
plt.title('Runtime of double_for_loop')
plt.show()
