#########
# Team: FancyDoor
# Team Members:
#   Kenneth Granger
#   Samuel Griffin
#   Austin Mitchell
# 
# Assignment: Test 02
# File: main.py
# Purpose: Python 3 code instantiates a GUI and allows the user to select a number n. When the button is pressed,
#          the nth prime is calculated and output to the GUI in decimal and the LED display in binary.
#
# Development Computer: Raspberry Pi 4B ARM-v8 64-bit 8GB
# Operating System: Raspbian (Debian) Linux 11 "Bullseye"
# Environment: Python 3.9.2
# IDE: Sublime Text
# Operational status: Functional
#########
import tkinter as Tk
from threading import Thread
import RPi.GPIO as GPIO


# Define pins and the pin for the button
buttonPin = 11
# b7 is the MSB, connected pin 19, b0 is the LSB
b7 = 19
b6 = 21
b5 = 23
b4 = 29
b3 = 31
b2 = 33
b1 = 35
b0 = 37

# Initialize states for pins
pinOn = GPIO.HIGH
pinOff = GPIO.LOW

# Defines pins as outputs
gpiopin = [b7, b6, b5, b4, b3, b2, b1, b0]
# Global result stores result of nth prime calculation
result = 0
root = Tk.Tk()


# Set up GPIO mode and pin functionality
def setup_GPIO():
    global gpiopin, pinOn, pinOff, buttonPin
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    for pin in range(0, 8):
        GPIO.setup(gpiopin[pin], GPIO.OUT)
        # Turn all pins off
        GPIO.output(gpiopin[pin], pinOff)



# BEGIN APPLICATION LOGIC #
class Application(Tk.Frame):
    def __init__(self, master=None):
        Tk.Frame.__init__(self, master)
        self.grid(sticky='nsew')
        self.createWidgets()

    def createWidgets(self):
        # User instructions
        self.instructionLabel = Tk.Label(self, text="Select a number, \nthen press the button!")
        self.instructionLabel.grid(sticky='ew', padx=(50, 50), pady=(50, 5))

        # Option variable and list of options for numbers
        self.optionVar = Tk.StringVar()
        optionList = (range(1, 55))
        # Current option from optionList
        self.optionVar.set(str(optionList[0]))
        self.om = Tk.OptionMenu(self, self.optionVar, *optionList)
        self.om.grid(sticky='ew', padx=(50, 50), pady=(5, 0))

        self.quitButton = Tk.Button(self, text="Quit", command=self.quit)
        self.quitButton.grid(sticky='ew', padx=(50, 50), pady=(0, 0))
        # Stores result of nth prime calculation
        self.resultLabel = Tk.Label(self, text="Result: ")
        self.resultLabel.grid(sticky='ew', padx=(50, 50), pady=(0, 50))

# Initial GPIO setup and application instantiation
setup_GPIO()
app = Application()


# Clear GPIO and start interface thread
def button_callback(channel):
    global result
    GPIO.cleanup()
    th = Thread(target=interface)
    th.start()


# Interface with GUI, GPIO, and computation thread
def interface():
    global app, result, gpiopin, buttonPin
    # Get selected value from GUI and start computation thread
    n = app.optionVar.get()
    th = Thread(target=nthPrime, args=(n,))
    th.start()

    # Wait for computation thread to stop before operating on result
    th.join()

    # Output converted result to GPIO
    result_bin = convertBinary(result)
    setup_GPIO()
    for i in range(0, 8):
        GPIO.output(gpiopin[i], int(result_bin[i]))

    # Output result to GUI
    result_string = "Result: " + str(result)
    app.resultLabel.config(text=result_string)

    # Reset button callback
    GPIO.remove_event_detect(buttonPin)
    GPIO.add_event_detect(buttonPin, GPIO.FALLING, callback=button_callback, bouncetime=300)


# Converts given decimal value to binary with zero fill for GPIO output
def convertBinary(decimal):
    binary = bin(decimal)
    binary = binary.replace('0b', '')
    binary = binary.zfill(8)
    return binary


# Gets nth prime number
def nthPrime(n):
    global result
    # x is the index, number is the nth prime number
    number = 1
    n = int(n)
    x = 0
    while x < n:  # while x is less than n (so that the xth prime number is the nth prime number)
        number = number + 1
        # If the number is prime, increase the count of prime numbers found
        if isprime(number):
            x = x + 1
    # Return the nth prime number
    result = number


# Returns True if num is prime
def isprime(num):
    # For all the numbers between 2 and 1-number were testing to see if its prime
    for i in range(2, num):
        # If the number is not prime, return false
        if num % i == 0:
            return False
    return True


# Initialize event detector for button
GPIO.add_event_detect(buttonPin, GPIO.FALLING, callback=button_callback, bouncetime=300)


# Run app mainloop
def main():
    global app
    app.master.title("Test 02")
    app.mainloop()


if __name__ == "__main__":
    main()
