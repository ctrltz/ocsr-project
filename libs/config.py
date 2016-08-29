#!/usr/bin/python
#
# This script contains:
#  - common functions used to output debug & error information
#  - all widely used variables (file paths, useful parameters, etc)

RESULTS_RELATIVE_PATH = './res'
DATA_RELATIVE_PATH = './data'

# ------------ Directories ----------------------------
prjDir = ''                  # project's working directory
dbDir = ''                   # directory with the current database
resDir = ''                  # directory with all results
outDir = ''                  # directory with results for current job
tmpDir = ''                  # directory with temporary files for processing
goodDir = ''                 # directory with SMILEs that are suggested to be good
allDir = ''                  # directory with all SMILEs obtained

# --------------- Files ----------------------------
spelling = ''                # location of the 'spelling.txt' file
superatom = ''               # location of the 'superatom.txt' file
spelling_noh = ''            # location of the 'spelling.noh.txt' file
superatom_noh = ''           # location of the 'superatom.noh.txt' file

# --------------- Flags ----------------------------
debug = 0                    # turning on (1) / off (0) debug mode
restore = 0                  # restoring (if 1) initial 'spelling.txt' file
auto = 1                     # correct automatically (if 1)
noh = 0                      # use 'spelling.noh.txt' and 'superatom.noh.txt'
manual = 0                   # number of images to correct manually

# --------------- Other ----------------------------
name = ''                    # name of the current job
osra_path = 'osra'           # location of OSRA
action = 'corr'              # type of action to perform ('cmp' - for test data, 'corr' - for real)
fPattern = '*.png'           # type of file to search in the database

action_full = {'cmp': 'compare', 'corr': 'correct'}
tumbler = ('Off', 'On')
pattern = {'cmp': '*.mol', 'corr': '*.png'}
qualityList = {}