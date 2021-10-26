from numpy import array
from pytesseract import image_to_string
from cv2 import cvtColor, imshow
from PIL.ImageGrab import grab
from win32.win32gui import EnumWindows, GetWindowRect,\
     GetWindowText, FindWindow, SetForegroundWindow, ShowWindow,\
     GetWindowPlacement
from time import sleep

def callback(hwnd, extra):
    topwindows.append(GetWindowText(hwnd).lower()) 

def index_containing_substring(the_list, substring):
    res = 0
    
    for pos in range(len(the_list)):        
        if substring in the_list[pos]:
            res = pos
            
    return res

topwindows = []

EnumWindows(callback, topwindows)

proceso = "chrome"

if any(proceso in mystring for mystring in topwindows):
    indice = index_containing_substring(topwindows, proceso)
    hwnd = FindWindow(None, topwindows[indice])

    if GetWindowPlacement(hwnd)[1] == 2: # estaMinimizada
        ShowWindow(hwnd, 1)

    rect = GetWindowRect(hwnd)[:4]       

    SetForegroundWindow(hwnd)
    sleep(0.2) #while not GetWindowPlacement(hwnd)[1] == 1:

    a = cvtColor(array(grab(bbox = rect)), 6) #a.show()
    imshow(None, a) 

    tesstr = image_to_string(a, lang ='eng')

    print(tesstr)

