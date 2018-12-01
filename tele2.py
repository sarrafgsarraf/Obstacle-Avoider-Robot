import RPi.GPIO as GPIO
import time, datetime
import telepot
from telepot.loop import MessageLoop

now = datetime.datetime.now()

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
    f = open("/home/pi/Desktop/logs.txt", 'a')
    f.write('\n' + 'OBSTACLE AHEAD, CLEAR PATH TO RESUME SERVICE!')
    f.close()
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
    f = open("/home/pi/Desktop/logs.txt", 'a')
    f.write('\n' + 'CLEAR.')
    f.close()

def left():
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 1)
    GPIO.output(m22, 0)
    print "TURNING LEFT.."
    f = open("/home/pi/Desktop/logs.txt", 'a')
    f.write('\n' + 'TURNING LEFT..')
    f.close()

def right():
    GPIO.output(m11, 1)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)
    print "TURNING RIGHT.."
    f = open("/home/pi/Desktop/logs.txt", 'a')
    f.write('\n' + 'TURNING RIGHT..')
    f.close()

def buzzer():  
    GPIO.output(buzz, 1)
    time.sleep(0.5)
    GPIO.output(buzz, 0)
    
def stay():
    print "REACHED DESTINATION!"
    f = open("/home/pi/Desktop/logs.txt", 'a')
    f.write('\n' + 'REACHED DESTINATION!')
    f.close()
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



def action(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print 'Received: %s' % command

    if command == 'Hi':
        telegram_bot.sendMessage (chat_id, str("Hi! CircuitDigest"))
    elif command == 'Time':
        telegram_bot.sendMessage(chat_id, str(now.hour)+str(":")+str(now.minute))
    elif command == 'Test all systems':
        telegram_bot.sendMessage (chat_id, str("Testing Systems now!!"))
        buzzer()
        time.sleep(0.5)
        buzzer()
        time.sleep(0.5)
        buzzer()
        time.sleep(0.5)
    elif command == 'Start delivery':
        telegram_bot.sendMessage (chat_id, str("Starting process now!"))
        while command != 'Stop':
                avd = averageD()
                flag=0
                
                if(GPIO.input(2)==True and GPIO.input(3)==True and avd>20): #both while move forward     
                    forward()
                    f = open("/home/pi/Desktop/logs.txt", 'a')
                    f.write('\n' + avd)
                    f.close()
                    print avd
                elif(GPIO.input(2)==False and GPIO.input(3)==True and avd>20): #turn right  
                    right()
                    f = open("/home/pi/Desktop/logs.txt", 'a')
                    f.write('\n' + avd)
                    f.close()
                    print avd
                elif(GPIO.input(2)==True and GPIO.input(3)==False and avd>20): #turn left
                    left()
                    f = open("/home/pi/Desktop/logs.txt", 'a')
                    f.write('\n' + avd)
                    f.close()
                    print avd
                elif avd < 20:      #Check whether the distance is within 20 cm range
                    count=count+1
                    stop()
                    buzzer()
                    time.sleep(0.5)
                else:  #stay still
                    stay()
                    
    elif command == 'Show log':
         telegram_bot.sendDocument(chat_id, document=open('/home/pi/Desktop/logs.txt'))

telegram_bot = telepot.Bot('413893493:AAG7hDN750o1tWa35Hill7G6QBItq0RtAEY')
print (telegram_bot.getMe())

MessageLoop(telegram_bot, action).run_as_thread()
print 'Up and Running....'

while 1:
    time.sleep(10)
