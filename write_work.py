import os
import sys

import serial


def upload_writer():
    """Uploads the required arduino sketch to the arduino.

    Args:
        No args

    Returns:
        No returns
    """
    COM_port = "COM5"
    FQBN = "arduino:avr:nano:cpu=atmega328old"

    print("Uploading Final_amiibo.ino...")
    # os.system("arduino-cli compile --fqbn arduino:avr:uno Final_amiibo")
    os.system("arduino-cli compile --fqbn {} Final_amiibo".format(FQBN))
    # os.system("arduino-cli upload -p {} --fqbn arduino:avr:uno Final_amiibo".format(COM_port))
    os.system("arduino-cli upload -p {} --fqbn {} Final_amiibo".format(COM_port, FQBN))
    print("upload_writer Successfully uploaded.")
    print("")


def upload_servo_off():
    COM_port = "COM5"
    FQBN = "arduino:avr:nano:cpu=atmega328old"
    
    # os.system("arduino-cli compile --fqbn {} servo_off".format(FQBN))
    os.system("arduino-cli upload -p {} --fqbn {} servo_off".format(COM_port, FQBN))
    print("upload_servo Successfully uploaded.")
    print("")


def replace_bin(bin_string):
    """Places correct .bin in file

    Args:
        bin_string: The string that needs to be placed in file
    Returns:
        No returns
    """
    file_path = "Write_amiibo_template/Write_amiibo_template.ino"
    file_path2 = "Final_amiibo/Final_amiibo.ino"

    print("replaceing bin...")
    with open(file_path, "r") as file:
        data = file.read()
        bin_string = "  byte dataBlock[]    = { " + bin_string + " }; "
        #bin_string = "  byte dataBlock[]    = { " + bin_string + " "
        data2 = data.replace("  byte dataBlock[]    = { replace me plz };", bin_string)

        with open(file_path2, "w") as file2:
            file2.write(data2)
    
    print("bin replacement complete.")


def write_to_card():
    """Writes the nfc card's data to a file

    Args:
        No args

    Returns:
        dump collection completed.: A confirmation string when the dump has been completed
        something went wrong.: The catch-all string if something went wrong
    """
    ser = serial.Serial('COM5', baudrate=9600, timeout=1)

    print("Open for writing. Please place card on sensor...")
    writing = 0
    while True:
        arduino_data = ser.readline()
        if str.encode("Writing data into page") in arduino_data:
            writing = 1

        if writing:
            sys.stdout.write("\rWriting to card...")
            sys.stdout.flush()
        
        if str.encode("Write process finished!") in arduino_data:
            return "dump writing completed."
    return "something went wrong."


def delete_temp():
    """Deletes the temporary file that was created

    Args:
        No args
    Returns:
        No returns
    """
    try:
        os.remove("Final_amiibo/Final_amiibo.ino")
        print("deletion complete.")
    except OSError as e:
        print("An error has occurred. error number: {}".format(e.errno))


def safe_mode():
    """Changes the arduino into a safer mode

    Args:
        No args
    Returns:
        No returns
    """
    COM_port = "COM5"
    FQBN = "arduino:avr:nano:cpu=atmega328old"

    # os.system("arduino-cli compile --fqbn arduino:avr:uno servo_off")
    # os.system("arduino-cli upload -p {} --fqbn arduino:avr:uno servo_off".format(COM_port))
    os.system("arduino-cli compile --fqbn {} servo_manual_reset".format(FQBN))
    os.system("arduino-cli upload -p {} --fqbn {} servo_manual_reset".format(COM_port, FQBN))


def main(replacement_bin):
    replace_bin(replacement_bin)
    upload_writer()
    write_to_card_output = write_to_card()
    print("")
    print(write_to_card_output)
    #delete_temp()
    print("You may remove your card.")
    print("")
    upload_servo_off()



if __name__ == "__main__":
    main("replacement bin.")
