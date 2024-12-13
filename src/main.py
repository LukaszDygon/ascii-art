import argparse
import string
from typing import List, Tuple, Union
import numpy as np
from PIL import ImageFont
import cv2
import curses
import emoji

FONT_H = 64
FONT_W = 64

BRIGHTNESS = 0 # Brightness control (0-100)
CONTRAST = 1 # Contrast control (1.0-3.0)

class AsciiCamera:
    intensity_to_ascii: List[Tuple[int, str]]
    intensity_to_emoji: List[Tuple[int, np.ndarray]]
    mode: str
    width: int
    height: int

    def __init__(self, mode: str, width: int, height: int):
        self._init_intensity_to_ascii()
        self._init_intensity_to_emoji()
        self.mode = mode
        self.width = width  
        self.height = height

    def _init_intensity_to_ascii(self):
        intensity = [(self._character_to_intensity(ch), ch) for ch in string.printable[:94]]
        max_character_intensity = max(intensity, key=lambda x: x[0])[0]
        self.intensity_to_ascii = sorted([(ch[0]/max_character_intensity*256, ch[1]) for ch in intensity], key=lambda x: x[0])
        
    def _init_intensity_to_emoji(self):
        intensity = [(self._emoji_to_intensity(ch), ch) for ch in list(emoji.EMOJI_DATA.keys())[100:300] if len(ch)==1]
        intensity = [i for i in intensity if i[0].shape]
        self.intensity_to_emoji = sorted([(ch[0], ch[1]) for ch in intensity], key=lambda x: sum(x[0]))

    def _character_to_intensity(self, character: str) -> float:
        font = ImageFont.truetype("fonts/Hack-Regular.ttf", FONT_H)
        mask = font.getmask(character)

        return sum(mask) / FONT_H * FONT_W
    
    def _emoji_to_intensity(self, emoji: str) -> np.ndarray:
        font = ImageFont.truetype('/System/Library/Fonts/Apple Color Emoji.ttc', 64)
        mask = np.array(font.getmask(emoji, mode='RGBA').convert('RGB'))
        avg_color = np.average(mask, axis=0)

        return np.array(avg_color)

    def _get_closest_character(self, intensity: Union[float, np.ndarray], map: Union[List[Tuple[float, str]], List[Tuple[np.ndarray, str]]]) -> str:
        if self.mode == 'emoji':
            return self._get_closest_character_rgb(intensity, map)
        elif self.mode == 'ascii':
            return self._get_closest_character_bw(intensity, map)
    
    def _get_closest_character_bw(self, intensity: float, map: List[Tuple[float, str]]) -> str:
        closest = min(map, key=lambda x:abs(x[0]-intensity))[1]

        return closest * 2

    def _get_closest_character_rgb(self, intensity: np.ndarray, map: List[Tuple[np.ndarray, str]]) -> str:
        closest = min(map, key=lambda x:np.linalg.norm(x[0]-intensity))[1]

        return closest
    
    def _image_to_vocab(self, img: np.ndarray, vocab: List[Tuple[float, str]]) -> List[str]:
        lines = []
        for row in img:
            line = ""
            for pixel in row:
                line += self._get_closest_character(np.mean(pixel), vocab)
            lines += [line]
        
        return lines

    def _image_to_emoji(self, img: np.ndarray) -> List[str]:
        lines = []
        for row in img:
            line = ""
            for character in row:
                line += self._get_closest_character(np.mean(character), self.intensity_to_emoji)
            lines += [line]
        
        return lines
    
    def run(self):
        if self.mode == 'ascii':
            vocabulary = self.intensity_to_ascii
        elif self.mode == 'emoji':
            vocabulary = self.intensity_to_emoji
        else:
            raise 'Mode not supported'

        cam = cv2.VideoCapture(0)
        screen = curses.initscr()
        curses.cbreak()
        curses.noecho()
        screen.nodelay(1)  # Make getch() non-blocking
        
        while True:
            # Check for any key press
            if screen.getch() != -1:  # -1 means no key was pressed
                break
                
            ret, img = cam.read()
            if not ret:
                print("failed to grab frame")
                break
            img_resized = cv2.resize(img, [self.width, self.height])
            img_adjusted = cv2.convertScaleAbs(img_resized, alpha=CONTRAST, beta=BRIGHTNESS)

            img_vocab = self._image_to_vocab(img_adjusted, vocabulary)
            for i, s in enumerate(img_vocab):
                screen.addstr(i, 0, s)
            screen.refresh()

        curses.echo()
        curses.nocbreak()
        curses.endwin()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert webcam feed to ASCII or Emoji.')
    parser.add_argument('--type', type=str, choices=['ascii', 'emoji'], default='ascii',
                        help='Choose to convert video feed to ascii or emoji.')
    parser.add_argument('--width', type=int, default=75,
                        help='Width of the output. Must be within the size of the command line window running the script.')
    parser.add_argument('--height', type=int, default=50,
                        help='Height of the output. Must be within the size of the command line window running the script.')
    args = parser.parse_args()
    AsciiCamera(args.type, args.width, args.height).run()