# Retrieving weight from Metler Toledo scales 

This application is designed to retrieve weight data from Metler Toledo scales that are connected via a serial port. The weight data is then displayed in Barcode39 format, making it easy for operators to input the weight information into the SAP Business by Design interface using a barcode reader during the production phase.

Developed using Python 3.8 and ChatGPT 4 this app is a user-friendly and efficient tool for streamlining the data input process in production. Its ability to retrieve weight data from the scales and display it in barcode format saves valuable time and reduces the risk of data entry errors.

To create the executable, use `pyinstaller` in a virtual environment with the packages listed in the `src/requirements.txt` file.

1. Open a terminal and go to the directory where you want to create the virtual environment.
2. Use the following command to create a new virtual environment:

   ```
   python -m venv name_of_your_virtual_environment
   ```

   Where "name_of_your_virtual_environment" is the name you want to assign to your virtual environment.

3. Visual Studio will ask if you want to consider this as an environment, tell it yes.
4. Activate your virtual environment using the following command:

   ```
   source name_of_your_virtual_environment/Scripts/activate
   ```

   Where "name_of_your_virtual_environment" is the name you chose for your virtual environment.

Now you are inside your virtual environment and can install the necessary libraries using the `pip` command, for example:

```
pip install -r requirements.txt
```

Then go into the `src` folder and run this command to create the executable:

```
pyinstaller --onefile --name=bilancia_3.0 balance_2.0.py
```

This will create a `dist` folder with the executable inside.

To use the app, follow these steps:

1. Create a new folder.
2. Copy the executable inside the folder.
3. Add a `config.properties` file in the same folder as the executable.
4. Add the `dejaVuSans.ttf` font in the font folder inside the folder.
5. Add the `barcode_peso_bilancia.png` image in the same folder.
6. Copy the `libusb-1.0.dll` file in the `c:\windows\system32` folder.
