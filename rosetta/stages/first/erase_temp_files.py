import os

def erase_temp_files(row, complex_name):
    for file in os.listdir(row[0]):
        if not "_renumbered" in file:
            os.remove(os.path.join(row[0], file))