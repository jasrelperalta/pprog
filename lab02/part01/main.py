import numpy as np
import random
import datetime
import threading

# prettier printing options
np.set_printoptions(linewidth=1000, formatter={'float': '{: 0.0f}'.format})

# for given example in exer file
# mat[0][0] = 200
# mat[0][10] = 250
# mat[10][0] = 280
# mat[10][10] = 300

# interpolate function
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

# modified interpolation function
# to run concurrently with other threads
# from other x1 to x2's
def terrain_inter_threaded(mat,x1,x2):
    for i in range(0,n):
        for j in range(x1,x2+2):
            if mat[i][j] != 0:
                continue
            if (i % dist == 0):
                get_row_val(i,j)
    for i in range(0,n):
        for j in range(x1,x2+2):
            if (mat[i][j] == 0):
                get_col_val(i,j)

def get_submatrices(n,t):
    # array of submatrices
    sub_arr = []
    temp = []
    for i in range(0,n):
        temp.append(i)
        if (len(temp) == (n-1) / t):
            sub_arr.append(temp)
            temp = []

    return sub_arr

# get size of matrix
def getSize():
    n = 1
    while (n % 10 != 0):
        n = int(input("enter size of matrix: "))
        if n % 10 != 0:
            print('invalid size of matrix')
    return n+1

# get number of threads
def getThreads(n):
    n -= 1
    t = 0
    # n size should be less than t threads
    # t threads should not be 0
    # n size should be divisible by t threads
    while (n < t) or (t == 0) or (n % t != 0):
        t = int(input('enter number of threads: '))
        if (n < t) or (n % t != 0):
            print('invalid number of threads')
    return t

# dp array format:
# dp = [[x1,y1][x2,y2]]

# interpolate rows with random values
def get_row_val(i,j):
    dp = get_datapoints_row(i,j)
    x = j               # j -> row
    x1 = dp[0][0]
    x2 = dp[1][0]
    y1 = dp[0][1]
    y2 = dp[1][1]
    res = fcc(x1,y1,x2,y2,x)
    mat[i][j] = res

# interpolate columns
def get_col_val(i,j):
    dp = get_datapoints_col(i,j)
    # dp = [[x1,y1][x2,y2]]
    x = i               # i -> col
    x1 = dp[0][0]
    x2 = dp[1][0]
    y1 = dp[0][1]
    y2 = dp[1][1]
    res = fcc(x1,y1,x2,y2,x)
    mat[i][j] = res


# get closest datapoints to the current gridpoint
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
## improved from recursion from previous exercise to direct computation
def get_nearest_row(i,j,dir):
    # go up
    if dir < 0:
        dir = j - (j % 10)
    # go down
    else:
        dir = j + (10 - (j % 10))
    return [dir,mat[i][dir]]

def get_nearest_col(i,j,dir):
    # go left
    if dir < 0:
        dir = i - (i % 10)
    # go right
    else:
        dir = i + (10 - (i % 10))
    return [dir,mat[dir][j]]

# follow given FCC formula
def fcc(x1,y1,x2,y2,x):
    return (y1 + (((x-x1)/(x2-x1)) * (y2-y1)))

# main function
if __name__ == "__main__":
    # initialize data
    n = getSize()
    t = getThreads(n)

    # distance between randomized values
    dist = 10

    # # create a zero nxn matrix
    # mat = np.zeros((n,n), dtype = float)

    # # randomize elevation values for gridpoints divisible by 10
    # for i in range(n):
    #     for j in range(n):
    #         if i % dist == 0 and j % dist == 0:
    #             mat[i][j] = random.uniform(0.0, 1000.0)

    # # print initial matrix
    # print(mat)

    # # record time before serial interpolation
    # time_before_serial = datetime.datetime.now()

    # # interpolate matrix
    # terrain_inter(mat)

    # # record time after serial interpolation
    # time_after_serial = datetime.datetime.now()


    # # print resulting matrix
    # print(mat)

    # print("\n\n\n")


    # create a zero nxn matrix
    mat = np.zeros((n,n), dtype = float)

    # randomize elevation values for gridpoints divisible by 10
    for i in range(n):
        for j in range(n):
            if i % dist == 0 and j % dist == 0:
                mat[i][j] = random.uniform(0.0, 1000.0)

    # print initial matrix
    print(mat)

    threads = list()

    for set in get_submatrices(n,t):
        x1, x2 = set[0], set[-1]
        thread = threading.Thread(target=terrain_inter_threaded, args=(mat,x1,x2))
        threads.append(thread)

    # record time before threaded interpolation
    time_before_parallel = datetime.datetime.now()


    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    # record time after threaded interpolation
    time_after_parallel = datetime.datetime.now()


    # print resulting matrix
    print(mat)

    # print interpolation time
    # print("serial: ",time_after_serial-time_before_serial)
    print("parallel: ",time_after_parallel-time_before_parallel)