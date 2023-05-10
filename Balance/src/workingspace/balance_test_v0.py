import serial
import usb.core
import usb.util
import time
from barcode import EAN13
from barcode.writer import ImageWriter
from PIL import Image, ImageTk
import tkinter as tk


def leggi_peso_seriale(porta_seriale, baud_rate=9600, timeout=1):
    with serial.Serial(porta_seriale, baud_rate, timeout=timeout) as ser:
        time.sleep(2)
        ser.write(b'\x05')
        peso_raw = ser.readline().decode('ascii').strip()
        peso_raw = 12
        return float(peso_raw)

def leggi_peso_usb(vendor_id, product_id):
    dev = usb.core.find(idVendor=vendor_id, idProduct=product_id)

    if dev is None:
        raise ValueError('Bilancia non trovata')

    dev.reset()

    try:
        dev.detach_kernel_driver(0)
    except Exception as e:
        pass

    dev.set_configuration()

    cfg = dev.get_active_configuration()
    intf = cfg[(0, 0)]

    ep_in = usb.util.find_descriptor(intf, custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)
    ep_out = usb.util.find_descriptor(intf, custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)

    peso_raw = dev.read(ep_in.bEndpointAddress, ep_in.wMaxPacketSize)
    peso = float(peso_raw.decode('ascii').strip())

    usb.util.dispose_resources(dev)

    return peso

def crea_barcode(peso, nome_file='barcode.png'):
    barcode_num = f"{int(peso*100):012}"
    ean = EAN13(barcode_num, writer=ImageWriter())
    ean.save(nome_file)
    
    
def mostra_finestra(peso, nome_file='barcode.png.png'):
    root = tk.Tk()
    root.title("Peso e Codice a Barre")

    img = Image.open(nome_file)
    img_tk = ImageTk.PhotoImage(img)

    label_img = tk.Label(root, image=img_tk)
    label_img.pack(padx=20, pady=20)

    label_peso = tk.Label(root, text=f"Peso rilevato: {peso} kg", font=("Arial", 16))
    label_peso.pack(padx=20, pady=10)

    btn_exit = tk.Button(root, text="Esci", command=root.destroy, font=("Arial", 12))
    btn_exit.pack(padx=20, pady=20)

    root.mainloop()

if __name__ == "__main__":
    porta_seriale = 'COM2'
    peso_seriale = leggi_peso_seriale(porta_seriale)
    peso_usb = leggi_peso_seriale(porta_seriale)
    
    print(f"Peso rilevato: {peso_seriale} kg")
    crea_barcode(peso_seriale)
    mostra_finestra(peso_seriale)