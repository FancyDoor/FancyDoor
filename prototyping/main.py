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
import logging, random, sys, os
import tkinter as Tk
from captcha.image import ImageCaptcha
from imageai.Detection import ObjectDetection
from PIL import ImageTk, Image


# Application class handles GUI
class Application(Tk.Frame):
    def __init__(self, master=None):
        Tk.Frame.__init__(self, master)
        self.grid(sticky='nsew')
        self.createWidgets()

    def createWidgets(self):
        # User instructions
        self.instructionLabel = Tk.Label(self, text="Select a number, \nthen press the button!")
        self.instructionLabel.grid(sticky='ew', padx=(50, 50), pady=(50, 5))

        # # Option variable and list of options for numbers
        # self.optionVar = Tk.StringVar()
        # optionList = (range(1, 55))
        # # Current option from optionList
        # self.optionVar.set(str(optionList[0]))
        # self.om = Tk.OptionMenu(self, self.optionVar, *optionList)
        # self.om.grid(sticky='ew', padx=(50, 50), pady=(5, 0))

        self.quitButton = Tk.Button(self, text="Quit", command=self.quit)
        self.quitButton.grid(sticky='ew', padx=(50, 50), pady=(0, 0))

        # # Stores result of nth prime calculation
        # self.resultLabel = Tk.Label(self, text="Result: ")
        # self.resultLabel.grid(sticky='ew', padx=(50, 50), pady=(0, 50))


root = Tk.Tk()
# Initialize app
app = Application()


# Given length of captcha, generate a captcha and return generated text
def generate_captcha(length):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    captcha_text = "".join(random.choice(characters) for _ in range(length))
    logging.debug("Generated captcha: " + captcha_text)
    image = ImageCaptcha(width=300, height=150, fonts=['assets/times.ttf', 'assets/lucon.ttf'])
    image.generate(captcha_text)
    image.write(captcha_text, 'assets/CAPTCHA.png')
    return captcha_text


def captcha_handler():
    captcha_text = generate_captcha(8).lower()
    user_input = input("Captcha validation: ").lower()
    if captcha_text == user_input:
        print("Success")
    else:
        print("Incorrect captcha")


# image_recognizer
# Params: image_path    A string path to an image
# Returns: results      A tuple consisting of the prediction name and percent certainty
def image_recognizer(image_path):
    execution_path = os.getcwd()
    detector = ObjectDetection()
    # NOTE Change this to use different models
    detector.setModelTypeAsRetinaNet()
    # detector.setModelTypeAsYOLOv3()
    # detector.setModelTypeAsTinyYOLOv3()
    # NOTE Path for Windows
    detector.setModelPath(execution_path + "\\assets\\retinanet_resnet50_fpn_coco-eeacb38b.pth")
    # NOTE Path for Linux (RasPi)
    # detector.setModelPath(execution_path + "/assets/retinanet_resnet50_fpn_coco-eeacb38b.pth")

    detector.loadModel()
    predictions = detector.detectObjectsFromImage(input_image=image_path, minimum_percentage_probability=30)
    results = []
    for prediction in predictions:
        results.append((prediction['name'], prediction['percentage_probability']))
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
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
        logging.debug("Logging enabled")
    else:
        # Otherwise, set base logging level
        logging.basicConfig(stream=sys.stderr, level=logging.ERROR)

    # Test captcha functionality
    captcha_handler()

    # Test image recognition functionality
    paths = ["assets/hand.jpg"]
    for i in paths:
        results = image_recognizer(i)
        print("Image predictions for", i)
        for name, percentage in results:
            print(" -", name, "with certainty", percentage)
            if percentage > 60:
                print("SUCCESS")

    app.master.title("Fancy Door")
    app.mainloop()


if __name__ == "__main__":
    main()
