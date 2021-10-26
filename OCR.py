from win32.win32gui import EnumWindows, GetWindowRect,\
     GetWindowText, FindWindow, SetForegroundWindow, ShowWindow,\
     GetWindowPlacement
from PIL.ImageGrab import grab
from time import sleep

topwindows = []

def callback(hwnd, extra):
    topwindows.append(GetWindowText(hwnd).lower()) 

def index_containing_substring(the_list, substring):
    for i, s in enumerate(the_list):
        if substring in s:
              return i

EnumWindows(callback, topwindows)

if any("chrome" in mystring for mystring in topwindows):
    indice = index_containing_substring(topwindows, "chrome")
    hwnd = FindWindow(None, topwindows[indice])

    if GetWindowPlacement(hwnd)[1] == 2: # estaMinimizada
        ShowWindow(hwnd, 1)

    rect = GetWindowRect(hwnd)[:4]       

    SetForegroundWindow(hwnd)
    sleep(0.2)

    a = grab(bbox = rect)
    a.show()
    

