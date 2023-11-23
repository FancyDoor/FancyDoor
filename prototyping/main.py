# Build state machine for door
# Features:
#   Retina Scan.
#   Hand Scan.
#   Triple layered keycode lock.
#   - 4-key pin lock
#   - 8-key pin lock
#   - 16-key pin lock
#   Voice activation.
#   Distance detection activation.
#   GUI driven captcha.
#   Digital logic gate driven input combination.
#   Servo controlled locks.
#   Door will open (manually).

# IMPORTS #
import logging
import os
import random
import sys
import tkinter as Tk

from PIL import ImageTk, Image
from captcha.image import ImageCaptcha
from imageai.Detection import ObjectDetection
# Set up new logger for use in debugging
logger = logging.getLogger("debug_logger")


# Given length of captcha, generate a captcha and return generated text
def generate_captcha(length):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    captcha_text = "".join(random.choice(characters) for _ in range(length))
    logger.debug("Generated captcha: " + captcha_text)
    image = ImageCaptcha(width=300, height=150, fonts=['assets/times.ttf', 'assets/lucon.ttf'])
    image.generate(captcha_text)
    path = 'assets/CAPTCHA.png'
    image.write(captcha_text, path)
    return captcha_text.lower(), path


# Application class handles GUI
class Application(Tk.Frame):
    pinCount = 0
    def __init__(self, master=None):
        Tk.Frame.__init__(self, master)
        self.captchaUserInput = Tk.StringVar()
        self.pin = Tk.StringVar()
        self.grid(sticky='nsew')
        self.createWidgets()

    # Destroy all widgets in application and prompt user to quit GUI
    def lock(self):
        # Locks application
        for widget in self.winfo_children():
            widget.destroy()
        self.lockLabel = Tk.Label(self, text="DOOR LOCKED - TRY AGAIN")
        self.lockLabel.grid(sticky='nsew', padx=(50, 50), pady=(50, 50))

        self.quitButton = Tk.Button(self, text="Quit", command=self.quit)
        self.quitButton.grid(sticky='ew', padx=(100, 100), pady=(5, 50))

    # Captcha submission function validates captcha and sets up window for pin entry
    def submitCaptcha(self):
        logger.debug("Submitted captcha, check now")
        # Validate captcha here
        if self.captchaUserInput.get() == self.captchaText:
            # Destroy and reconfigure buttons/entry boxes
            self.captchaLabel.destroy()
            self.captchaEntry.destroy()
            self.submitButton.destroy()
            self.quitButton.destroy()

            # Setup next application state (PIN entry)
            self.instructionLabel.configure(text="Enter 4-digit pin")

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
            self.instructionLabel.configure(text="Success")
            self.pinEntry.destroy()
            self.submitButton.destroy()
            self.quitButton.destroy()
            self.logicGateInstructions = Tk.Label(self, text="Complete the logic gate puzzle"
                                                             "\nto unlock the door")
            self.logicGateInstructions.grid(sticky='ew', padx=(100, 100), pady=(5, 5))
            self.quitButton = Tk.Button(self, text="Quit", command=self.quit)
            self.quitButton.grid(sticky='ew', padx=(100, 100), pady=(5, 50))

            # TODO call function to set up listener for logic gate puzzle here

        else:
            logger.debug("Pin entry failed")
            self.lock()

    def createWidgets(self):
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


root = Tk.Tk()
# Initialize app
app = Application()


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

    # NOTE Path for Windows
    # detector.setModelPath(execution_path + "\\assets\\retinanet_resnet50_fpn_coco-eeacb38b.pth")
    # NOTE Path for Linux (RasPi)
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


# Retina and hand scanner - should open camera, take a picture, save the picture, and call image_recognizer with the
# image path. Will update state depending on success or fail.
# NOTE difference between the scanner and the recognizer is that the scanner handles state.
def scanner(state):
    # TODO Wrap in "if" block when state known
    if state:
        # TODO Get hand image from camera. Take a picture, save image & its path, and pass path to image_recognizer()
        # Recognize image
        result = image_recognizer("path/to/image")
        # Result is good if it detects a person with more than 60% certainty
        for name, percent in result:
            if name == 'person' and percent > 60:
                pass
            else:
                # TODO Figure out state control...
                break

        # Get eye image from camera
        # Recognize image
        result = image_recognizer("path/to/image")
        # Result is good if it detects a person with more than 60% certainty
        for name, percent in result:
            if name == 'person' and percent > 60:
                state += 1
    else:
        # If image recognition failed,
        state = 0


def main():
    global app

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

    # Disable this to only test image recognition
    app.master.title("Fancy Door")
    app.mainloop()

    # # Test image recognition functionality
    # paths = ["assets/hand.jpg"]
    # for i in paths:
    #     results = image_recognizer(i)
    #     print("Image predictions for", i)
    #     for name, percentage in results:
    #         print(" -", name, "with certainty", percentage)
    #         if percentage > 60:
    #             print("SUCCESS")
    #             break

    path = "assets/hand.jpg"
    results = image_recognizer(path)
    print("Image predictions: ")
    for name, percentage in results:
        print(" -", name, "with certainty", percentage)


if __name__ == "__main__":
    main()
