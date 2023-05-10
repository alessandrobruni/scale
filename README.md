# Retrieving the weight from Metler Toledo scales 

This application retrieves the weight from Metler Toledo scales that are connected with a serial port. The weight is displayed in Barcode39 format, allowing operators to easily input the weight data into the SAP Business by Design interface during the production make phase. The interface is developed in Python 3.8.

To create the executable, use `pyinstaller` in a virtual environment with the packages listed in the `requirements.txt` file.

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
