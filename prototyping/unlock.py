import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

BUTTONPIN = 19
motorpin = 21
GPIO.setup(BUTTONPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(motorpin,GPIO.OUT)
print("something")
freq = 50
p = GPIO.PWM(motorpin, freq)
print("something")



p.start(5)
def unlock(condition):
	if condition: 
		p.ChangeDutyCycle(10.2)
		
def piside (channel):
	global p
	print("something")
	"""
	for i in range(50,100):
		p.ChangeDutyCycle(i/10)
		time.sleep(2)
		print(i/10)
	"""
	p.ChangeDutyCycle(10.2)
GPIO.add_event_detect(BUTTONPIN, GPIO.FALLING, callback=piside, bouncetime = 300)
"""

if __name__ == "__main__":
	main()
"""
try:
	input("Press enter to quit\n\n")


except KeyboardInterrupt:
	GPIO.cleanup()
	p.ChangeDutyCycle(5)
finally: 
	GPIO.cleanup()
