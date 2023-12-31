import UdpComms as U
import time
import modi

# define range constant 
# Different beween sensor
rcls = [1,36,1]
rmid = [56,57,57]
rfar = [83,83,86]
ccls = [1,0,1]
cmid = [65,65,57]
cfar = [85,85,79]

# modi sensor init
bundle = modi.MODI()
network = bundle.networks[0]
ul0 = bundle.ultrasonics[0] 
ul1 = bundle.ultrasonics[1] 
ul2 = bundle.ultrasonics[2] 
ul3 = bundle.ultrasonics[3] 
ul4 = bundle.ultrasonics[4] 

def figuration(detection, sen_num):
    input("Hide "+ sen_num +" sensor and enter any key to continue:")  

    for pos in range(5):
        if detection[pos].distance == 0:
            print("Correctly hidden!")
            break
        else:
            print("Not hidden")
    return pos

for s in [ul0,ul1,ul2,ul3,ul4]:
    print(s.distance)
time.sleep(0.5)
for s in [ul0,ul1,ul2,ul3,ul4]:
    print(s.distance)

# Sensor ordering
detection = [ul0,ul1,ul2,ul3,ul4]
position  = [None,None,None,None,None] #r1,r2,r3,c1,c3 sensor

print("Detection list:",detection)

# Sensor catching in a order of r3-c3-r2-r1-c1 
position[2] = detection[figuration(detection, "r3")]
position[4] = detection[figuration(detection, "c3")]
position[1] = detection[figuration(detection, "r2")]
position[0] = detection[figuration(detection, "r1")]
for i in [0,1,2,4]:
    detection.remove(position[i])
position[3] = detection[0]

print("position list:", position)

for i in range(10):
    print("Check "+str(i+1)+"/5")
    print("r1: ", position[0].distance)
    print("r2: ", position[1].distance)
    print("r3: ", position[2].distance)
    print("c1: ", position[3].distance)
    print("c3: ", position[4].distance)
    input("Enter any key to continue: ")



# Create UDP socket to use for sending
sock = U.UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True)

while True:
    time.sleep(0.1) # minimum detection time

    # get sensor value
    row = [position[0].distance,position[1].distance,position[2].distance]
    col = [position[3].distance,200,position[4].distance] # middle one is not used

    # set 1 / 2 / 3 if stepped for each row and column
    for i in range(3):
        row[i] = 1 if row[i]<rcls[i] else (2 if row[i]<rmid[i] else (3 if row[i]<rfar[i] else 0))
        col[i] = 1 if col[i]<ccls[i] else (2 if col[i]<cmid[i] else (3 if col[i]<cfar[i] else 0))

    # value init - Unpressed : 0 / Pressed : 1
    step = [0,0,0,0,0,0,0,0,0] # Each position denote number

    # detection result update
    for i in range(3):
        if row[i] != 0:
            for j in range(3):
                if col[j] == i+1:
                    if (3*i+j) %2 == 0: 
                        step[3*i+j] = 1
                if i == 1 and row[i] == 2:
                    step[4] = 1

    txt = ""
    for i in range(5):
        txt = txt + str(step[2*i])

    print("Current step info:",txt)
    
    sock.SendData(txt) # Send this string to other application

    # data = sock.ReadReceivedData() # read data

    # if data != None: # if NEW data has been received since last ReadReceivedData function call
    #     print(data) # print new received data
