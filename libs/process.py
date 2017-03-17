from os import path, mkdir, chdir, listdir, removedirs
import fnmatch
from joblib import Parallel, delayed
import shutil

import config
import correct
import utils


def launch():
    found_files = []            # List of found files
    diff = dict()               # List of results

    # Find all files
    chdir(config.dbDir)
    for f in listdir('.'):
        if fnmatch.fnmatch(f, config.fPattern):
            found_files.append(f)
            diff.setdefault(f, 0)

    if len(found_files) > 0:
        if config.debug:
            utils.log('List of found files: {}', found_files)
        if not path.exists(config.resDir):
            mkdir(config.resDir)
        if not path.exists(config.tmpDir):
            mkdir(config.tmpDir)
        if not path.exists(config.inDir):
            mkdir(config.inDir)
        if not path.exists(config.outDir):
            mkdir(config.outDir)

        # Parallel(n_jobs=-2)(delayed(process_image)(found_file) for found_file in found_files)
        for found_file in found_files:
            process_image(path.normpath(path.join(config.dbDir, found_file)))
    else:
        utils.log('No files matching input pattern were found.')

    removedirs(config.tmpDir)


def process_image(filename):
    shutil.copy(filename, config.tmpDir)
    correct.correct(filename)