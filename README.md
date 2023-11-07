# FancyDoor

## Build instructions:
1. Set up a Python 3.9.2 virtual environment
    - [Download and install Python 3.9.2](https://www.python.org/ftp/python/3.9.2/python-3.9.2-amd64.exe)
    - Once installed, go to Settings > Project: FancyDoor > Python Interpreter and select "Add Interpreter > Add Local Interpreter..."
    - Set up a new environment located at FancyDoor/venv, with the base interpreter configured as Python 3.9.2
2. Open the terminal in PyCharm (Alt + F12)
3. Run `./prototyping/setup_packages.bat`

4. [Download the RetinaNet library](https://github.com/OlafenwaMoses/ImageAI/releases/download/3.0.0-pretrained/retinanet_resnet50_fpn_coco-eeacb38b.pth/) and place in FancyDoor/prototyping/assets