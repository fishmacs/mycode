
## Frog Jumping Path Problem
# A frog is jumping in the coordinate plane according to the following rules: From
# any lattice point (a, b), the frog can jump to (a+1, b), (a, b+1), or (a+1, b+1).
# There are no right angle turns in the frog's path. How many different paths can the
# frog take from (0, 0) to (n, n)? [ n=1, 2, 3, ...]

import numpy as np

def countPaths (i, j):
    L = np.zeros((20, 20))
    M = np.zeros((20, 20))
    D = np.zeros((20, 20))
    
    S = np.zeros((20, 20))
    
    if i == 0 and j == 0:
         L[i][j] = 0
         M[i][j] = 1
         D[i][j] = 0
         S[i][j] = L[i][j] + M[i][j] + D[i][j]
   
    elif i == 0 and j == 1:
         L[i][j] = 0
         M[i][j] = 0
         D[i][j] = 1
         S[i][j] = L[i][j] + M[i][j] + D[i][j]

    elif i == 1 and j == 0:
         L[i][j] = 1
         M[i][j] = 0
         D[i][j] = 0
         S[i][j] = L[i][j] + M[i][j] + D[i][j]
         
    else:
         L[i][j] = countPaths(i-1, j) - D[i-1][j]
         M[i][j] = countPaths(i-1, j-1)
         D[i][j] = countPaths(i, j-1) - L[i][j-1]
         S[i][j] = L[i][j] + M[i][j] + D[i][j]

    return S[i][j]

def main():

    for n in range(1, 11):
         print('The total number of paths to reach point (%d, %d) is ' % (n, n), int(countPaths(n, n)))

if __name__ == "__main__":
    main()

