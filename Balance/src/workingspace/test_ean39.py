import os
import barcode
from barcode.writer import ImageWriter

def crea_barcode39(peso, nome_file='barcode_peso_bilancia'):
    
    barcode_val  = "2023009155"

    ean = barcode.get('code39', barcode_val)
    
    # Imposta la larghezza degli spazi bianchi nel codice a barre
    image_writer = ImageWriter()
    image_writer.module_width = 1

    #image_writer.font_path = os.path.join(os.getcwd(),'fonts', 'DejaVuSansMono.ttf')

    posizione_file= os.path.join(os.getcwd(), f"{nome_file}.png")

    # Salva l'immagine del codice a barre direttamente nel file
    ean.save(posizione_file, image_writer)

crea_barcode39("123.45", "barcode_peso_bilancia")