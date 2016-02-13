import sys
import zmq
import msgpack

port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

if len(sys.argv) > 2:
    port1 =  sys.argv[2]
    int(port1)

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print "Collecting updates from weather server..."
socket.connect ("tcp://192.168.1.40:%s" % port)

if len(sys.argv) > 2:
    socket.connect ("tcp://192.168.1.40:%s" % port1)

    # Subscribe to zipcode, default is NYC, 10001
topicfilter = "10001"
socket.setsockopt(zmq.SUBSCRIBE, topicfilter)

# Process 5 updates
total_value = 0
for update_nbr in range (5):
    string = socket.recv()
    topic, messagedata = string.split()
    decoded_data = msgpack.unpackb(messagedata)
    print "Received on topic %s: " %(topic) , decoded_data["ball"]["x_pos"]

    #total_value += int(messagedata)
    #print topic, messagedata

#print "Average messagedata value for topic '%s' was %dF" % (topicfilter, total_value / update_nbr)