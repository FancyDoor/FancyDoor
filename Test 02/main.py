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

# Setup GPIO and for button
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize states for pins
pinOn = GPIO.HIGH
pinOff = GPIO.LOW

# Defines pins as outputs
gpiopin = [b7, b6, b5, b4, b3, b2, b1, b0]
for pin in range(0, 8):
    GPIO.setup(gpiopin[pin], GPIO.OUT)
    # Turn all pins off
    GPIO.output(gpiopin[pin], pinOff)

result = 0
root = Tk.Tk()


# BEGIN APPLICATION LOGIC #
class Application(Tk.Frame):
    def __init__(self, master=None):
        Tk.Frame.__init__(self, master)
        self.grid(sticky='nsew')
        self.createWidgets()

    def createWidgets(self):
        self.optionVar = Tk.StringVar()
        optionList = (range(1, 55))
        # Current option from optionList
        self.optionVar.set(str(optionList[0]))
        self.om = Tk.OptionMenu(self, self.optionVar, *optionList)
        self.om.grid(sticky='ew', padx=(50, 50), pady=(50, 0))

        self.quitButton = Tk.Button(self, text="Quit", command=self.quit)
        self.quitButton.grid(sticky='ew', padx=(50, 50), pady=(0, 0))

        self.resultLabel = Tk.Label(self, text="Result: 0")
        self.resultLabel.grid(sticky='ew', padx=(50, 50), pady=(0, 50))

        # add results display widget


app = Application()


def interface():
    global app, result, gpiopin
    # Get N from GUI
    n = app.optionVar.get()
    # Start threading for compute function, passing n
    th = Thread(target=nthPrime, args=n)
    th.start()
    # Wait for computation thread to stop
    th.join()
    # Output N to GUI and Circuit
    # GPIO.output()
    # 1. Convert to Binary
    # 2. Output to each pin
    result_bin = convertBinary(result)
    for i in range(0, 8):
        GPIO.output(gpiopin[i], result_bin[i])
    # Output to GUI
    result_string = "Result: " + str(result)
    app.resultLabel.config(result_string)


def button_callback(channel):
    # Per press of the button, clear GPIO
    GPIO.cleanup()
    # Start thread for interface
    th = Thread(target=interface)
    th.start()


def convertBinary(decimal):
    binary = bin(decimal)
    binary = binary.replace('0b', '')
    binary = binary.zfill(8)
    return binary


def nthPrime(n):
    global result
    # x is the index
    # number is the nth prime number
    number = 1
    x = 0
    while x < n:  # while x is less than n (so that the xth prime number is the nth prime number)
        number = number + 1
        # If the number is prime, increase the count of prime numbers found
        if isprime(number):
            x = x + 1
    # Return the nth prime number
    result = number


def isprime(num):
    # For all the numbers between 2 and 1-number were testing to see if its prime
    for i in range(2, num):
        # If the number is not prime, return false
        if num % i == 0:
            return False
    return True


GPIO.add_event_detect(buttonPin, GPIO.FALLING, callback=button_callback, bouncetime=300)


def main():
    global app
    app.master.title("Test 02")
    app.mainloop()


if __name__ == "__main__":
    main()

# button function
# pass control to the interface


# Thread receives signal to perform computation (nth prime)
# Returns result to the circuit and the GUI

# Compute nth prime

# Give 1 to 54
# self.optionVar = Tk.StringVar()
# optionList = ('a', 'b', 'c', 'd')
# self.optionVar.set(optionList[0])
# self.om = Tk.OptionMenu(self, self.optionVar, *optionList)
# self.om.grid(sticky = Tk.W)

# Thread interfaces with circuit and GUI

# Thread gets number, performs computation, and returns to circuit and GUI thread
