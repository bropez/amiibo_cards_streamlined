import serial
import os

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def upload_reader():
    """Uploads the required arduino sketch to the arduino.

    Args:
        No args

    Returns:
        No returns
    """
    COM_port = "COM5"
    FQBN = "arduino:avr:nano:cpu=atmega328old"

    print("Uploading DumpInfo.ino...")
    # os.system("arduino-cli compile --fqbn arduino:avr:uno DumpInfo")
    # os.system("arduino-cli upload -p {} --fqbn arduino:avr:uno DumpInfo".format(COM_port))
    os.system("arduino-cli compile --fqbn {} DumpInfo".format(FQBN))
    os.system("arduino-cli upload -p {} --fqbn {} DumpInfo".format(COM_port, FQBN))
    print("upload_reader Successfully uploaded.")
    print("")


def upload_servo_off():
    COM_port = "COM5"
    FQBN = "arduino:avr:nano:cpu=atmega328old"

    #os.system("arduino-cli compile --fqbn {} servo_off".format(FQBN))
    os.system("arduino-cli upload -p {} --fqbn {} servo_off".format(COM_port, FQBN))
    print("servo_off Successfully uploaded.")
    print("")


def write_data_to_file():
    """Writes the nfc card's data to a file

    Args:
        No args

    Returns:
        dump collection completed.: A confirmation string when the dump has been completed
        something went wrong.: The catch-all string if something went wrong
    """
    ser = serial.Serial('COM5', baudrate=9600, timeout=1)
    
    with open("amiibo_information/card_number.txt", "wb") as file:
        print("Open for reading. Please place card on sensor...")
        while True:
            arduino_data = ser.readline()
            file.write(arduino_data)

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
        os.remove("amiibo_information/card_number.txt")
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
    with open("amiibo_information/card_number.txt", "r") as file:
        for line in file:
            if "Card UID" in line:
                print("UID collection completed.")
                return line.replace("Card UID: ", "")
        
    print("problem here.")



def get_bin_replacement(uid, dump_file, key_file):
    """Gets the information to write to the card from the online dump editor

    Args:
        uid: The uid of the card that is being read/written to
        dump_file: The dump file that you would like to write onto the card
        key_file: The key file that you want to use for the card

    Returns:
        dump_output: The final information that will be written onto the card
    """
    print("Collecting bin to write...")
    options = Options()
    options.headless = True
    browser = Firefox(options=options)
    browser.get("https://games.kel.mn/amiibo/")

    uid_input = browser.find_element_by_id("UID")
    dump_file_btn = browser.find_element_by_id("fileToUpload")
    key_file_btn = browser.find_element_by_id("keyToUpload")

    uid_input.send_keys(uid)
    dump_file_btn.send_keys(dump_file)
    key_file_btn.send_keys(key_file)
    browser.find_element_by_id("saveForm").click()

    wait = WebDriverWait(browser, 10)
    element = wait.until(EC.element_to_be_clickable((By.ID, 'dialog')))

    dump_output = browser.find_element_by_tag_name("pre").text
    browser.quit()
    print("bin collected successfully.")
    return dump_output


def main(file_location):
    upload_reader()
    print(write_data_to_file())
    upload_servo_off()
    uid = get_uid()
    delete_card_number()
    print("You may remove your card now.")
    print("")

    current_dir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    output = get_bin_replacement(uid, 
        file_location,
        os.path.join(current_dir, 'key_try2.bin'))

    return output


if __name__ == "__main__":
    upload_reader()
    print("")
    print(write_data_to_file())
    uid = get_uid()
    delete_card_number()
    print("You may remove your card now.")
    print("")

    print("we did it")
