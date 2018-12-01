import time, datetime
import RPi.GPIO as GPIO 
import telepot
from telepot.loop import MessageLoop
now = datetime.datetime.now()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)                    # programming the GPIO by BCM pin numbers
TRIG1 = 17
ECHO1 = 27

TRIG2 = 22
ECHO2 = 5

TRIG3 = 6
ECHO3 = 13

buzz = 19
m11 = 16
m12 = 12
m21 = 21
m22 = 20

GPIO.setup(TRIG1,GPIO.OUT)                  # initialize GPIO Pin as outputs
GPIO.setup(ECHO1,GPIO.IN)                   # initialize GPIO Pin as input

GPIO.setup(TRIG2,GPIO.OUT)                  
GPIO.setup(ECHO2,GPIO.IN)                  

GPIO.setup(TRIG3,GPIO.OUT)                  
GPIO.setup(ECHO3,GPIO.IN)                   

GPIO.setup(buzz,GPIO.OUT)                  
GPIO.setup(m11,GPIO.OUT)
GPIO.setup(m12,GPIO.OUT)
GPIO.setup(m21,GPIO.OUT)
GPIO.setup(m22,GPIO.OUT)
GPIO.setup(buzz,GPIO.OUT)
time.sleep(5)

def stop():
    print "OBSTACLE AHEAD!!!"
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)
    

def forward():
    GPIO.output(m11, 1)
    GPIO.output(m12, 0)
    GPIO.output(m21, 1)
    GPIO.output(m22, 0)
    print "CLEAR.."

def back():
    GPIO.output(m11, 0)
    GPIO.output(m21, 0)
    GPIO.output(m12, 1)
    GPIO.output(m22, 1)
    time.sleep(0.5)
    GPIO.output(m12, 0)
    GPIO.output(m22, 0)
    print "REVERSE.."

def left():
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 1)
    time.sleep(0.5)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)
    print "TURNING LEFT.."

def right():
    GPIO.output(m11, 1)
    time.sleep(0.5)
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)
    print "TRUNING RIGHT.."

def buzzer():
    GPIO.output(buzz, 1)
    time.sleep(0.5)
    GPIO.output(buzz, 0)

stop()
count = 0


def action(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    print 'Received: %s' % command
    if command == 'Hi':
        telegram_bot.sendMessage (chat_id, str("Hi! NBA Team!!"))
    elif command == 'Time':
        telegram_bot.sendMessage(chat_id, str(now.hour)+str(":")+str(now.minute))
    elif command == 'Show logs':
        telegram_bot.sendDocument(chat_id, document=open('/home/pi/Desktop/logs.txt'))
    elif command == 'Test all systems':
        telegram_bot.sendMessage (chat_id, str("Testing Systems now!!"))
        buzzer()
        forward()
        time.sleep(0.5)
        buzzer()
        right()
        time.sleep(0.5)
        buzzer()
        left()
        time.sleep(0.5)
        stop()
    elif command == 'Start delivery':
        try:
            while True:
                i = 0
                avgDistance1 = 0
                avgDistance2 = 0
                avgDistance3 = 0

                for i in range(5):
                    GPIO.output(TRIG1, False)                 #Set TRIG1 as LOW
                    time.sleep(0.1)                                   #Delay
                    GPIO.output(TRIG1, True)                  #Set TRIG1 as HIGH
                    time.sleep(0.00001)
                    GPIO.output(TRIG1, False)
                    while GPIO.input(ECHO1)==0:            #Check whether the ECHO1 is LOW
                            GPIO.output(buzz, False)
                    pulse_start1 = time.time()
                    while GPIO.input(ECHO1) == 1:          #Check whether the ECHO1 is HIGH
                            GPIO.output(buzz, False)
                    pulse_end1 = time.time()     
                    
                    GPIO.output(TRIG2, False)                 #Set TRIG2 as LOW
                    time.sleep(0.1)
                    GPIO.output(TRIG2, True)                  #Set TRIG2 as HIGH
                    time.sleep(0.00001)
                    GPIO.output(TRIG2, False)
                    while GPIO.input(ECHO2)==0:            #Check whether the ECHO2 is LOW
                            GPIO.output(buzz, False)
                    pulse_start2 = time.time()
                    while GPIO.input(ECHO2) == 1:          #Check whether the ECHO2 is HIGH
                            GPIO.output(buzz, False)
                    pulse_end2 = time.time() 


                    GPIO.output(TRIG3, False)                 #Set TRIG3 as LOW
                    time.sleep(0.1)                                   #Delay
                    GPIO.output(TRIG3, True)                  #Set TRIG3 as HIGH
                    time.sleep(0.00001)
                    GPIO.output(TRIG3, False)
                    while GPIO.input(ECHO3)==0:            #Check whether the ECHO3 is LOW
                            GPIO.output(buzz, False)
                    pulse_start3 = time.time()
                    while GPIO.input(ECHO3) == 1:          #Check whether the ECHO3 is HIGH
                            GPIO.output(buzz, False)
                    pulse_end3 = time.time()
                    
      
                    pulse_duration1 = pulse_end1 - pulse_start1 #time to get back the pulse to sensor
                    pulse_duration2 = pulse_end2 - pulse_start2 
                    pulse_duration3 = pulse_end3 - pulse_start3 

                    
                    distance1 = pulse_duration1 * 17150        #Multiply pulse duration by 17150 (34300/2) to get distance
                    distance2 = pulse_duration2 * 17150        
                    distance3 = pulse_duration3 * 17150        

                    
                    distance1 = round(distance1, 2)            #Round to two decimal points
                    distance2 = round(distance2, 2)            
                    distance3 = round(distance3, 2)            

                    
                    avgDistance1 = avgDistance1 + distance1
                    avgDistance2 = avgDistance2 + distance2
                    avgDistance3 = avgDistance3 + distance3
                    
                avgDistance1 = avgDistance1/5
                avgDistance2 = avgDistance2/5
                avgDistance3 = avgDistance3/5

                
                print 'The distance left of the robot is:', avgDistance1
                print 'The distance front of the robot is:', avgDistance2
                print 'The distance right of the robot is:', avgDistance3

                
                flag1 = 0
                flag2 = 0
                flag3 = 0

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
                        if (count%2 == 1) & (flag1 == 0) & (flag2 == 0) & (flag3 == 0):
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
                
                        
telegram_bot = telepot.Bot('413893493:AAG7hDN750o1tWa35Hill7G6QBItq0RtAEY')
print (telegram_bot.getMe())
MessageLoop(telegram_bot, action).run_as_thread()
print 'Up and Running....'
while 1:
    time.sleep(5)
