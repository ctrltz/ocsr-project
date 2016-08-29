import molecule
import config
import utils
import subprocess


def estimate(base, cor_number=0, size="png:w1920,h1080"):
    finalsmi = base + ".final.smi"
    finalpng = base + ".final.png"
    finalmol = base + ".final.mol"

    # TODO - user degrees
    degmax = {'C': 4, 'N': 3, '0': 2, 'H': 1, 'Br': 1, 'Cl': 1}
    undefined = 0
    failed = 0
    wrong_deg = 0
    qual = 0

    subprocess.call(['molconvert', 'mol:V3-H+-a_gen', finalsmi, '-o', finalmol])
    subprocess.call(['molconvert', size, finalmol, '-o', finalpng])
    final = molecule.Molecule(finalmol)

    if final.atoms == 0 and final.bonds == -1:
        config.log('OSRA failed to convert your image. Output file is empty.', [], config.debug)
        failed = 1
        qual = 0.0
    else:
        for data in final.atom_dict.values():
            if data[0] == 'A':
                undefined += 1
            elif data[0] in degmax.keys():
                if int(data[1]) == degmax[data[0]] + data[2]:
                    qual += 1.0
                else:
                    wrong_deg += 1
                    qual += 0.5

        # TODO: strange situation with empty files got here
        try:
            qual /= float(final.atoms)
            qual -= (cor_number / (4 * final.atoms))
        except ZeroDivisionError:
            failed = 1
            qual = 0.0

    return [undefined, failed, cor_number, wrong_deg, qual]
