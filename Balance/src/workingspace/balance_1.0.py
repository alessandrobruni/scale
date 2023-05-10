import os
import serial
import serial.tools.list_ports
import time
from barcode import EAN13
from serial import Serial
from barcode.writer import ImageWriter
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import re


import random

def genera_peso():
    peso = round(random.uniform(1, 200), 2)
    return peso


def leggi_peso(porta_seriale, baud_rate=9600, timeout=1):
    with serial.Serial(porta_seriale, baud_rate, timeout=timeout) as ser:
        time.sleep(2)
        ser.write(b'\x05')
        raw_str = ser.readline().decode('ascii').strip()
        peso_val = re.search(r"[-+]?\d*\.\d+|\d+", raw_str)
        unita_di_misura = None

        if peso_val:

            peso_raw = peso_val.group(0)
            last_space_index = raw_str.rfind(' ')
            unita_di_misura = peso_raw[last_space_index + 1:]
            
        else:
            peso_raw = None

        return abs(float(peso_raw)), unita_di_misura #preso abs perchè se non c'è nulla il peso puo oscillare tra positivo e negativo


def crea_barcode(peso, nome_file='barcode_peso_bilancia'):
    
    barcode_num  = f"{int(peso*100):012}"
    image_writer = ImageWriter()
    #image_writer.font_path = os.path.join(os.getcwd(),'fonts', 'DejaVuSansMono.ttf')
    ean = EAN13(barcode_num, writer=image_writer) # aggiunge .png
    #ean = EAN13(barcode_num, writer=ImageWriter()) # aggiunge .png
    posizione_file= os.path.join(os.getcwd(), nome_file)  
    print(f"Barcode salvato in : {posizione_file}")
    ean.save(posizione_file)
    print(f"Barcode correttamente salvato in : {posizione_file}")


def elenca_porte_seriali():
    return [porta.device for porta in serial.tools.list_ports.comports()]


def aggiorna_peso():
    global label_peso, img_tk
    posizione_file= os.path.join(os.getcwd(), 'barcode_peso_bilancia.png')  
    porta_selezionata = combo_porte.get()
    try:
        
        peso, unita = leggi_peso(porta_selezionata)
        label_peso.config(text=f"Peso rilevato: {peso} {unita}")
        crea_barcode(peso)
        img = Image.open(posizione_file)
        img_tk = ImageTk.PhotoImage(img)
        label_img.config(image=img_tk)       
        label_img.pack(padx=20, pady=20)
    
    except Exception as e:
        print(e)
        peso  = genera_peso()
        label_peso.config(text=f"Errore nella lettura del peso\nPeso simulato : \n {e}\n\n Peso similato : \n{peso} kg")
        crea_barcode(peso)
        img = Image.open(posizione_file)
        img_tk = ImageTk.PhotoImage(img)
        label_img.config(image=img_tk)
        label_img.pack(padx=20, pady=20)


def mostra_finestra():
    global combo_porte, label_peso, label_img
    root = tk.Tk()
    root.title("Peso e Codice a Barre")

    frame_top = tk.Frame(root)
    frame_top.pack(padx=20, pady=10)

    tk.Label(frame_top, text="Seleziona la porta COM:", font=("Arial", 12)).pack(side=tk.LEFT)

    combo_porte = ttk.Combobox(frame_top, values=elenca_porte_seriali(), font=("Arial", 12))
    combo_porte.pack(side=tk.LEFT)
    combo_porte.set(elenca_porte_seriali()[0] if elenca_porte_seriali() else "")

    btn_aggiorna = tk.Button(frame_top, text="Aggiorna peso", command=aggiorna_peso, font=("Arial", 12))
    btn_aggiorna.pack(side=tk.LEFT, padx=10)

    label_peso = tk.Label(root, text="Peso rilevato: -- kg", font=("Arial", 16))
    label_peso.pack(padx=20, pady=10)

    label_img = tk.Label(root)
    label_img.pack(padx=20, pady=10)
    
    
    btn_exit = tk.Button(root, text="Esci", command=root.destroy, font=("Arial", 12))
    btn_exit.pack(padx=20, pady=20)

    root.mainloop()




if __name__ == "__main__":
    mostra_finestra()

