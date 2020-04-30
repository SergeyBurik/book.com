# coding:utf-8

import os
import zipfile


def zipdir(zipname, directory, path=None):
    if path:
        completeName = os.path.join(path, zipname)
    else:
        completeName = zipname


    # writing files to a zipfile
    zip = zipfile.ZipFile(f'{completeName}.zip', 'w')

    # Iterate over all the files in directory
    for folderName, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            # create complete filepath of file in directory
            filePath = os.path.join(folderName, filename)
            # Add file to zip
            zip.write(filePath, filePath.split('projects/')[1])
    return zip
