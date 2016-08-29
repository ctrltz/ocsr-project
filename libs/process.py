from os import path, mkdir, chdir, listdir
import fnmatch
from joblib import Parallel, delayed
import shutil
import subprocess

import config
import correct
import utils


def launch():
    found_files = []            # List of found files
    diff = dict()               # List of results
    counter = 0                 # Current file number

    # Find all files
    chdir(config.dbDir)
    for f in listdir('.'):
        if fnmatch.fnmatch(f, config.fPattern):
            found_files.append(f)
            diff.setdefault(f, 0)

    if len(found_files) > 0:
        if config.debug:
            utils.log('List of found files: {}', found_files)
        if not path.exists(config.outDir):
            mkdir(config.outDir)

        Parallel(n_jobs=-2)(delayed(process_image)(found_file) for found_file in found_files)
    else:
        utils.log('No files matching input pattern were found.')


def process_image(filename):
    directory = path.join(config.outDir, path.splitext(filename)[0])
    if not path.exists(directory):
        mkdir(directory)
    shutil.copy(filename, directory)
    correct.correct(filename, directory)