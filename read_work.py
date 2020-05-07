import serial
import os


def write_data_to_file():
    """Writes the nfc card's data to a file

    Args:
        No args

    Returns:
        dump collection completed.: A confirmation string when the dump has been completed
        something went wrong.: The catch-all string if something went wrong
    """
    ser = serial.Serial('COM3', baudrate=9600, timeout=1)
    
    with open("Write_amiibo_temp/card_number.txt", "wb") as file:
        print("Open for reading. Please place card on sensor...")
        while True:
            arduino_data = ser.readline()
            file.write(arduino_data)
            # print(arduino_data)

            if str.encode("Dump finished!") in arduino_data:
                return "dump collection completed."

    return "something went wrong."



def delete_card_number():
    """Deletes the file that holds the nfc card information

    Args:
        No args

    Returns:
        No Returns
    """
    try:
        os.remove("Write_amiibo_temp/card_number.txt")
        print("deletion complete.")
    except OSError as e:
        print("An error has occurred. error number: {}".format(e.errno))



def get_uid():
    """Gets the UID of the nfc card just read from a file

    Args:
        No args

    Returns:
        line.replace("Card UID: ", ""): The UID in string form if it is formatted correctly
        problem here.: The catch-all if the UID is not correctly formatted in the file
    """
    with open("Write_amiibo_temp/card_number.txt", "r") as file:
        for line in file:
            if "Card UID" in line:
                print("UID collection completed.")
                return line.replace("Card UID: ", "")
        
    print("problem here.")



# TODO: get bin from amiibo converter website
print(write_data_to_file())
uid = get_uid()
print("UID: {}".format(uid))
delete_card_number()
print("we did it")
# print(data)
