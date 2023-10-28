import time
import RPi.GPIO as GPIO


#Define pins and the pin for the button
buttonPin = 11
#b7 is the MSB, connected pin 19, b0 is the LSB
b7 = 19
b6 = 21
b5 = 23
b4 = 29
b3 = 31
b2 = 33
b1 = 35
b0 = 37



# Setup GPIO and for button
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize states for pins
pinOn = GPIO.HIGH
pinOff = GPIO.LOW

#Defines pins as outputs
gpiopin = [b7, b6, b5, b4, b3, b2, b1, b0]
for i in range(0,8):
    GPIO.setup(gpiopin[i],GPIO.OUT)
    
    #                                                                    def convertBinary(decimal):
    #                                                                        binary = bin(decimal)
    #                                                                        binary = binary.replace('0b', '')
    #                                                                        binary = binary.zfill(8)
    #                                                                        return binary

        #display on LEDs
   # for i in range(0,8):
    #    GPIO.output(gpiopin[i], binary[i])
    
def button_callback(channel):
    interface()

    
    

        
   


GPIO.add_event_detect(BUTTONPIN, GPIO.FALLING, callback=button_callback, bouncetime = 300)

