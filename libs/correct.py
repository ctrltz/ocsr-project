import config
import quality
import subprocess
import utils
from os import path, mkdir, chdir


def remove(string, pos):
    return string[:pos] + string[(pos+1):]


def toupper(string, pos):
    return string[:pos] + string[pos].upper() + string[(pos+1):]


def remove_hydrogens(mol):  # removes all H with their counters from string
    flag = 0
    i = 0
    while i < len(mol):
        # print 'String: {0}. Ch: {1}. Action: {2}'.format(mol, i+1, mol[i] == 'H' or flag and mol[i].isdigit())
        if mol[i] == 'H' or flag and mol[i].isdigit():
            mol = remove(mol, i)
            flag = 1
        else:
            mol = toupper(mol, i)
            flag = 0
            i += 1

    return mol


def correct(fin, folder):
    base = path.join(folder, path.splitext(path.basename(fin))[0])
    init = base + ".smi"
    src = base + ".png"

    if config.debug:
        utils.log('\nSource file: {}', src)
        utils.log('Output: {}', init)

    if not config.auto:
        initdebug = base + ".init.debug"
        initdfile = open(initdebug, "w")
        subprocess.call([config.osra_path, "-l", config.spelling, "-d", "-f", "smi", "-w", init, src],
                        stdout=initdfile)
        '''
        initdfile.close()
        initdfile = open(initdebug, "r")

        common.log("Some help with spelling correction may be needed", [])

        changeList = {}
        helpFlag = 0
        for line in initdfile:
            info = line.split()
            if len(info) == 3:
                if not info[0] in changeList:
                    helpFlag = 1
                    if common.auto:
                        change = remove_hydrogens(info[0])
                        # common.log('{0} --> {1}', [info[0], change])
                    else:
                        change = raw_input(info[0] + ' --> ')
                    changeList[info[0]] = change

        if helpFlag == 0:
            common.log("Never mind, everything's ok", [])
        else:
            common.log("Updated the 'spelling.txt' file", [])

        spell = open(common.spelling, "a")
        spell.write("\n")
        for el in changeList.keys():
            if changeList[el] is not '':
                spell.write("%s %s\n" % (el, changeList[el]))

        spell.close()
        '''

        final = base + ".final.smi"
        finaldebug = base + ".final.debug"
        finaldfile = open(finaldebug, "w+")
        subprocess.call([config.osra_path, "-l", config.spelling, "-d", "-f", "smi", "-w", final, src],
                        stdout = finaldfile)

        utils.log('\nCorrected output: {}', final, config.debug)
        utils.log('Final debug info: {}', finaldebug, config.debug)

        initdfile.close()
        finaldfile.close()
    else:
        subprocess.call([config.osra_path, "-f", "smi", "-w", init, src])

    config.qualityList[fin] = quality.estimate(base)
