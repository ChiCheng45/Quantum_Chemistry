import os
import sys

from src.main.objects import Basis
from src.main.objects import PrimitiveBasisFactory


class FileInputBasis:

    def __init__(self, file_input_basis, nuclei_array):
        self.file_input_basis = os.path.join(sys.path[1], 'basissets\\' + file_input_basis)
        self.nuclei_array = nuclei_array

    def create_basis_set_array(self):
        basis_array = []
        for a in range(0, len(self.nuclei_array)):
            i = j = 0
            nuclei = self.nuclei_array[a]
            primitive_basis_array = []
            with open(self.file_input_basis, 'r') as file:
                lines = file.readlines()
                for b in range(0, len(lines)):
                    line = lines[b]
                    if nuclei.name in line:
                        i = 1
                    if i == 1:
                        if '#' in line:
                            if nuclei.name not in line:
                                break
                        else:
                            if any(letter in line for letter in ('S', 'L', 'P', 'D')) or line == '\n':
                                if j == 1:
                                    basis = Basis(nuclei.name, primitive_basis_array)
                                    basis_array.append(basis)
                                    j = 0
                                if line != '\n':
                                    primitive_basis_array = []
                                    function_type = line.split()[0]
                            else:
                                j = 1
                                float_array = [float(x) for x in line.split()]
                                primitive_basis_from_factory = PrimitiveBasisFactory().expand_basis(function_type, float_array, nuclei.coordinates)
                                primitive_basis_array += primitive_basis_from_factory
                                if b + 1 == len(lines):
                                    basis = Basis(nuclei.name, primitive_basis_array)
                                    basis_array.append(basis)
            file.close()
        return basis_array