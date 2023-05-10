import os
import configparser
import serial
import serial.tools.list_ports
import time
from barcode import EAN13
from barcode import Code39
from barcode.writer import ImageWriter
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import re
import random

'''
Retrieving the weight from Metler Toledo scales, which are connected with a serial port. 
The app displays the weight in Barcode39 format, allowing operators to easily input the weight data into the SAP 
Business by Design interface during the production make phase. The interface is developed in Python 3.8.
To create the executable, use pyinstaller in a virtual environment with the packages listed in the requirements.txt file.

1.Open a terminal and go to the directory where you want to create the virtual environment.
2.Use the following command to create a new virtual environment:
    python -m venv name_of_your_virtual_environment
    Where "name_of_your_virtual_environment" is the name you want to assign to your virtual environment.

3.Visual Studio will ask if you want to consider this as an environment, tell it yes.
4.Activate your virtual environment using the following command:
    source name_of_your_virtual_environment/Scripts/activate
Where "name_of_your_virtual_environment" is the name you chose for your virtual environment.

Now you are inside your virtual environment and can install the necessary libraries using the pip command, for example:
    pip install -r requirements.txt

Then go into the src folder and run this ti create the executable:
    pyinstaller --onefile --name=bilancia_3.0 balance_2.0.py

This will create a dist folder with the executable inside.

To use the app, you can create a new folder and 
    a- copy the executable inside. 
    b- add config.properties file in the same folder as the executable
    c- add the dejaVuSans.ttf font in the font folder inside the folder
    d- add the barcode_peso_bilancia.png image in the same folder
    e- copy the libusb-1.0.dll file in the c:\windows\system32 folder

'''

#take properties form config.properties 
config = configparser.ConfigParser()
config.read('config.properties')

def elenca_porte_seriali():
    '''
    Returns a list of the serial ports available on the system
    '''
    return [porta.device for porta in serial.tools.list_ports.comports()]

def esegui_aggiorna_peso(n, millisec=400):
    '''
    Recursively calls itself to update the weight
    '''
    if n > 0:
        aggiorna_peso()
        print(f"Aggiorna il peso .... {n}")
        root.after(millisec, esegui_aggiorna_peso, n - 1)#attende 400 millisecondi

def aggiorna_peso():
    '''
    Creates the barcode in 13 or 39 format 
    depending on the configuration file and displays it
    in the GUI
    '''
    global label_peso, img_tk, img
    posizione_file= os.path.join(os.getcwd(), 'barcode_peso_bilancia.png')  
    porta_selezionata = combo_porte.get()
    try:

        #if test mode is enabled, the weight is simulated 
        simula_peso = config.getboolean('debug', 'simula_peso')
        if not simula_peso:
            peso, unita = leggi_peso(porta_selezionata)
        else:
            peso, unita =  leggipesotest()

        label_peso.config(text=f"Peso rilevato: {peso} {unita}")

        #create barcode
        codifica_ean = config.getint('barcode', 'codifica_ean') 
        if codifica_ean == 13:
            crea_barcode13(peso)
        else:
            crea_barcode39(peso)
        
        img = Image.open(posizione_file)
        
        resize_image = config.getboolean('barcode', 'resize_barcode')
        if(resize_image):
            fixed_width = config.getint('barcode', 'fixed_width') 
            fixed_height = config.getint('barcode', 'fixed_height') 
            img_resized = img.resize((fixed_width, fixed_height), Image.ANTIALIAS)
            img_tk = ImageTk.PhotoImage(img_resized)
        else:
            img_tk = ImageTk.PhotoImage(img)

        label_img.config(image=img_tk)
        label_img.pack(padx=20, pady=2)

    
    except Exception as e:
        print(f"Errore nella lettura del peso: {e}")#print error on console
        label_peso.config(text=f"Errore nella lettura del peso. Peso non rilevabile.")



def leggi_peso(porta_seriale, baud_rate=9600, timeout=1):
    '''
    To read the weight from the Toledo scale, it is necessary to send the command for reading.
    The byte string b'S\r\n' contains the ASCII characters corresponding to the letter "S" followed 
    by a carriage return (\r) and a line feed (\n) character. In this case, the letter "S" represents 
    the specific command that is sent to the device connected to the serial port.
    S: Send stable weight value.
    
    Other requirements on the scale : 
        the scale has to be set to “Dialog” Mode. 
        Verify that the baud rate is set to 9600, parity 8, none, Handshake XonXoff.

    '''
    with serial.Serial(porta_seriale, baud_rate, timeout=timeout) as ser:

        comando_seriale = os.path.join(os.getcwd(),'balance', 'comando_peso')
        print(f"SERIALE - comando :", comando_seriale)
        time.sleep(2)

        ser.write(b'S\r\n')
        raw_str = ser.readline().decode('ascii').strip()
        print(f"SERIALE - lettura :", raw_str)        

        #regex to extract the weight
        peso_val = re.search(r"[-+]?\d*\.\d+|\d+", raw_str)
        unita_di_misura = None

        if peso_val:

            peso_raw = peso_val.group(0)
            print(f"SERIALE - Peso decodifcato :",peso_raw)
            last_space_index = raw_str.rfind(' ')
            unita_di_misura = raw_str[last_space_index + 1:]
            
        else:
            peso_raw = None

        try:
            #round to 1 decimal
            #abs to remove the sign if the weight is oscillating around 0
            peso = round(abs(float(peso_raw)),1) 
        except Exception as e:
            #it can be an error if the weight is not a number
            print(f"SERIALE - Errore nella lettura, peso letto  : {peso_raw} \n {e}")
            peso = None

        return peso , unita_di_misura 


