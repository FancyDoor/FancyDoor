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

# WHAT DOES ANY OF THIS MEAN
import logging, random, sys, os
from captcha.image import ImageCaptcha
from imageai.Detection import ObjectDetection


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


def image_recognizer(image_path):
    execution_path = os.getcwd()
    detector = ObjectDetection()
    # NOTE Change this to use different models
    detector.setModelTypeAsRetinaNet()
    # detector.setModelTypeAsYOLOv3()
    # detector.setModelTypeAsTinyYOLOv3()
    detector.setModelPath(execution_path + "\\assets\\retinanet_resnet50_fpn_coco-eeacb38b.pth")
    detector.loadModel()
    predictions = detector.detectObjectsFromImage(input_image=image_path, minimum_percentage_probability=30)
    names = []
    for prediction in predictions:
        names.append(prediction['name'])
    return names


def main():
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
        names = image_recognizer(i)
        print("Image predictions for", i)
        for name in names:
            print(" -", name)


if __name__ == "__main__":
    main()
