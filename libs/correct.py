import config
import quality
import subprocess
import utils

from os import path, mkdir, chdir, remove
from shutil import move

def rm(string, pos):
    return string[:pos] + string[(pos+1):]


def toupper(string, pos):
    return string[:pos] + string[pos].upper() + string[(pos+1):]


def remove_hydrogens(mol):  # removes all H with their counters from string
    flag = 0
    i = 0
    while i < len(mol):
        # print 'String: {0}. Ch: {1}. Action: {2}'.format(mol, i+1, mol[i] == 'H' or flag and mol[i].isdigit())
        if mol[i] == 'H' or flag and mol[i].isdigit():
            mol = rm(mol, i)
            flag = 1
        else:
            mol = toupper(mol, i)
            flag = 0
            i += 1

    return mol


def correct(fin):
    image_name = path.splitext(path.basename(fin))[0]
    base = path.join(config.tmpDir, image_name)
    src = base + ".png"

    utils.log('\nSource file: {}', src)

    '''
    if not config.auto:
        initdebug = base + ".init.debug"
        initdfile = open(initdebug, "w")
        subprocess.call([config.osra_path, "-l", config.spelling, "-d", "-f", "smi", "-w", init, src],
                        stdout=initdfile)

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
    '''

    chdir(config.tmpDir)
    template = 'struct-'
    print config.osra_path + ' -b -f smi -p -o ' + template + ' ' + fin
    osra = subprocess.Popen([config.osra_path, '-b', '-f', 'smi', '-p', '-o', template, fin],
                            stdout = subprocess.PIPE)

    counter = 0
    for line in osra.stdout:
        image_path = template + str(counter) + '.png'

        if config.jar_path != '':
            jar_path = 'java -jar ' + config.jar_path + ' ' + image_path
            print jar_path

            jar = subprocess.Popen(['java', '-jar', config.jar_path, image_path],
                                   stdout=subprocess.PIPE)

            with open(config.report_file, "a") as fout:
                fout.write(line[:-1] + '\t' + jar.stdout.readline() + '\n')
                # fout.write(line)

        inPath = path.normpath(path.join(config.inDir, image_name + '.' + image_path))
        move(image_path, inPath)
        counter += 1

    # config.qualityList[fin] = quality.estimate(base)
    remove(src)
    chdir(config.dbDir)