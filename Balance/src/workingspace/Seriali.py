

import serial.tools.list_ports

# Ottieni tutte le porte seriali disponibili sul sistema
port_list = list(serial.tools.list_ports.comports())

# Stampa tutte le porte seriali trovate
for port in port_list:
    print("Porta Seriale: ", port.device)
    print("Nome del produttore: ", port.manufacturer)
    print("Numero del prodotto: ", port.product)
    print("Descrizione: ", port.description)
    print("Tipo della porta: ", port.interface)
    print("Numero della porta: ", port.location)
    print("ID del prodotto: ", port.pid)
    print("ID del venditore: ", port.vid)
    print("Altre informazioni: ", port.hwid)
    print(" ")