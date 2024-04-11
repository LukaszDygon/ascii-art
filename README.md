## Setup

```shell
poetry install
```

# AsciiCamera

## Overview

AsciiCamera is a Python tool that converts webcam feed into real-time ASCII or Emoji characters. It uses OpenCV, Curses, and Python's string and emoji libraries.

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
poetry run python ascii.py --type [ascii/emoji] --width [output width] --height [output height]
```

Replace `[ascii/emoji]` with `ascii` or `emoji`, and `[output width]` and `[output height]` with desired dimensions. Defaults are `ascii`, `75`, and `50` respectively.

Example run:

```bash
poetry run python ascii.py --type ascii --width 100 --height 75
```
