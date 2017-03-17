#!/usr/bin/python
#
# This script contains:
#  - common functions used to output debug & error information
#  - all widely used variables (file paths, useful parameters, etc)

RESULTS_RELATIVE_PATH = '../../res'
REPORT_FILE = 'report.txt'


# ------------ Directories ----------------------------
prjDir = ''                  # project's working directory
dbDir = ''                   # directory with the current database
resDir = ''                  # directory with all results
tmpDir = ''                  # directory with temporary files for processing
goodDir = ''                 # directory with SMILEs that are suggested to be good
allDir = ''                  # directory with all SMILEs obtained
inDir = ''                   # directory with input recognized structures
outDir = ''                  # directory with the results of recognition

# --------------- Files ----------------------------
spelling = ''                # location of the 'spelling.txt' file
superatom = ''               # location of the 'superatom.txt' file
spelling_noh = ''            # location of the 'spelling.noh.txt' file
superatom_noh = ''           # location of the 'superatom.noh.txt' file
report_file = ''             # location of the file with SMILEs obtained

# --------------- Flags ----------------------------
debug = 0                    # turning on (1) / off (0) debug mode
restore = 0                  # restoring (if 1) initial 'spelling.txt' file
auto = 1                     # correct automatically (if 1)
noh = 0                      # use 'spelling.noh.txt' and 'superatom.noh.txt'
manual = 0                   # number of images to correct manually

# --------------- Other ----------------------------
name = ''                    # name of the current job
osra_path = 'osra'           # location of OSRA
jar_path = ''                # location of a .jar counting several characteristics for images
action = 'corr'              # type of action to perform ('cmp' - for test data, 'corr' - for real)
fPattern = '*.png'           # type of file to search in the database

action_full = {'cmp': 'compare', 'corr': 'correct'}
tumbler = ('Off', 'On')
pattern = {'cmp': '*.mol', 'corr': '*.png'}
qualityList = {}