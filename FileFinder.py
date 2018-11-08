import os


def findfiles(dir):
    for entry in os.scandir(dir):
        if entry.is_dir(follow_symlinks=False):
            findfiles(entry.path)
        else:
            print(entry.path)


print("Please enter the directory you wish to find files in:")
path = input()
findfiles(path)


