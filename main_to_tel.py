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
import numpy as np
import ctypes


def get_metrics():
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    return screensize

METRICS = get_metrics()

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

# ↓↓ alt25
# ↓↓
# ↓↓
# ↓↓

def find_box_tel():
    image = ImageGrab.grab()
    obj = image.load()
    flag = False
    for i in range(METRICS[0]):
        for j in range(METRICS[1]): # вниз
            # if obj[i,j] == (239, 253, 222): # для избранного
            #     pyautogui.moveTo(i,j)
            #     return [i,j]
            if obj[i,j] == (250, 167, 116): # для streams
                pyautogui.moveTo(i,j)
                return [i,j+100]


def find_box_tc():
    image = ImageGrab.grab()
    obj = image.load()
    flag = False
    # pix = np.array(obj)
    for i in range(METRICS[0]):
        for j in range(METRICS[1]): # вниз
            if obj[i,j] == (188, 220, 244): # начало голубой полоски, где имя
                x = i
                y = j
                for k in range(y, 768):
                    if obj[i,k] != (188, 220, 244): # верхний левый угол снизу от г.п.
                        i1 = i
                        j1 = k
                        # pyautogui.moveTo([i1,j1])
                        # time.sleep(1)
                        break
                for k in range(x, 1366):
                    if obj[k,j] != (188, 220, 244): # справа конец голубой полоски
                        i2 = k
                        j2 = j+(j1-j)
                        # pyautogui.moveTo([i2,j2])
                        # time.sleep(1)
                        break
                for k in range(j2, 768):
                    if obj[i2,k] == (240, 240, 240): # правая нижняя граница, первое серое по горизонтали
                        i3 = i2
                        j3 = k 
                        # pyautogui.moveTo([i3,j3])
                        # time.sleep(1)
                        flag = True
                        break
        if flag:
            break
    return [[i1,j1],[i2,j2],[i3,j3]]

def find_blue_pixel_in_tc():
    image = ImageGrab.grab()
    obj = image.load()
    box = find_box_tc()
    for i in range(box[0][0], box[1][0]):
        for j in range(box[0][1], box[2][1]):
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
    used_names = []
    pyautogui.MINIMUM_DURATION = 2
    sl = 3
    time.sleep(sl+5)
    while True:
        blue_coor = find_blue_pixel_in_tc()
        print(blue_coor)
        time.sleep(sl)
        print("Нажимаем на строку")
        pyautogui.click(blue_coor)
        time.sleep(sl)
        print("Открываем название")
        pyautogui.hotkey('shiftleft', 'f6')
        time.sleep(sl)
        print("Копируем")
        pyautogui.hotkey('ctrlleft', 'c')
        time.sleep(sl)
        cb = get_cb()
        if "part" in cb and "mp4" in cb:
            print("Название", cb)
            if cb in used_names:
                print("Название уже переносили", cb)
                break
        else:
            break
        used_names.append(cb)
        print("Выходим")
        pyautogui.press("esc")
        time.sleep(sl)
        print("Перемещаем мышь на синюю")
        pyautogui.moveTo(blue_coor)
        time.sleep(sl)
        print("Зажимаем лкм")
        pyautogui.mouseDown(button='left')
        time.sleep(sl)
        print("Передвигаем в телегу")
        pyautogui.moveTo(find_box_tel())
        time.sleep(1)
        print("Чуть двигаем мышь")
        pyautogui.moveRel(0, 10)
        time.sleep(1)
        print("Передвигаем в телегу")
        pyautogui.moveTo(find_box_tel())
        time.sleep(sl)
        pyautogui.mouseUp(button='left')
        time.sleep(sl)
        print("Вставляем")
        pyautogui.hotkey('ctrlleft', 'v')
        time.sleep(sl)
        print("Нажимаем ентер")
        pyautogui.press('enter')
        time.sleep(sl)
        print("Альтабаемся")
        pyautogui.hotkey('alt', 'tab')
        time.sleep(sl)
        print("Снимаем выделение со старого файла")
        pyautogui.click(blue_coor,button='right')
        time.sleep(sl)
        print("Стрелка вниз")
        pyautogui.press('down')
        time.sleep(sl)