def crea_barcode13(peso, nome_file='barcode_peso_bilancia'):
    '''
    Barcode 13: is only for numbers, it is the most used in the world
    '''
    
    barcode_num  = f"{int(peso*100):012}"
    image_writer = ImageWriter()

    image_writer.font_path = os.path.join(os.getcwd(),'fonts', 'DejaVuSansMono.ttf')
    ean = EAN13(barcode_num, writer=image_writer,no_checksum=False) # aggiunge .png

    posizione_file= os.path.join(os.getcwd(), nome_file)  
    print(f"Barcode 13 salvato in : {posizione_file}")
    ean.save(posizione_file)
    print(f"Barcode 13 correttamente salvato in : {posizione_file}")


def crea_barcode39(peso, nome_file='barcode_peso_bilancia'):
    '''
    Barcode 39: is alphanumeric, it is used in most of the industrial applications
    In this case, this is the default barcode used by the Toledo scale

    Options used in this example are from the documentation:
    https://python-barcode.readthedocs.io/en/stable/writers.html#common-writer-options
    
    '''
    
    barcode_val  = str(peso)

    image_writer = ImageWriter()

    #set the font path to the font file to use for the text. 
    #This is NECESSARY to avoid the error: "RuntimeError: Failed to create font object"
    #The font file is in the fonts folder in the same directory of the script
    image_writer.font_path = os.path.join(os.getcwd(),'fonts', 'DejaVuSansMono.ttf')

    #Set the DPI as int to calculate the image size in pixel. This value is used for all mm to px calculations. Defaults to 300
    image_writer.dpi = config.getint('barcode', 'dpi')

    #ean = barcode.get('code39', barcode_val, writer=image_writer,add_checksum=False)
    #no checksum for the barcode 39 so that the barcode is showing correctly only  the numbers
    ean =  Code39(barcode_val, writer=image_writer, add_checksum=False)

    posizione_file = os.path.join(os.getcwd(), f"{nome_file}")

    #Options used in this example are from the documentation
    #text_distance: The distance between the barcode and the text in pixel. Defaults to 5
    #module_width: The width of the smallest bar in pixel. Defaults to 0.2
    #module_height: The height of the barcode in pixel. Defaults to 15.0
    text_distance = config.getint('barcode', 'text_distance')
    module_width = config.getfloat('barcode', 'module_width')
    module_height = config.getfloat('barcode', 'module_height')
  
    ean.save(posizione_file, options={"text_distance": text_distance, "module_width" : module_width, "module_height": module_height})

    print(f"Barcode 39 correttamente salvato in : {posizione_file}")




#INIT_FINESTRA_______________________________________________________________________________________________________________________
def mostra_finestra():
    '''
    This function creates the window consolle from which 
    the user can interact with the program 
    '''
    global combo_porte, label_peso, label_img, root

    root = tk.Tk()
    root.title("Peso e Codice a Barre")

    # Positioning the window at the bottom-left corner
    # for easy access 
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = config.getint('window', 'window_width')  # Replace with your desired window width
    window_height = config.getint('window', 'window_height')  # Replace with your desired window height
    font1 = config.getint('window', 'font1')
    from_bottom_px = config.getint('window', 'from_bottom_px')


    x_pos = screen_width - window_width
    y_pos = screen_height - window_height - from_bottom_px
    root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
    
    frame_top = tk.Frame(root)
    frame_top.pack(padx=20, pady=2)

    tk.Label(frame_top, text="Seleziona la porta:", font=("Arial", 10)).pack(side=tk.LEFT)

    combo_porte = ttk.Combobox(frame_top, values=elenca_porte_seriali(), font=("Arial", font1))
    combo_porte.pack(side=tk.LEFT)
    combo_porte.set(elenca_porte_seriali()[0] if elenca_porte_seriali() else "")

    #parametri per aggiornare il peso
    n_iter = config.getint('aggiorna', 'numero_iterazioni')
    millisec_iter = config.getint('aggiorna', 'millisecondi_iterazioni')
    btn_aggiorna = tk.Button(frame_top, text="Pesa", command=lambda: esegui_aggiorna_peso(n_iter, millisec_iter), font=("Arial", font1))
    btn_aggiorna.pack(side=tk.RIGHT, padx=2)

    label_peso = tk.Label(root, text="Peso rilevato: -- ", font=("Arial", font1))
    label_peso.pack(padx=20, pady=2)

    label_img = tk.Label(root)
    label_img.pack(padx=20, pady=2)
    
    
    btn_exit = tk.Button(root, text="Esci", command=root.destroy, font=("Arial", font1))
    btn_exit.pack(padx=20, pady=2)

    root.mainloop()

#DEBUG__________________________________________________________________________________________
def genera_peso():#non serve
    peso = round(random.uniform(1, 200), 2)
    return peso

def leggipesotest():
    return 10,"bb"

def load_config():
    config = configparser.ConfigParser()
    config_file_path = os.path.join(os.getcwd(), 'config.properties')
    print(config_file_path)
    config.read(config_file_path)
    for section in config.sections():
        print(f"[{section}]")
        for option in config.options(section):
            value = config.get(section, option)
            print(f"{option} = {value}")
        print()    
    return config


if __name__ == "__main__":
    load_config()
    mostra_finestra()

