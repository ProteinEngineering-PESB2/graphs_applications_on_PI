import shutil

def create_file(file_name, content, path):
    file = open(file_name, "w")
    file.write(content)
    file.close()
    shutil.move(file_name, path)