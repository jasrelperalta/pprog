import numpy as np
import random

np.set_printoptions(formatter={'float': '{: 0.5f}'.format})

n = int(input("enter size: "))
n += 1
dist = 10

mat = np.zeros((n,n), dtype = float)

# testing stuff
# TODO: use area weighted and change conditions after testing stuff
for i in range(n):
    for j in range(n):
        if i % dist == 0 and j % dist == 0:
            mat[i][j] = random.uniform(0.0, 1000.0)

# for given example at exer file
# mat[0][0] = 200
# mat[0][10] = 250
# mat[10][0] = 280
# mat[10][10] = 300



# matrix [row][col]

def terrain_inter(mat):
    for i in range(0,n):
        for j in range(0,n):
            if mat[i][j] != 0:
                continue
            if (i % dist == 0):
                get_row_val(i,j)
    for i in range(0,n):
        for j in range(0,n):
            if (mat[i][j] == 0):
                get_col_val(i,j)
    print("\n")

# interpolate rows with random values
def get_row_val(i,j):
    dp = get_datapoints_row(i,j)
    x1 = dp[0][0]
    x2 = dp[1][0]
    x = j
    y1 = dp[0][1]
    y2 = dp[1][1]
    res = fcc(x1,y1,x2,y2,x)
    mat[i][j] = res


# interpolate cols
def get_col_val(i,j):
    dp = get_datapoints_col(i,j)
    x1 = dp[0][0]
    x2 = dp[1][0]
    x = i
    y1 = dp[0][1]
    y2 = dp[1][1]
    res = fcc(x1,y1,x2,y2,x)
    mat[i][j] = res


# top to bottom; left to right
def get_datapoints_row(i,j):
    dp = []
    dp.append(get_nearest_row(i,j,-1))
    dp.append(get_nearest_row(i,j,+1))
    return dp

def get_datapoints_col(i,j):
    dp = []
    dp.append(get_nearest_col(i,j,-1))
    dp.append(get_nearest_col(i,j,+1))
    return dp

# x, y -> point; dir -> direction 
# change direction to check to the nearest 10
def get_nearest_row(i,j,dir):
    if mat[i][j+dir] != 0:
        return [j+dir,mat[i][j+dir]]
    return get_nearest_row(i,j+dir,dir)

def get_nearest_col(i,j,dir):
    if mat[i+dir][j] != 0:
        return [i+dir,mat[i+dir][j]]
    return get_nearest_col(i+dir,j,dir)


def fcc(x1,y1,x2,y2,x):
    return (y1 + (((x-x1)/(x2-x1)) * (y2-y1)))

print(mat)
terrain_inter(mat)
print(mat)