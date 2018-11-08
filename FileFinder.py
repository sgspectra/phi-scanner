import os


def findfiles(dir):
    output = open('./lib/textFiles.txt', 'a+')
    for entry in os.scandir(dir):
        if entry.is_dir(follow_symlinks=False):
            findfiles(entry.path)
        else:
            print(entry.path)
            output.write(entry.path)
            output.write('\n')
    output.close()


print("Please enter the directory you wish to find files in:")
path = input()
findfiles(path)


