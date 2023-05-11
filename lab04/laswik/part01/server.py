import main as inter
import pickle


# first of all import the socket library
import socket            
 
# next create a socket object
s = socket.socket()        
print ("Socket successfully created")
 
# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345               
 
# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('127.0.0.1', port))        
print ("socket binded to %s" %(port))
 
# put the socket into listening mode
s.listen(5)    
print ("socket is listening")           



# initialize data
n = inter.getSize()
t = inter.getSubmatrices(n)
x = inter.get_submatrices(n,t)

# distance between randomized values
dist = 10

# create nxn matrix  
mat = inter.createMatrix(n, dist)

# wait until all submatrices are distributed
counter = 0

while counter!=t:
 
# Establish connection with client.
  c, addr = s.accept()    
  print ('Got connection from', addr )
 

  data = [mat, n, t, x, dist]
  data = pickle.dumps(data)
  c.send(data)

  counter += 1

c.close()