import numpy as np
import random
import datetime


np.set_printoptions(formatter={'float': '{: 0.5f}'.format})

n = int(input("enter size: "))
n += 1
dist = 10

mat = np.zeros((n,n), dtype = float)

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
                # print(mat[i][j], i, j)
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
    # go up
    if dir < 0:
        dir = j - (j % 10)
    # go down
    else:
        dir = j + (10 - (j % 10))
    # print(i,j,[dir,mat[i][dir]])
    return [dir,mat[i][dir]]


def get_nearest_col(i,j,dir):
    # go left
    if dir < 0:
        dir = i - (i % 10)
    # go right
    else:
        dir = i + (10 - (i % 10))
    # print(i,j,[dir,mat[dir][j]])
    return [dir,mat[dir][j]]


def fcc(x1,y1,x2,y2,x):
    return (y1 + (((x-x1)/(x2-x1)) * (y2-y1)))


print(mat)
time_before = datetime.datetime.now()
terrain_inter(mat)
time_after = datetime.datetime.now()
print(time_after-time_before)
print(mat)