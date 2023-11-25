#################################################
# Team: FancyDoor
# Team Members: 
#   Kenneth Granger
#   Samuel Griffin
#   Austin Mitchell
#
# Assignment: COSC3143 Project
# Description: A multi-stage door safety system
# Features:
#   Voice activation
#   Proximity detection
#   Retina Scan
#   Hand Scan
#   GUI-driven captcha
#   Triple layered keycode lock
#   - 4-key pin lock
#   - 8-key pin lock
#   - 16-key pin lock
#   Digital logic gate driven input combination
#   Servo controlled lock
# 
# Development Computer: Raspberry Pi 4B ARM-v8 64-bit 8GB
# Operating System: Raspbian (Debian) Linux 11 "Bullseye"
# Environment: Python 3.9.2
# IDE: Sublime Text
# Operational status: Functional
#################################################

# IMPORTS #
import logging
import os
import random
import sys
import tkinter as Tk
import cv2
import time
import RPi.GPIO as GPIO
import sounddevice as sd
import numpy as np

from PIL import ImageTk, Image
from captcha.image import ImageCaptcha
from imageai.Detection import ObjectDetection

# Perform GPIO Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Set up pins for servo and start PWM
entrypin = 21
motorpin = 19
GPIO.setup(entrypin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(motorpin, GPIO.OUT)
freq = 50
p = GPIO.PWM(motorpin, freq)
p.start(5)

# Set up pins for ultrasonic sensor
trigger = 11
echo = 13
GPIO.setup(trigger, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

# Declare global image path
image_path = "assets/image.jpg"
# Set up new logger for use in debugging
logger = logging.getLogger("debug_logger")

# Enables logging if run with command line argument '-d'
if len(sys.argv) != 1 and sys.argv[1] == '-d':
    handler = logging.StreamHandler(stream=sys.stderr)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    logger.debug("Logging enabled")
else:
    # Otherwise, set base logging level
    handler = logging.StreamHandler(stream=sys.stderr)
    handler.setLevel(logging.ERROR)
    logger.addHandler(handler)
    logger.setLevel(logging.ERROR)


# Given length of captcha, generate a captcha and return generated text
def generate_captcha(length):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    captcha_text = "".join(random.choice(characters) for _ in range(length))
    logger.debug("Generated captcha: " + captcha_text)
    image = ImageCaptcha(width=300, height=150, fonts=['assets/times.ttf', 'assets/lucon.ttf'])
    image.generate(captcha_text)
    path = "assets/CAPTCHA.png"
    image.write(captcha_text, path)
    return captcha_text.lower(), path


# Get an image from the video capture device
def get_image():
    global image_path
    try:
        cam = cv2.VideoCapture(0)
        while True:
            ret, image = cam.read()
            cv2.imshow('Imagetest',image)
            k = cv2.waitKey(1)
            if k != -1:
                break
        cv2.imwrite(image_path, image)
        cam.release()
        cv2.destroyAllWindows()
    except cv2.error:
        logger.error("OpenCV error detected, no image captured")
        return False
    return True


# Get normalized sound data
def get_sound(indata, outdata, frames, time, status):
    global sound_val 
    sound_val = np.linalg.norm(indata)*10


# Listen for voice activation
def listen(max_delta):
    global sound_val
    delta = 0
    prev_sound_val = 0
    try:
        while delta < max_delta:
            with sd.Stream(callback=get_sound):
                sd.sleep(50)
            delta = abs(sound_val - prev_sound_val)
            logger.debug(str(delta))
            prev_sound_val = sound_val
        return True
    except:
        logger.error("Sound Device error detected")
        return False


# Get distance from ultrasonic sensor
def distance():
    # set Trigger to HIGH
    GPIO.output(trigger, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(trigger, False)

    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(echo) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(echo) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    logger.debug("Distance function returning: " + str(distance))
    return distance


# image_recognizer
# Params: image_path    A string path to an image
# Returns: results      A tuple consisting of the prediction name and percent certainty
def image_recognizer(image_path):
    logger.debug("Recognizer called with path " + image_path + " , setting up model...")
    execution_path = os.getcwd()
    detector = ObjectDetection()

    # NOTE Change this to use different models
    # detector.setModelTypeAsRetinaNet()
    detector.setModelTypeAsYOLOv3()
    # detector.setModelTypeAsTinyYOLOv3()

    # detector.setModelPath(execution_path + "/assets/retinanet_resnet50_fpn_coco-eeacb38b.pth")
    detector.setModelPath(execution_path + "/assets/yolov3.pt")
    # detector.setModelPath(execution_path + "/assets/tiny-yolov3.pt")

    detector.loadModel()
    detector.useCPU()
    logger.debug("Model loaded successfully, performing image detection...")
    predictions = detector.detectObjectsFromImage(input_image=image_path, minimum_percentage_probability=30)
    results = []
    for prediction in predictions:
        results.append((prediction['name'], prediction['percentage_probability']))
    logger.debug("Detection finished. Returning results.")
    return results


# Application class handles GUI
class Application(Tk.Frame):
    pinCount = 0
    def __init__(self, master=None):
        Tk.Frame.__init__(self, master)
        self.captchaUserInput = Tk.StringVar()
        self.pin = Tk.StringVar()
        self.grid(sticky='nsew')
        logger.debug("Application initialized, setting up widgets...")
        self.createStartingWidgets()

    # Destroys all widgets in application
    def clearFrame(self):
        for widget in self.winfo_children():
            widget.destroy()

    # Clears frame and prompt user to quit GUI
    def lock(self):
        # Locks application
        self.clearFrame()
        self.lockLabel = Tk.Label(self, text="DOOR LOCKED - TRY AGAIN")
        self.lockLabel.grid(sticky='nsew', padx=(50, 50), pady=(50, 50))

        self.quitButton = Tk.Button(self, text="Quit", command=self.quit)
        self.quitButton.grid(sticky='ew', padx=(100, 100), pady=(5, 50))

    # Displays message to user when unlock successful and cleans up GPIO
    def unlock(self):
        logger.debug("Setting up unlock screen")
        self.clearFrame()
        self.successLabel = Tk.Label(self, text="Congration, you done it")
        self.successLabel.grid(sticky='ew', padx=(100, 100), pady=(5, 50))

        self.okButton = Tk.Button(self, text="OK", command=self.quit)
        self.okButton.grid(sticky='ew', padx=(100, 100), pady=(5, 50))
        GPIO.cleanup()


    # Captcha submission function validates captcha and sets up window for pin entry
    def submitCaptcha(self):
        logger.debug("Submitted captcha, checking now...")
        # Validate captcha here
        if self.captchaUserInput.get() == self.captchaText:
            logger.debug("Captcha succeeded, setting up pin entry")
            # Destroy and reconfigure buttons/entry boxes
            self.clearFrame()

            # Setup next application state (PIN entry)
            self.instructionLabel = Tk.Label(self, text="Enter 4-digit pin")
            self.instructionLabel.grid(sticky='ew', padx=(100, 100), pady=(50, 5))
            self.pinEntry = Tk.Entry(self, textvariable=self.pin, show="*")
            self.pinEntry.grid(sticky='ew', padx=(100, 100), pady=(5, 5))
            self.submitButton = Tk.Button(self, text="Submit", command=self.submitPin)
            self.submitButton.grid(sticky='ew', padx=(100, 100), pady=(5, 5))
            self.quitButton = Tk.Button(self, text="Quit", command=self.quit)
            self.quitButton.grid(sticky='ew', padx=(100, 100), pady=(5, 50))
        else:
            logger.debug("Captcha failed")
            self.lock()

    # Pin submission function validates pin entries, sets up each pin state, and calls success function on proper entry
    def submitPin(self):
        userPinInput = self.pin.get()
        if len(userPinInput) == 4 and userPinInput == "1234" and self.pinCount == 0:
            logger.debug("4-Digit pin passed")
            self.pinCount += 1
            # Update instruction label and clear pin field
            self.instructionLabel.configure(text="Enter 8-digit pin")
            self.pinEntry.delete(0, Tk.END)
            self.pinEntry.insert(0, "")
        elif len(userPinInput) == 8 and userPinInput == "12345678" and self.pinCount == 1:
            logger.debug("8-Digit pin passed")
            self.pinCount += 1
            self.instructionLabel.configure(text="Enter 16-digit pin")
            self.pinEntry.delete(0, Tk.END)
            self.pinEntry.insert(0, "")
        elif len(userPinInput) == 16 and userPinInput == "1234567890123456" and self.pinCount == 2:
            logger.debug("16-Digit pin passed")
            self.pinCount += 1
            self.logicGateSetup()
        else:
            logger.debug("Pin entry failed")
            self.lock()


    # Sets up prompt for user to complete logic gate function. Also sets up event detectors and callback function for logic gate input.
    def logicGateSetup(self):
        logger.debug("Setting up logic gate prompt frame")
        self.clearFrame()
        self.instructionLabel = Tk.Label(self, text="Success")
        self.instructionLabel.grid(sticky='ew', padx=(100, 100), pady=(50, 5))
        self.logicGateInstructions = Tk.Label(self, text="Complete the logic gate puzzle\n to unlock the door")
        self.logicGateInstructions.grid(sticky='ew', padx=(100, 100), pady=(5, 5))
        self.quitButton = Tk.Button(self, text="Quit", command=self.quit)
        self.quitButton.grid(sticky='ew', padx=(100, 100), pady=(5, 50))
        def callback(channel):
            global p
            p.ChangeDutyCycle(10.2)
            time.sleep(1.5)
            logger.debug("\nDOOR UNLOCKED\n")
            self.unlock()

        logger.debug("Setting up event detector for logic gate puzzle")
        GPIO.add_event_detect(entrypin, GPIO.RISING, callback = callback, bouncetime = 300)
        

    # Calls captcha generator and sets up frame with captcha image and text entry box
    def captchaSetup(self):
        logger.debug("Setting up Captcha frame")
        self.clearFrame()
        # User instructions
        self.instructionLabel = Tk.Label(self, text="Enter Captcha:")
        self.instructionLabel.grid(sticky='ew', padx=(100, 100), pady=(50, 5))

        # Generate captcha and show in label
        self.captchaText, captchaPath = generate_captcha(8)
        self.captchaImage = Image.open(captchaPath)
        self.captchaImageTk = ImageTk.PhotoImage(self.captchaImage)
        self.captchaLabel = Tk.Label(self, image=self.captchaImageTk)
        self.captchaLabel.image = self.captchaImageTk
        self.captchaLabel.grid(sticky='new', padx=(0, 0), pady=(5, 5))

        self.captchaEntry = Tk.Entry(self, textvariable=self.captchaUserInput)
        self.captchaEntry.grid(sticky='ew', padx=(100, 100), pady=(5, 5))

        self.submitButton = Tk.Button(self, text="Submit", command=self.submitCaptcha)
        self.submitButton.grid(sticky='ew', padx=(100, 100), pady=(5, 5))

        self.quitButton = Tk.Button(self, text="Quit", command=self.quit)
        self.quitButton.grid(sticky='ew', padx=(100, 100), pady=(5, 5))


    # Calls image recognizer and sets up frame to display to user while recognizer is running. Also handles return from recognizer.
    def imageScanSuccess(self):
        logger.debug("Setting up transient image recognition screen")
        global image_path
        self.clearFrame()
        self.infoLabel = Tk.Label(self, text="Please wait, recognizing image...")
        self.infoLabel.grid(sticky='ew', padx=(100, 100), pady=(50, 5))
        self.quitButton = Tk.Button(self, text="Quit", command=self.quit)
        self.quitButton.grid(sticky='ew', padx=(100, 100), pady=(5, 5))
        self.update()
        results = image_recognizer(image_path)
        for name, percentage in results:
            logger.debug("Recognizing " + name + " with certainty " + str(percentage))
            if name == 'person' and percentage > 60:
                logger.debug("Succeeded image recognition")
                self.infoLabel.configure(text="Image recognition success.\nPlease proceed to the next step.")
                self.update()
                time.sleep(3)
                return True
        logger.debug("Failed image recognition")
        return False


    # Calls function to get image from function and handles state returned by image scanner, locking or passing to captcha setup
    def handScanSetup(self):
        logger.debug("Setting up hand scanner frame")
        self.clearFrame()
        self.instructionLabel = Tk.Label(self, text="Hand Scan: Press any key to capture image")
        self.instructionLabel.grid(sticky='ew', padx=(100, 100), pady=(50,5))

        self.quitButton = Tk.Button(self, text="Quit", command=self.quit)
        self.quitButton.grid(sticky='ew', padx=(100, 100), pady=(5, 5))
        self.update()
        #time.sleep(.5)
        return_val = get_image()
        if return_val:
            logger.debug("Image created successfully")
            if self.imageScanSuccess():
                logger.debug("Image scanned successfully")
                self.captchaSetup()
            else:
                logger.debug("Hand scan failed")
                self.lock()
        else:
            self.lock()


    # Calls function to get image from function and handles state returned by image scanner, locking or passing to hand scanner
    def retinaScanSetup(self):
        logger.debug("Setting up retina scanner frame")
        self.clearFrame()
        self.instructionLabel = Tk.Label(self, text="Retina Scan: Press any key to capture image")
        self.instructionLabel.grid(sticky='ew', padx=(100, 100), pady=(50,5))

        self.quitButton = Tk.Button(self, text="Quit", command=self.quit)
        self.quitButton.grid(sticky='ew', padx=(100, 100), pady=(5, 5))
        self.update()
        #time.sleep(.5)
        return_val = get_image()
        if return_val:
            logger.debug("Image created successfully")
            if self.imageScanSuccess():
                logger.debug("Image scanned successfully")
                self.handScanSetup()
            else:
                logger.debug("Retina scan failed")
                self.lock()
        else:
            self.lock()


    # Sets up first state of program. Prompts user for voice command and calls listen function, then queries distance function and validates both values.
    def createStartingWidgets(self):
        logger.debug("Setting up starting widgets")
        self.instructionLabel = Tk.Label(self, text="Voice validation needed.\n Please speak into the microphone.")
        self.instructionLabel.grid(sticky='ew', padx=(100, 100), pady=(50, 5))

        self.quitButton = Tk.Button(self, text="Quit", command=self.quit)
        self.quitButton.grid(sticky='ew', padx=(100, 100), pady=(5, 5))
        # Force update before calling logic
        self.update()

        # Start listening for audio at threshold 100
        logger.debug("Listening for voice")
        voice_validation = listen(100)

        # Get current distance
        logger.debug("Getting distance")
        proximity = distance()

        # Call retina scan if voice and proximity thresholds passed
        if voice_validation and proximity < 30:
            self.retinaScanSetup()
        else:
            self.lock()


# Initialize app
root = Tk.Tk()
app = Application()


def main():
    global app
    app.master.title("Fancy Door")
    app.mainloop()


if __name__ == "__main__":
    main()
