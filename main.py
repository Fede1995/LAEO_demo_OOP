# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
from pathlib import Path

import main_classes as mc

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
           alist.sort(key=natural_keys) sorts in human order
           http://nedbatchelder.com/blog/200712/human_sorting.html
           (See Toothy's implementation in the comments)
           '''
    return [atoi(c) for c in re.split(r'(\d+)', text)]

if __name__ == '__main__':
    saving_folder = Path('/home/federico/Videos')
    current_video = mc.Video()
    path = Path('/home/federico/Videos/Got01.mp4/ypr')
    frame_names = []


    for f in path.iterdir():
        if f.is_file():
            frame_names.append(f.name)
    frame_names.sort(key=natural_keys)

    for f in frame_names:
        current_video.acquire_frame(path / f)
        current_video.frame.observer.save_interactions(saving_folder)
    print(f'ciao')