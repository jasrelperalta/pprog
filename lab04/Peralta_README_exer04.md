# CMSC 180 - Parallel Programming

### Distributing parts of a Matrix over Sockets

Use t number of slaves to interpolate n / t x n submatrices through an open socket. Compare and analyze the running times when running on a single machine and different machines. 

## Running Instructions

Install numpy module (if not yet installed):
``` bash
$ pip install numpy 
```

Run python program:
``` bash
$ python3 main.py 
```
Input n size of nxn table:
```bash
$ 1000
```
Input instance type [0] = master, [1] = slave:
```bash
$ 0
```

:cry:
