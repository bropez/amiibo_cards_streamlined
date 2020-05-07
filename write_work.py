import os


def replace_bin(bin_string):
    file_path = "Write_amiibo/Write_amiibo.ino"
    file_path2 = "Write_amiibo_temp/Write_amiibo_temp.ino"

    with open(file_path, "r") as file:
        data = file.read()
        data2 = data.replace("  byte dataBlock[]    = { replace me plz };", bin_string)

        with open(file_path2, "w") as file2:
            file2.write(data2)
    
    print("bin replacement complete.")


def delete_temp():
    try:
        os.remove("Write_amiibo_temp/Write_amiibo_temp.ino")
        print("deletion complete.")
    except OSError as e:
        print("An error hass occurred. error number: {}".format(e.errno))


delete_temp()