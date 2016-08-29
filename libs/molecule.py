#!/usr/bin/python
#
# Molecule class contains necessary info about the structure from
# the input file:
#   - number of atoms
#   - number of bonds
#   - number of atoms of each type
#   - number of bonds of each type
#   - charge and valence of each atom
#
# Only MOL (V3000) and SMI file formats are supported.

import os
import config


class Molecule (object):

    default = ['Cl', 'Br', 'H', 'O', 'N', 'C', 'P', 'S', 'F']
    bondTypes = ['single', 'double', 'triple', 'aromatic']

    def __init__(self, fin):
        self.filename = fin
        self.ext = os.path.splitext(self.filename)[1][1:]

        if config.debug:
            config.log('Input: {} - {} file', os.path.basename(self.filename), self.ext)

        self.atoms = 0                                            # Number of atoms
        self.bonds = 0                                            # Number of bonds
        self.atomsByType = dict.fromkeys(self.default, 0)         # {atom type: number of these atoms}
        self.bondsByType = dict.fromkeys(self.bondTypes, 0)       # {bond type: number of these bonds}
        self.atom_dict = {}                                       # {id: [atom, valence, charge]}

        if self.ext == 'smi':
            self.smi_parse()
        elif self.ext == 'mol':
            self.mol_parse()
        else:
            config.log('Only MOL / SMI file formats are supported')

        if config.debug:
            config.log('{} atoms: {}', self.atoms, self.atomsByType)
            config.log('{} bonds: {}', self.bonds, self.bondsByType)

    # Parsing SMI file - not ideal, still to do:
    #   - counting atom degrees
    #   - [C@@] error
    #   - might be some more
    # Useful link: http://www.opensmiles.org/spec/open-smiles-3-input.html#3.1
    def smi_parse(self):
        digits = 0
        with open(self.filename) as f:
            for line in f:
                line = line.lower()
        
                # Need to exclude [atoms] first
                for i in range(line.count('[')):
                    # Get '[' and ']' pos
                    start = line.index('[')
                    end = line.index(']')

                    # Exclude element
                    el = line[(start + 1):end].upper()
                    line = line[:start] + line[(end + 1):]

                    # Add to dict or increase counter
                    if self.atomsByType.has_key(el):
                        self.atomsByType[el] += 1
                    else:
                        if '@' in el:
                            self.atomsByType[el[0]] += 1
                            self.atomsByType[el[-1]] += 1
                        else:
                            self.atomsByType.setdefault(el, 1)
                    # print "Element: {0} - {1}".format(el, self.atomsByType[el])

                # Then can go through dictionary
                for el in self.default:
                    if el == 'C':
                        self.atomsByType[el] -= self.atomsByType['Cl']
                    self.atomsByType[el] += line.count(el.lower())
                digits += sum(c.isdigit() for c in line)

                self.bondsByType['double'] += line.count('=')
                self.bondsByType['triple'] += line.count('#')
                self.bondsByType['aromatic'] += line.count(':')

            for atom in self.atomsByType.values():
                self.atoms += atom

            self.bonds = self.atoms - 1 + digits / 2
            self.bondsByType['single'] = self.bonds - sum(self.bondsByType.values())

    # Parsing MOL file - much more stable
    # Only molV3 is available now
    # Sort of specification: http://c4.cabrillo.edu/404/ctfile.pdf
    def mol_parse(self):
        counter = 0
        with open(self.filename) as mol:
            for line in mol:
                counter += 1
                if counter == 6:
                    self.atoms = int(line.split()[3])
                    self.bonds = int(line.split()[4])
                if 8 <= counter < 8 + self.atoms:
                    # Element label
                    el = line.split()[3]
                    if el in self.atomsByType:
                        self.atomsByType[el] += 1
                    else:
                        self.atomsByType[el] = 1
                    # Charge
                    charge = 0
                    for val in line.split():
                        if val[0:3] == 'CHG':
                            charge = int(val[4:])
                    # Add to the dictionary
                    self.atom_dict[counter - 7] = [el, 0.0, charge]
                if 10 + self.atoms <= counter < 10 + self.atoms + self.bonds:
                    # Bond type: 1 - single, 2 - double, 3 - single,
                    #            4 - aromatic (1.5), > 4 - not processed
                    bond_type = int(line.split()[3])
                    if bond_type == 4:
                        bond_type = 1.5
                    elif bond_type > 4:
                        config.log('Warning: bond type > 4')
                    id_first = int(line.split()[4])
                    id_second = int(line.split()[5])
                    self.atom_dict[id_first][1] += bond_type
                    self.atom_dict[id_second][1] += bond_type

            if config.debug:
                config.log('{}', self.atom_dict)
