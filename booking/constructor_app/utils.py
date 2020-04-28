# coding:utf-8

import os
import zipfile


def get_all_file_paths(directory):
    file_paths = []

    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    return file_paths


def zipdir(zipname, directory, path=None):
    # path to folder which needs to be zipped

    # calling function to get all file paths in the directory
    file_paths = get_all_file_paths(directory)
    print(file_paths)

    if path:
        completeName = os.path.join(path, zipname)
    else:
        completeName = zipname

    # writing files to a zipfile
    with zipfile.ZipFile(f'{completeName}', 'w') as zip:
        # writing each file one by one
        for file in file_paths:
            print(file)
            zip.write(file)
        zip.close()
