import os

dir_path = os.path.dirname(os.path.realpath(__file__))
directory = os.fsencode(dir_path)
    
for file in os.listdir(directory):
    filename = os.fsdecode(file)

    if filename[-3:] != ".py":
        os.rename(os.path.join(dir_path, filename), os.path.join(dir_path, str(int(filename[6:9])) + ".png"))