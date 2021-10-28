# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from pathlib import Path

import main_classes as mc



if __name__ == '__main__':
    saving_folder = Path('/home/federico/Videos')
    current_video = mc.Video()
    path = Path('/home/federico/Videos/Got01.mp4/ypr/176.json')
    current_video.acquire_frame(path)
    current_video.frame.observer.save_interactions(saving_folder)
    print(f'ciao')