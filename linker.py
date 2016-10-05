from os import path, chdir, listdir, mkdir, rmdir, remove
from pubchempy import get_compounds, BadRequestError
import shutil
import sys
import subprocess


def extract (name, directory):
    output_base = path.join(directory, 'image')
    subprocess.call(['pdfimages', '-png', '-j', name, output_base])


def recognize (image):
    return subprocess.check_output(['osra', image]).split("\n")[:-1]


def sift ():
    pass


def search (smile):
    try:
        compounds = get_compounds(smile, 'smiles')
    except BadRequestError:
        print 'Failed to search for', smile
        return None

    if len(compounds) == 1:
        if compounds[0].cid is None:
            return None
        else:
            return compounds[0].cid
    else:
        return None  # seems strange


def pipeline (db_dir):
    files = []
    for name in listdir(db_dir):
        if name.endswith('.pdf'):
            files.append(name)
    print 'Found', len(files), 'PDF files in specified directory'
    if len(files) == 0:
        print 'Nothing to be processed'
        return

    chdir(db_dir)
    try:
        mkdir('images')
    except OSError:
        pass  # TODO: print to stderr
    output_dir = path.join(db_dir, 'images')

    for item in files:
        chdir(db_dir)
        extract(item, output_dir)
        images = listdir(output_dir)
        chdir(output_dir)
        print path.splitext(item)[0]
        for img in images:
            print path.splitext(item)[0], '-', path.splitext(img)[0]
            links = []
            smiles = recognize(img)
            for smile in smiles:
                result = search(smile)
                if not result is None:
                    links.append(result)
            remove(img)
        if len(links) > 0:
            print "%s: %s" % (path.splitext(item)[0], ", ".join(links))
        else:
            print "%s: no links" % (path.splitext(item)[0])

    chdir(db_dir)
    shutil.rmtree('images')


if len(sys.argv) != 2 or sys.argv[1] == "-h":
    print 'usage: python linker.py <absolute database location>'
else:
    if path.isdir(sys.argv[1]):
        database_dir = sys.argv[1]
        print 'Database location:', database_dir
        pipeline(database_dir)
    else:
        print 'Specified directory does not exist'
