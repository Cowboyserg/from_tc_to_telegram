import os
import math
import subprocess
import datetime
import re
import moviepy.editor as mp
import cv2
from PIL import Image, ImageGrab
import pyautogui
import time
import win32clipboard

def get_cb():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return data

def get_Len1(filename):
    cap = cv2.VideoCapture(filename)
    fps = cap.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count/fps
    minutes = int(duration/60)
    seconds = duration%60
    cap.release()
    return duration

def find_blue_pixel_in_tc():
    image = ImageGrab.grab()
    obj = image.load()
    print(obj)
    for i in range(304, 985):
        for j in range(184, 788):
            if obj[i,j] == (204, 232, 255):
                coor_i = i+3
                coor_j = j+3
                return [coor_i,coor_j]
                # print(coor_i, coor_j)
                # pyautogui.moveTo([coor_i,coor_j])

def getLength(filename):
  result = subprocess.Popen([r"d:\projects\programms_for_every_day\twitch3_find_download\ffprobe.exe", filename],stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
  return [re.findall(r"ation:\s([.]+),",str(x))[0] for x in result.stdout.readlines() if b'Duration' in x]


def get_videos_names():
    return [i for i in os.listdir() if "mp4" in i]

if __name__ == "__main__":
    videos = get_videos_names()
    len_of_parts = 44
    for i in videos:
        if "part" not in i and "mp4" in i:
            # duration = mp.VideoFileClip(i).duration
            duration = get_Len1(i)
            duration_t = datetime.timedelta(seconds=int(duration))
            count_of_parts = math.ceil(duration/(60*len_of_parts))
            print("Количество частей", count_of_parts)
            for j in range(count_of_parts):
                start = datetime.timedelta(minutes=j*len_of_parts)
                delta = datetime.timedelta(minutes=len_of_parts)
                old_name = i
                if j == count_of_parts-1:
                    print("Последняя часть")
                    command = f'ffmpeg.exe -i "{i}" -vcodec copy -acodec copy -ss {str(datetime.timedelta(minutes=len_of_parts*(j)))} -t {duration_t-datetime.timedelta(minutes=len_of_parts*(j))} -async 1 "{i.replace(".mp4","")}__part{j+1}__{str(start).replace(":","_")}__{str(duration_t).replace(":","_")}.mp4"'
                else:
                    command = f'ffmpeg.exe -i "{i}" -vcodec copy -acodec copy -ss {start} -t {delta} -async 1 "{i.replace(".mp4","")}__part{j+1}__{str(start).replace(":","_")}__{str(start+delta).replace(":","_")}.mp4"'
                print(command)
                subprocess.check_call(command)
                start += delta