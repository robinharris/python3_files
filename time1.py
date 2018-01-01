import timeit
clock = timeit.default_timer

print("Enter your name: ", end="")
start_time = clock()
name = input()
elapsed = clock() - start_time
print(name, " it took you ", elapsed, " seconds to respond")