n = 3
arr = [[0 for x in range(n)] for y in range(n)]
arr[2][1] = 3  # wraps around once for negative

print("length", len(arr))
print(arr[1][0])
print(arr)