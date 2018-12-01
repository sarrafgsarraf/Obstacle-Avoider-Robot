import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)                    # programming the GPIO by BCM pin numbers

TRIG = 22
ECHO = 5
buzz = 19
m11=16
m12=12
m21=21
m22=20
IR1=2
IR2=3

GPIO.setup(TRIG,GPIO.OUT)                  # initialize GPIO Pin as outputs
GPIO.setup(ECHO,GPIO.IN)                   # initialize GPIO Pin as input
GPIO.setup(buzz,GPIO.OUT)                  
GPIO.setup(m11,GPIO.OUT)
GPIO.setup(m12,GPIO.OUT)
GPIO.setup(m21,GPIO.OUT)
GPIO.setup(m22,GPIO.OUT)
GPIO.setup(IR1,GPIO.IN)                     #GPIO 2 -> Left IR out
GPIO.setup(IR2,GPIO.IN)                     #GPIO 2 -> Left IR out

time.sleep(5)

def stop():
    print "OBSTACLE AHEAD, CLEAR PATH TO RESUME SERVICE!"
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)

def forward():
    GPIO.output(m11, 1)
    GPIO.output(m12, 0)
    GPIO.output(m21, 1)
    GPIO.output(m22, 0)
    print "CLEAR."

def left():
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 1)
    GPIO.output(m22, 0)
    print "TURNING LEFT.."

def right():
    GPIO.output(m11, 1)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)
    print "TURNING RIGHT.."

def buzzer():  
    GPIO.output(buzz, 1)
    time.sleep(0.5)
    GPIO.output(buzz, 0)
    
def stay():
    print "REACHED DESTINATION!"
    GPIO.output(m11, 1)
    GPIO.output(m12, 1)
    GPIO.output(m21, 1)
    GPIO.output(m22, 1)


def averageD():
    i=0
    avgDistance=0
    for i in range(5):
        GPIO.output(TRIG, False)                 #Set TRIG as LOW
        time.sleep(0.1)                                   #Delay
        GPIO.output(TRIG, True)                  #Set TRIG as HIGH
        time.sleep(0.00001)                       #Delay of 0.00001 seconds
        GPIO.output(TRIG, False)                 #Set TRIG as LOW
        while GPIO.input(ECHO)==0:            #Check whether the ECHO is LOW
            GPIO.output(buzz, False)             
        pulse_start = time.time()
        while GPIO.input(ECHO)==1:          #Check whether the ECHO is HIGH
            GPIO.output(buzz, False)
        pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start #time to get back the pulse to sensor
        distance = pulse_duration * 17150        #Multiply pulse duration by 17150 (34300/2) to get distance
        distance = round(distance,2)            #Round to two decimal points
        avgDistance=avgDistance+distance
        
    avgDistance=avgDistance/5
    return avgDistance

stop()
count=0

try:
    
    while True:
                avd = averageD()
                flag=0
                
                if(GPIO.input(2)==True and GPIO.input(3)==True and avd>20): #both while move forward     
                    forward()
                    print avd
                elif(GPIO.input(2)==False and GPIO.input(3)==True and avd>20): #turn right  
                    right()
                    print avd
                elif(GPIO.input(2)==True and GPIO.input(3)==False and avd>20): #turn left
                    left()
                    print avd
                elif avd < 20:      #Check whether the distance is within 20 cm range
                    count=count+1
                    stop()
                    buzzer()
                    time.sleep(0.5)
                else:  #stay still
                    stay()
                    
except KeyboardInterrupt:
    GPIO.cleanup()
    exit
