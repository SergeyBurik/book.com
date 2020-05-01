# coding:utf-8


import os
import zipfile
import os, shutil


def get_all_file_paths(directory):
    file_paths = []

    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    return file_paths


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def zipdir(zipname, directory, path=None):
    # path to folder which needs to be zipped

    # calling function to get all file paths in the directory
    file_paths = get_all_file_paths(directory)

    if path:
        completeName = os.path.join(path, zipname)
    else:
        completeName = zipname

    # writing files to a zipfile
    with zipfile.ZipFile(f'{completeName}', 'w') as zip:
        # writing each file one by one
        for file in file_paths:
            print(file)
            print(file.split('preparing_projects/')[1])
            zip.write(file, file.split('preparing_projects/')[1])
        zip.close()
