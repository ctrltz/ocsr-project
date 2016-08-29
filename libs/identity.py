# Script checks .raw.can and .can files
#
# Several steps of difference: (plan)
#   1a - number of atoms
#   1b - number of bonds
#   2a - atoms by type
#   2b - types of bonds
#   3 - degrees of atoms
#   ...

import molecule
import config
import sys


def main():
    debug = 0
    if len(sys.argv) == 4:
        output = sys.argv[1]
        infile = sys.argv[2]
        outfile = sys.argv[3]
        if output is '-d':
            debug = 1
    else:
        infile = sys.argv[2]
        outfile = sys.argv[3]

    identity(infile, outfile, debug)


def identity(fin, fout, debug):
    initial = molecule.Molecule(fin, debug)
    final = molecule.Molecule(fout, debug)

    atoms = abs(initial.atoms - final.atoms)
    bonds = abs(initial.bonds - final.bonds)
    diff = 0
    for el, val in initial.atomsByType.items():
        if final.atomsByType.has_key(el):
            diff += abs(val - final.atomsByType[el])
            # common.log('{0}: {1} --- {2} --> {3}', [el, val, final.atomsByType[el], diff], debug)
        else:
            diff += val
            # common.log('{0}: {1} --- 0 --> {2}', [el, val, diff], debug)

    for el, val in final.atomsByType.items():
        if not initial.atomsByType.has_key(el):
            diff += val
            # common.log('{0}: 0 --- {1} --> {2}', [el, val, diff], debug)

#    for el in initial.bondsByType.keys():
#        if final.bondsByType.has_key(el):
#            diff += abs(initial.bondsByType[el] - final.bondsByType[el])
#            if debug:
#                print '{0}: {1} --- {2} --> {3}'.format(el, initial.bondsByType[el], final.bondsByType[el], diff)
#        else:
#            diff += initial.bondsByType[el]
#            if debug:
#                print '{0}: {1} --- 0 --> {3}'.format(el, initial.bondsByType[el], diff)

#   for el in final.bondsByType.keys():
#        if not initial.bondsByType.has_key(el):
#            diff += final.bondsByType[el]
#            if debug:
#                print '{0}: 0 --- {2} --> {3}'.format(el, final.bondsByType[el], diff)

    return diff, atoms, bonds

def launch_compare(filename):
    name = path.splitext(filename)[0]
    directory = path.join(config.outDir, name)
    if not path.exists(directory):
        mkdir(directory)
    mol = path.join(directory, name)
    noh = path.join(directory, name + '.noH.mol')
    image = path.join(directory, name + '.png')
    smi = path.join(directory, name + '.smi')
    raw = path.join(directory, name + '.raw.smi')
    dfile = open(name+ '.debug', 'w')

    shutil.copyfile(filename, mol)
    subprocess.call(['molconvert', 'mol:-H', mol, '-o', noh])
    subprocess.call(['molconvert', 'png:w1920,h1080', noh, '-o', image])
    subprocess.call(['molconvert', 'smiles', noh, '-o', raw])
    subprocess.call([config.version, '-d', '-f', 'smi', '-w', smi, image], stdout=dfile)
    return identity.identity(raw, smi, config.debug)

if __name__ == '__main__':
    launch_compare(sys.argv[1])
