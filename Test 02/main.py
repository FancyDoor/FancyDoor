import tkinter as Tk
from tkinter import LEFT, RIGHT
from threading import Thread



root = Tk.Tk()

class Application(Tk.Frame):
    def __init__(self, master=None):
        Tk.Frame.__init__(self, master)
        self.grid(sticky='nsew')
        self.createWidgets()

    def createWidgets(self):
        self.optionVar = Tk.StringVar()
        optionList = (range(1, 55))
        # Current option from optionList
        self.optionVar.set(optionList[0])
        self.optionVar.trace()

        self.om = Tk.OptionMenu(self, self.optionVar, *optionList)
        self.om.grid(sticky = Tk.W, padx=(50, 50), pady=(50, 0))

        self.quitButton = Tk.Button(self, text="Quit", command=self.quit)
        self.quitButton.columnconfigure(0, weight=1)
        self.quitButton.grid(sticky='ew', padx=(50, 50), pady=(0, 50))


def testfunction(app)
    val = app.optionVar.get()
    print(val)




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

def main():
    app = Application()
    app.master.title("Sample Application")
    app.mainloop()


if __name__ == "__main__":
    main()
