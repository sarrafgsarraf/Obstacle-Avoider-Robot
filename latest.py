import RPi.GPIO as GPIO                       #Import GPIO library
import time                             #Import time library

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)                    # programming the GPIO by BCM pin numbers

TRIG1 = 17
TRIG2 = 22
TRIG3 = 6

ECHO1 = 27
ECHO2 = 5
ECHO3 = 13

buzz = 19

m11=16
m12=12

m21=21
m22=20

IR1=2
IR2=3


GPIO.setup(IR1,GPIO.IN)                     #GPIO 2 -> Left IR out
GPIO.setup(IR2,GPIO.IN)                     #GPIO 3 -> Right IR out

GPIO.setup(TRIG1,GPIO.OUT)                  # initialize GPIO Pin as outputs
GPIO.setup(TRIG2,GPIO.OUT)
GPIO.setup(TRIG3,GPIO.OUT)

GPIO.setup(ECHO1,GPIO.IN)                    # initialize GPIO Pin as input
GPIO.setup(ECHO2,GPIO.IN)                  
GPIO.setup(ECHO3,GPIO.IN)                   

GPIO.setup(buzz,GPIO.OUT)                  

GPIO.setup(m11,GPIO.OUT)
GPIO.setup(m12,GPIO.OUT)

GPIO.setup(m21,GPIO.OUT)
GPIO.setup(m22,GPIO.OUT)

time.sleep(5)



def stop():

    print "OBSTACLE ADEAD!!!"
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



def back():

    GPIO.output(m11, 0)
    GPIO.output(m12, 1)
    GPIO.output(m21, 0)
    GPIO.output(m22, 1)
    print "REVERSE.."



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

stop()
count=0

try:

    while True:

            i=0
            avgDistance1=0
            avgDistance2=0
            avgDistance3=0
            for i in range(5):
                    GPIO.output(TRIG1, False)                 #Set TRIG1 as LOW
                    time.sleep(0.1)                                   #Delay
                    GPIO.output(TRIG1, True)                  #Set TRIG1 as HIGH
                    time.sleep(0.00001)                       #Delay of 0.00001 seconds
                    GPIO.output(TRIG1, False)                 #Set TRIG1 as LOW

                    while GPIO.input(ECHO1)==0:            #Check whether the ECHO1 is LOW
                            GPIO.output(buzz, False)
                            
                    pulse_start1 = time.time()

                    while GPIO.input(ECHO1)==1:          #Check whether the ECHO1 is HIGH
                            GPIO.output(buzz, False)

                    pulse_end1 = time.time()
                    pulse_duration1 = pulse_end1 - pulse_start1 #time to get back the pulse to sensor
                    distance1 = pulse_duration1 * 17150        #Multiply pulse duration by 17150 (34300/2) to get distance
                    distance1 = round(distance1,2)            #Round to two decimal points
                    avgDistance1=avgDistance1+distance1

                    GPIO.output(TRIG2, False)                 #Set TRIG1 as LOW
                    time.sleep(0.1)                                   #Delay
                    GPIO.output(TRIG2, True)                  #Set TRIG1 as HIGH
                    time.sleep(0.00001)                       #Delay of 0.00001 seconds
                    GPIO.output(TRIG2, False)                 #Set TRIG1 as LOW

                    while GPIO.input(ECHO2)==0:            #Check whether the ECHO1 is LOW
                            GPIO.output(buzz, False)             

                    pulse_start2 = time.time()

                    while GPIO.input(ECHO2)==1:          #Check whether the ECHO1 is HIGH
                            GPIO.output(buzz, False)

                    pulse_end2 = time.time()
                    pulse_duration2 = pulse_end2 - pulse_start2 #time to get back the pulse to sensor
                    distance2 = pulse_duration2 * 17150        #Multiply pulse duration by 17150 (34300/2) to get distance
                    distance2 = round(distance2,2)            #Round to two decimal points
                    avgDistance2=avgDistance2+distance2
                    
		    GPIO.output(TRIG3, False)                 #Set TRIG1 as LOW
                    time.sleep(0.1)                                   #Delay
                    GPIO.output(TRIG3, True)                  #Set TRIG1 as HIGH
                    time.sleep(0.00001)                       #Delay of 0.00001 seconds
                    GPIO.output(TRIG3, False)                 #Set TRIG1 as LO

                    while GPIO.input(ECHO3)==0:            #Check whether the ECHO1 is LOW
                            GPIO.output(buzz, False)             

                    pulse_start3 = time.time()

                    while GPIO.input(ECHO3)==1:          #Check whether the ECHO1 is HIGH
                            GPIO.output(buzz, False)

                    pulse_end3 = time.time()
                    pulse_duration3 = pulse_end3 - pulse_start3 #time to get back the pulse to sensor
                    distance3 = pulse_duration3 * 17150        #Multiply pulse duration by 17150 (34300/2) to get distance
                    distance3 = round(distance3,2)            #Round to two decimal points
                    avgDistance3=avgDistance3+distance3

            avgDistance1=avgDistance1/5
            print 'distance left:', avgDistance1
            flag1=0
      
            avgDistance2=avgDistance2/5
            print 'distance ahead:', avgDistance2
            flag2=0
         
            avgDistance3=avgDistance3/5
            print 'distance right:', avgDistance3
            flag3=0

            if avgDistance2 < 30:      #Check whether the distance is within 30cm range
                    count = count+1
                    stop()
                    buzzer()
                    time.sleep(0.5)
                    back()
                    time.sleep(1.5)

                    if avgDistance1 > avgDistance3 :
                            left()

                    elif avgDistance3 > avgDistance1 :
                            right()
                            
                    else:

                        if (count%3 == 1) & (flag == 0):
                            right()
                            flag1 = 1
                            flag2 = 1
                            flag3 = 1

                        else:
                            left()
                            flag1 = 0
                            flag2 = 0
                            flag3 = 0

                    time.sleep(1.5)
                    stop()
                    time.sleep(0.5)

            else:
                forward()
                flag1 = 0
                flag2 = 0
                flag3 = 0

except KeyboardInterrupt:
    GPIO.cleanup()
    exit


