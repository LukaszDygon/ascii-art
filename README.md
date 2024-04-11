# AsciiCamera

## Overview

AsciiCamera is a Python tool that converts webcam feed into real-time ASCII or Emoji characters. It uses OpenCV, Curses, and Python's string and emoji libraries.

_Note: I have tested this on MacOS. Because it uses Curses and PIL libraries, other operating systems may require some changes to work._

## How to Run

Ensure you have Python 3.6 or above and Poetry installed.

Install dependencies with:

```bash
source ./.venv/bin/activate
pip install poetry
poetry install
```

Run AsciiCamera with:

```bash
poetry run python main.py --type [ascii/emoji] --width [output width] --height [output height]
```

Replace `[ascii/emoji]` with `ascii` or `emoji`, and `[output width]` and `[output height]` with desired dimensions. Defaults are `ascii`, `75`, and `50` respectively.

Example run:

```bash
poetry run python main.py --type ascii --width 100 --height 75
```

_Note: For the script to run successfully, your command line window needs to be at least the width and height specified_
