[![PyPi Release](https://img.shields.io/pypi/v/mercurygui.svg?style=flat)](https://pypi.org/project/mercurygui/)

# mercurygui
mercurygui provides a higher-level worker thread which regularly queries the MercuryiTC for its sensor readings and provides a live stream of this data to other parts of the software. This prevents individual functions from querying the MercuryiTC directly and causing unnecessary overhead.

The user interface for the cryostat plots historic temperature readings going back up to 24 h and provides access to relevant temperature control settings such as gas flow, heater power, and ramp speed while lower-level configurations such as calibration tables must be changed programmatically.


<img src="https://raw.githubusercontent.com/OE-FET/mercurygui/master/screenshots/MercuryGUI.png" alt="Screenshot of the user interface" width="800"/>

## Installation
Install the stable version from PyPi by running:
```console
$ pip install mercurygui
```
or the latest version from github:
```console
$ pip install git+https://github.com/OE-FET/mercurygui
```

## System requirements

- Linux or macOS
- Python 2.7 or 3.x

## Acknowledgements
Config modules are based on the implementation from [Spyder](https://github.com/spyder-ide).
