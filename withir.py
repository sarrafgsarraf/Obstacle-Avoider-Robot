import RPi.GPGPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(2,GPIO.IN) #GPGPIO 2 -> Left IR out
GPIO.setup(3,GPIO.IN) #GPGPIO 3 -> Right IR out

GPIO.setup(16,GPIO.OUT) #GPGPIO 4 -> Motor 1 terminal A
GPIO.setup(12,GPIO.OUT) #GPGPIO 14 -> Motor 1 terminal B

GPIO.setup(21,GPIO.OUT) #GPGPIO 17 -> Motor Left terminal A
GPIO.setup(20,GPIO.OUT) #GPGPIO 18 -> Motor Left terminal B

while 1:
    if(GPIO.input(2)==True and GPIO.input(3)==True): #both while move forward     
        GPIO.output(16,True) #1A+
        GPIO.output(12,False) #1B-

        GPIO.output(21,True) #2A+
        GPIO.output(20,False) #2B-

    elif(GPIO.input(2)==False and GPIO.input(3)==True): #turn right  
        GPIO.output(16,True) #1A+
        GPIO.output(12,True) #1B-

        GPIO.output(21,True) #2A+
        GPIO.output(20,False) #2B-

    elif(GPIO.input(2)==True and GPIO.input(3)==False): #turn left
        GPIO.output(16,True) #1A+
        GPIO.output(12,False) #1B-

        GPIO.output(21,True) #2A+
        GPIO.output(20,True) #2B-

    else:  #stay still
        GPIO.output(16,True) #1A+
        GPIO.output(12,True) #1B-

        GPIO.output(21,True) #2A+
        GPIO.output(20,True) #2B-
