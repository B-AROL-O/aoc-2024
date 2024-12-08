#download and install latest python and add path

#remove path of the older python

#check that the version is right with
#python --version

#Create Venv
#python -m venv Astral

#activate the env
#Astral\Scripts\activate

#upgrade pip
#python.exe -m pip install --upgrade pip

#install numpy in the venv
#pip install numpy

#pip doesn't unistall dependencies
import itertools
from typing import List, Tuple

def seek_sequence(self, s_sequence: str) -> List[Tuple[int, int, int, int]]:
    """
    Search for all the occurrences of a sequence within the matrix in eight directions.
    """
    ltn_result = list()

    # Find where the first letter appears
    ltn_first_char = self.seek_letter(s_sequence[0])

    # Find where the second letter appears
    ltn_second_char = self.seek_letter(s_sequence[1])

    # Scan all combinations of the first and second tuples using itertools.product
    for first, second in itertools.product(ltn_first_char, ltn_second_char):
        # Check if the distance between the two is 1 in any direction
        if abs(first[0] - second[0]) <= 1 and abs(first[1] - second[1]) <= 1:
            x_increment = second[0] - first[0]
            y_increment = second[1] - first[1]
            ltn_result.append((first[0], first[1], x_increment, y_increment))

    return ltn_result
