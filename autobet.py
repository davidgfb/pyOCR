from numpy import array
from pytesseract import image_to_data, Output#image_to_string #Tesseract OCR v5
from cv2 import cvtColor, resize, INTER_AREA, imshow#opencv-python
from PIL.ImageGrab import grab
from win32gui import GetWindowRect,FindWindow,SetForegroundWindow # win32. #pywin32
from time import sleep

#************ recortes **************
#****** 1ªrios *******
def mitad_Izda(arr): return arr[:, :arr.shape[1] // 2] # 1a) 

def mitad_Dcha(arr): return arr[:, arr.shape[1] // 2:] # 1b) 
 
def mitad_Superior(arr): return arr[:arr.shape[0] // 2, :] # 2a)

def mitad_Inferior(arr): return arr[arr.shape[0] // 2:, :] # 2b) 
#**********************

#****** 2ªrios *******
def cuarto_Sup_Izdo(arr):return mitad_Superior(mitad_Izda(arr))#3a)

def cuarto_Sup_Dcho(arr):return mitad_Superior(mitad_Dcha(arr))#3b)

def cuarto_Inf_Izdo(arr):return mitad_Inferior(mitad_Izda(arr))#3c)
 
def cuarto_Inf_Dcho(arr):return mitad_Inferior(mitad_Dcha(arr))#3d)
#*********************
#*************************************

def busca_Palabra(p, texto_mm, d):
    res = None
    
    if p in texto_mm:
        indice = texto_mm.index(p)

        return d['left'][indice],d['top'][indice],\
            d['width'][indice],d['height'][indice],\
            d['conf'][indice] / 100

def main():
    dpi, hwnd = 1.25, FindWindow(None, 'Parsec')#1.25 CUIDADO la escala puede cambiar

    rect_ventana = GetWindowRect(hwnd)

    rect=tuple(int(x*dpi)for x in rect_ventana)#MUY IMPORTANTE escalar dpi

    SetForegroundWindow(hwnd)
    sleep(1e-3)

    arr, escala = cvtColor(array(grab(bbox =rect)),6),0.5#captura orig

    arr = cuarto_Inf_Dcho(arr)  

    dd = tuple(int(x * escala) for x in arr.shape)[::-1] #dimensiones

    redimension=resize(arr, dd, interpolation = INTER_AREA)#captura

    imshow(None, redimension)

    #tesstr = image_to_string(arr, lang = 'spa')#pasamos la cap recortada
    d = image_to_data(arr, lang = 'spa', output_type = Output.DICT)

    texto_mm = tuple(p.lower() for p in d['text']) # a_Minusculas

    palabra = 'apostar'
  
    x, y, ancho, alto, confianza = busca_Palabra(palabra, texto_mm, d)     

    print(f'''palabra = \'{palabra}\' en x, y = ({x}, {y}),
        ancho, alto = ({ancho}, {alto}),
        confianza = {confianza}''')

    #'''
    #*********** transformacion *************
    win_x, win_y, win_x1, win_y2 = rect_ventana

    # 2. Calcular el tamaño de la transmisión dentro de Parsec
    # (Asumiendo que el cuarto inferior derecho empieza a la mitad)
    win_ancho, win_alto = win_x1 - win_x, win_y2 - win_y

    offset_recorte_x, offset_recorte_y = win_ancho // 2, win_alto // 2


    # --- TRANSFORMACIÓN FINAL ---
    # Sumamos: Posición Ventana + Inicio Recorte + Centro del Texto detectado
    final_pos = win_x + offset_recorte_x + x + (ancho // 2),\
        win_y + offset_recorte_y + y + (alto // 2)

    #from pydirectinput import moveTo#pyautogui NO funciona sobre Parsec

    from pyautogui import moveTo, FAILSAFE 

    FAILSAFE = False #pyautogui

    moveTo(*final_pos, duration = 3)#steps NO existe en pydirectinput



    print(final_pos)

main()

'''
from threading import Thread

#def mueve_Raton(pos): moveTo(*pos, duration = 3)

#hilo = Thread(target = mueve_Raton, args = (final_pos,))


hilo = Thread(target = main)

hilo.start()
#moveTo(final_x, final_y, duration = 3)#*final_pos
'''


#************ PROBADOR recortes **************
#****** 1arios *******
#arr = mitad_Izda(arr) # 1a) 

#arr = mitad_Dcha(arr) # 1b)

#arr = mitad_Superior(arr) # 2a) 

#arr = mitad_Inferior(arr) # 2b)
#*********************

#****** 2arios *******
#arr = cuarto_Sup_Izdo(arr) 

#arr = cuarto_Sup_Dcho(arr) 

#arr = cuarto_Inf_Izdo(arr)

#arr = cuarto_Inf_Dcho(arr) 
#**********************
#**********************************************

'''
def callback(hwnd, extra):
    topwindows.append(GetWindowText(hwnd).lower()) 

def index_containing_substring(the_list, substring):
    res = 0
    
    for pos in range(len(the_list)):        
        if substring in the_list[pos]:
            res = pos
            
    return res
'''

