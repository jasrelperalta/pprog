import numpy as np
import random
import datetime
import help
import socket

# TODO: use threads to connect to multiple slaves
# use this https://stackoverflow.com/questions/10810249/python-socket-multiple-clients

# TODO: fix animation during interpolation

# TODO: divide matrix into t parts


# prettier printing options
np.set_printoptions(linewidth=1000, formatter={'float': '{: 0.0f}'.format})

# get size of nxn matrix
def getSize():
    n = 1
    while (n % 10 != 0):
        n = int(input("enter size of matrix: "))
        if n % 10 != 0:
            print('invalid size of matrix')
    return n+1

# get port number
def getPort():
    p = 0
    while (p < 5000) or (p > 65535):
        p = int(input('enter port number: '))
        if (p < 5000) or (p > 65535):
            print('invalid port number')
    return p

# get status of the instance
# 0 = master
# 1 = slave
def getInstance():
    s = 2
    while (s != 0) and (s != 1):
        s = int(input('enter status of instance: '))
        if (s != 0) and (s != 1):
            print('invalid status of instance')
    return s


# interpolate function
def terrain_inter(mat,x1,x2):
    for i in range(0,n):
        for j in range(x1,x2):
            if mat[i][j] != 0:
                continue
            if (i % dist == 0):
                get_row_val(i,j)
    for i in range(0,n):
        for j in range(x1,x2):
            if (mat[i][j] == 0):
                get_col_val(i,j)

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


def createMatrix(n, dist):
    # create a zero nxn matrix
    mat = np.zeros((n,n), dtype = float)

    # randomize elevation values for gridpoints divisible by 10
    for i in range(n):
        for j in range(n):
            if i % dist == 0 and j % dist == 0:
                mat[i][j] = random.uniform(0.0, 1000.0)
        
    return mat


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

# convert matrix to string
def matToString(mat):
    mat = mat.tobytes()
    return mat

# convert string to matrix
def stringToMat(data):
    mat = np.frombuffer(data)
    mat = np.reshape(mat, (n,n))
    return mat

# create copy of matrix
def copyMat(mat):
    mat = np.copy(mat)
    return mat

# main function
if __name__ == "__main__":
    # initialize data
    n = getSize()
    s = getInstance()

    # initialize distance between gridpoints
    dist = 10

    # master instance
    if s == 0:
        # create matrix
        mat = createMatrix(n, dist)

        # print matrix
        print(mat)

        # read config file
        f = open('config.in', 'r')
        lines = f.readlines()
        f.close()

        # get number of slaves, ip address, and port number
        num_slaves = int(lines[0])
        ip_address = lines[1].strip('\n')
        port = int(lines[2])

        # start server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((ip_address, port))
        print('server started on port', port)
        s.listen(num_slaves)
        print('server started listening on port', port)
        
        # start timer
        start = datetime.datetime.now()

        # accept connections until all slaves are connected
        for i in range(num_slaves):
            conn, addr = s.accept()
            print('connected to', addr, i+1, 'out of', num_slaves)
            mat = matToString(mat)
            # conn.send(mat)
            help.send_msg(conn, mat)
            print('matrix sent to', addr)
            # receive matrix
            # mat = conn.recv(8192)
            mat = help.recv_msg(conn)
            mat = stringToMat(mat)
            print(mat)
            print('matrix received from', addr)
            
            # close connection
            conn.close()   

        # print matrix
        print(mat)

        # stop server
        s.close()
        print('server stopped listening on port', port)
        print('server closed')
         


        # stop timer
        end = datetime.datetime.now()
        print('time elapsed:', end-start)


    # slave instance
    else:
        # read config file
        f = open('config.in', 'r')
        lines = f.readlines()
        f.close()

        # get number of slaves, ip address, and port number
        num_slaves = int(lines[0])-1
        ip_address = lines[1].strip('\n')
        port = int(lines[2])

        # connect to master
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip_address, port))

        # receive matrix
        # mat = s.recv(8192)
        mat = help.recv_msg(s)
        mat = stringToMat(mat)

        # interpolate matrix
        mat = mat.copy()
        terrain_inter(mat,0,n)
        # help.start(terrain_inter, mat, 0, n)

        # send matrix back to master
        mat = matToString(mat)
        # s.send(mat)
        help.send_msg(s, mat)
        s.close()


