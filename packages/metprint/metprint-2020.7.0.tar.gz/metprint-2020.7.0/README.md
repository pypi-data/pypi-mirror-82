[![Github top language](https://img.shields.io/github/languages/top/FHPythonUtils/MetPrint.svg?style=for-the-badge)](../../)
[![Codacy grade](https://img.shields.io/codacy/grade/4361c2b314a94e77a69b674885d7393a.svg?style=for-the-badge)](https://www.codacy.com/gh/FHPythonUtils/MetPrint)
[![Repository size](https://img.shields.io/github/repo-size/FHPythonUtils/MetPrint.svg?style=for-the-badge)](../../)
[![Issues](https://img.shields.io/github/issues/FHPythonUtils/MetPrint.svg?style=for-the-badge)](../../issues)
[![License](https://img.shields.io/github/license/FHPythonUtils/MetPrint.svg?style=for-the-badge)](/LICENSE.md)
[![Commit activity](https://img.shields.io/github/commit-activity/m/FHPythonUtils/MetPrint.svg?style=for-the-badge)](../../commits/master)
[![Last commit](https://img.shields.io/github/last-commit/FHPythonUtils/MetPrint.svg?style=for-the-badge)](../../commits/master)
[![PyPI Downloads](https://img.shields.io/pypi/dm/metprint.svg?style=for-the-badge)](https://pypi.org/project/metprint/)
[![PyPI Version](https://img.shields.io/pypi/v/metprint.svg?style=for-the-badge)](https://pypi.org/project/metprint/)

<!-- omit in TOC -->
# MetPrint

<img src="readme-assets/icons/name.png" alt="Project Icon" width="750">

Pretty print text in a range of builtin formats or make your own

Example usage in your project
```python
from metprint import (
	LogType,
	Logger,
	MeterpreterFormatter,
)

metLogger = Logger(MeterpreterFormatter())
metLogger.logPrint("none", LogType.NONE)
metLogger.logPrint("bold indent", LogType.BOLD, True)
metLogger.logPrint("italic indent", LogType.ITALIC, True)
metLogger.logPrint("header", LogType.HEADER)
metLogger.logPrint("debug", LogType.DEBUG)
metLogger.logPrint("info", LogType.INFO)
metLogger.logPrint("success", LogType.SUCCESS)
metLogger.logPrint("warning", LogType.WARNING)
metLogger.logPrint("error", LogType.ERROR)
metLogger.logPrint("critical", LogType.CRITICAL)
```

Output of test.py
<div>
<img src="readme-assets/screenshots/desktop/screenshot-0.svg" alt="Screenshot 1" width="500">
</div>

Alternatively, you may prefer to make use of the `LAZY_PRINT` function.
Set `builtins.METPRINT_LAZY_FORMATTER` to customize the formatter.

Also, you have the option to show dependencies some love with
`builtins.METPRINT_DONATIONS` add a dictionary of projects and the
donations/ funding URL. Note that this is outputted on import.

See below for example usage of these.
```python
#!/usr/bin/env python3
"""Test metprint LAZY_PRINT and donations
"""
import builtins

# Show some love to 'Test'
builtins.METPRINT_DONATIONS = {"Test": "Test URL"}
# Set this if you want to set the LAZY_PRINT formatter
builtins.METPRINT_LAZY_FORMATTER = "FHFormatter"

from metprint import LAZY_PRINT, LogType

print("#########################")
print("#      FHFormatter      #")
print("#########################")
# You will still need LogType for this
LAZY_PRINT("none", LogType.NONE)
LAZY_PRINT("bold", LogType.BOLD)
LAZY_PRINT("italic", LogType.ITALIC)
LAZY_PRINT("header", LogType.HEADER)
LAZY_PRINT("debug", LogType.DEBUG)
LAZY_PRINT("info", LogType.INFO)
LAZY_PRINT("success", LogType.SUCCESS)
LAZY_PRINT("warning", LogType.WARNING)
LAZY_PRINT("error", LogType.ERROR)
LAZY_PRINT("critical", LogType.CRITICAL)

# Test that the donations message is not triggered again
#pylint: disable=unused-import
import metprint
```

Output of lazytest.py (for simplicity this is the output copied from the
terminal so note that the actual output contains colours as above)
```none
1 project is looking for funding:

Test: Test URL

#########################
#      FHFormatter      #
#########################
none
bold
italic
header
[$  Deb] debug
[* Info] info
[+   Ok] success
[/ Warn] warning
[-  Err] error
[! Crit] critical
```

- [Install With PIP](#install-with-pip)
- [Language information](#language-information)
	- [Built for](#built-for)
- [Install Python on Windows](#install-python-on-windows)
	- [Chocolatey](#chocolatey)
	- [Download](#download)
- [Install Python on Linux](#install-python-on-linux)
	- [Apt](#apt)
- [How to run](#how-to-run)
	- [With VSCode](#with-vscode)
	- [From the Terminal](#from-the-terminal)
- [How to update, build and publish](#how-to-update-build-and-publish)
- [Download](#download-1)
	- [Clone](#clone)
		- [Using The Command Line](#using-the-command-line)
		- [Using GitHub Desktop](#using-github-desktop)
	- [Download Zip File](#download-zip-file)
- [Community Files](#community-files)
	- [Licence](#licence)
	- [Changelog](#changelog)
	- [Code of Conduct](#code-of-conduct)
	- [Contributing](#contributing)
	- [Security](#security)

## Install With PIP

```python
pip install metprint
```

Head to https://pypi.org/project/metprint/ for more info


## Language information
### Built for
This program has been written for Python 3 and has been tested with
Python version 3.8.0 <https://www.python.org/downloads/release/python-380/>.

## Install Python on Windows
### Chocolatey
```powershell
choco install python
```
### Download
To install Python, go to <https://www.python.org/> and download the latest
version.

## Install Python on Linux
### Apt
```bash
sudo apt install python3.8
```

## How to run
### With VSCode
1. Open the .py file in vscode
2. Ensure a python 3.8 interpreter is selected (Ctrl+Shift+P > Python:Select
Interpreter > Python 3.8)
3. Run by pressing Ctrl+F5 (if you are prompted to install any modules, accept)
### From the Terminal
```bash
./[file].py
```

## How to update, build and publish

1. Ensure you have installed the following dependencies
	Linux
	```bash
	wget dephell.org/install | python3.8
	wget https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3.8
	```
	Windows
	```powershell
	(wget dephell.org/install -UseBasicParsing).Content | python
	(wget https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
	```
2. Use poetry for the heavy lifting and dephell to generate requirements
	```bash
	poetry update
	dephell deps convert
	```
3. Build/ Publish
	```bash
	poetry build
	poetry publish
	```
	or
	```bash
	poetry publish --build
	```


## Download
### Clone
#### Using The Command Line
1. Press the Clone or download button in the top right
2. Copy the URL (link)
3. Open the command line and change directory to where you wish to
clone to
4. Type 'git clone' followed by URL in step 2
```bash
$ git clone https://github.com/FHPythonUtils/MetPrint
```

More information can be found at
<https://help.github.com/en/articles/cloning-a-repository>

#### Using GitHub Desktop
1. Press the Clone or download button in the top right
2. Click open in desktop
3. Choose the path for where you want and click Clone

More information can be found at
<https://help.github.com/en/desktop/contributing-to-projects/cloning-a-repository-from-github-to-github-desktop>

### Download Zip File

1. Download this GitHub repository
2. Extract the zip archive
3. Copy/ move to the desired location

## Community Files
### Licence
MIT License
Copyright (c) FredHappyface
(See the [LICENSE](/LICENSE.md) for more information.)

### Changelog
See the [Changelog](/CHANGELOG.md) for more information.

### Code of Conduct
In the interest of fostering an open and welcoming environment, we
as contributors and maintainers pledge to make participation in our
project and our community a harassment-free experience for everyone.
Please see the
[Code of Conduct](https://github.com/FHPythonUtils/.github/blob/master/CODE_OF_CONDUCT.md) for more information.

### Contributing
Contributions are welcome, please see the [Contributing Guidelines](https://github.com/FHPythonUtils/.github/blob/master/CONTRIBUTING.md) for more information.

### Security
Thank you for improving the security of the project, please see the [Security Policy](https://github.com/FHPythonUtils/.github/blob/master/SECURITY.md) for more information.
