import numpy as np
import random
import datetime
import help
import socket
import threading
import queue

# global counter of received acknowledgements
COUNTER_ACK = 0

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

# send and receive data from slave for each thread
def sendReceiveData(conn, mat, start, end, queue):
    # send data to slave
    mat = matToString(mat)
    help.send_msg(conn, mat)

    # send start and end indices to slave
    indices = [start, end]
    indices = np.array(indices)
    indices = indices.tobytes()
    help.send_msg(conn, indices)

    if conn.recv(1024) == b'ack':
        global COUNTER_ACK
        COUNTER_ACK += 1
        print('acknowledgement received from', conn.getpeername())


    # receive data from slave
    data = help.recv_msg(conn)
    data = stringToMat(data)

    # update matrix
    mat = data

    # close connection
    conn.close()

    # return updated matrix
    queue.put(mat)

# divide matrix into t parts to be sent to t threads
def divideMatrix(mat, t):
    # get size of matrix
    n = mat.shape[0]

    # get number of rows per thread
    rows = n // t

    # get start and end indices for each thread
    # if n is divisible by t
    if n % t == 0:
        start = 0
        end = rows
        indices = []
        for i in range(t):
            indices.append([start, end])
            start = end
            end += rows
    else:
        start = 0
        end = rows + (n % t)
        indices = []
        for i in range(t):
            indices.append([start, end])
            start = end
            end += rows

    # return indices
    return indices

# update matrix with data from slave
def updateMatrix(mat, data):
    # update matrix
    for i in range(n):
        for j in range(n):
            if mat[i][j] == 0:
                mat[i][j] = data[i][j]

    # return updated matrix
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
        

        # counter for number of slaves connected
        counter = 0
        with s:
            # bind socket to ip address and port
            s.bind((ip_address, port))
            print('server started on port', port)
            
            # start listening
            s.listen(num_slaves)
            print('server started listening on port', port)
            
            # list of threads
            threads = []

            # divide matrix into t parts
            indices = divideMatrix(mat, num_slaves)
            
            # create queue to store results
            q = queue.Queue()
            counter_again = 0

            while True and (COUNTER_ACK != num_slaves):
                # accept connections
                conn, addr = s.accept()
                print('connected to', addr)

                #start timer
                if counter_again == 0:
                    print('start timer')
                    start = datetime.datetime.now()
                    counter_again = 1

                # create thread
                thread = threading.Thread(target = sendReceiveData, args = (conn, mat, indices[counter-1][0], indices[counter-1][1], q))
                threads.append(thread)
                thread.start()
                print("thread", counter, "started running")
                counter += 1
                
                if counter == num_slaves:
                    break
            
            # keep looping until all acknowledges are received
            while COUNTER_ACK != num_slaves:
                continue

            # stop timer since all slaves are connected
            end = datetime.datetime.now()
            print('time elapsed during distributing:', end-start)
            
            # wait for all threads to finish then update matrix
            print('waiting for threads to finish...')
            for thread in threads:
                thread.join()
                mat = updateMatrix(mat, q.get())
                      

        # print matrix
        print(mat)

        # stop server
        s.close()

        # stop another timer
        end = datetime.datetime.now()
        print('time elapsed w/ interpolation:', end-start)

        # print message
        print('server stopped listening on port', port)
        print('server closed')
         




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


        
        # receive matrix from master
        mat = help.recv_msg(s)
        mat = stringToMat(mat)



        # get start and end indices for slave
        indices = help.recv_msg(s)
        indices = np.frombuffer(indices, int)
        indices = np.reshape(indices, (2,1))
        start = int(indices[0])
        end = int(indices[1])

        # send acknowledgement to master
        s.sendall(b'ack')


        # interpolate matrix
        print("interpolating from ", start, " to ", end)
        terrain_inter(mat, start, end)
        print(mat)

        # send matrix back to master
        mat = matToString(mat)
        help.send_msg(s, mat)
        s.close()

