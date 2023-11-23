# FancyDoor

## Build instructions for PyCharm on Windows:
1. Set up a Python 3.9.2 virtual environment
    - [Download and install Python 3.9.2](https://www.python.org/ftp/python/3.9.2/python-3.9.2-amd64.exe)
    - Once installed, go to Settings > Project: FancyDoor > Python Interpreter and select "Add Interpreter > Add Local Interpreter..."
    - Set up a new environment located at FancyDoor/venv, with the base interpreter configured as Python 3.9.2
2. Open the terminal in PyCharm (Alt + F12)
3. Run `./prototyping/setup_packages.bat`

4. [Download the YOLOv3 library](https://github.com/OlafenwaMoses/ImageAI/releases/download/3.0.0-pretrained/yolov3.pt/) and place in FancyDoor/prototyping/assets

## Build instructions for Raspberry Pi 4B:
1. Ensure Python 3.9.2 is installed
2. Open the terminal to the project folder
3. Run `./prototyping/setup_packages.sh`
4. [Download the YOLOv3 library](https://github.com/OlafenwaMoses/ImageAI/releases/download/3.0.0-pretrained/yolov3.pt/) and place in FancyDoor/prototyping/assets
