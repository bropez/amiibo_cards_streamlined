import serial
import os

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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
    # browser = Firefox()
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
    # print(dump_output)
    browser.quit()
    print("bin collected successfully.")
    return dump_output


if __name__ == "__main__":
    print(write_data_to_file())
    uid = get_uid()
    delete_card_number()
    print("You may remove your card now.")
    print("")


    print("we did it")
    # print(data)
