"""
--- Day 4: Ceres Search ---
"Looks like the Chief's not here. Next!" One of The Historians pulls out a device and pushes the only button on it. After a brief flash, you recognize the interior of the Ceres monitoring station!

As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: XMAS.

This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:

..X...
.SAMX.
.A..A.
XMAS.S
.X....
The actual word search will be full of letters instead. For example:

MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:

....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX
Take a look at the little Elf's word search. How many times does XMAS appear?exit
"""

"""
--- Part Two ---
The Elf looks quizzically at you. Did you misunderstand the assignment?

Looking for the instructions, you flip over the word search to find that this isn't actually an XMAS puzzle;
it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an X. One way to achieve that is like this:

M.S
.A.
M.S
Irrelevant characters have again been replaced with . in the above diagram. Within the X, each MAS can be written forwards or backwards.

Here's the same example from before, but this time all of the X-MASes have been kept instead:

.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
In this example, an X-MAS appears 9 times.

Flip the word search from the instructions back over to the word search side and try again. How many times does an X-MAS appear?
"""

"""
SEARCH ALGORITHM
-find all X and their coordinates
-find all M and their coordinates
-from those two lists, find all X with distance 1 from an M
-From there, try to match the rest of the string

PART 2:
i did the right thing conserving the coordinates.
I match all MAS
I search for pairs that obey a transformation
"""



#--------------------------------------------------------------------------------------------------------------------------------
#   IMPORTS
#--------------------------------------------------------------------------------------------------------------------------------

import logging

import itertools

#import math

from typing import Dict, Tuple, List

#--------------------------------------------------------------------------------------------------------------------------------
#   
#--------------------------------------------------------------------------------------------------------------------------------

class Matrix:
    """
    A class to represent a matrix loaded from a text file.

    Attributes:
    -----------
    lls_matrix : List[List[str]]
        A 2D list to store the matrix elements.
    n_num_rows : int
        Number of rows in the matrix.
    n_num_cols : int
        Number of columns in the matrix.
    """

    def __init__(self):
        """
        Initializes the Matrix with empty attributes.
        """
        self.lls_matrix: List[List[str]] = list()
        self.dtn_matrix = dict()
        self.n_num_rows: int = 0
        self.n_num_cols: int = 0

    def load_matrix(self, s_filename: str) -> bool:
        """
        Loads the matrix from a text file. Ensures all rows have the same length.

        Parameters:
        -----------
        s_filename : str
            The name of the file to load the matrix from.

        Returns:
        --------
        bool
            False if the matrix is loaded successfully, True if there is an error.
        """
        with open(s_filename, 'r') as cl_file:
            for s_line in cl_file:
                s_row: List[str] = list(s_line.strip())
                if self.lls_matrix and len(s_row) != len(self.lls_matrix[0]):
                    logging.error("All rows in the matrix must be the same length.")
                    return True # fail
                self.lls_matrix.append(s_row)

        if not self.lls_matrix:
            logging.error("The matrix is empty.")
            return True # fail

        self.n_num_rows = len(self.lls_matrix)
        self.n_num_cols = len(self.lls_matrix[0])

        logging.info(f"Matrix loaded successfully with size {self.n_num_rows} rows x {self.n_num_cols} columns.")

        self.create_dict()

        self.print_matrix(self.lls_matrix)

        return False # OK

    def create_dict(self) -> Dict[Tuple[int, int], str]:
        """
        Creates a dictionary from the matrix where the key is a tuple of coordinates
        and the value is the letter at that position.

        Returns:
        bool
            False if the matrix is loaded successfully, True if there is an error.
        --------
        Dict[Tuple[int, int], str]
            A dictionary with coordinates as keys and letters as values.
        """
        self.dtn_matrix = dict()
        for row_index, row in enumerate(self.lls_matrix):
            for col_index, elem in enumerate(row):
                self.dtn_matrix[(row_index, col_index)] = elem
        logging.info(f"Dict: {self.dtn_matrix}")
        return False

    def is_coordinate_letter( self, in_x, in_y, s_char ):
        if (in_x < 0):
            logging.error(f"ERR Underflow X: {in_x}")
            return False

        if (in_y < 0):
            logging.error(f"ERR Underflow: Y: {in_y}")
            return False

        if (in_x >= self.n_num_cols):
            logging.error(f"ERR Overflow X: {in_x}")
            return False

        if (in_y >= self.n_num_rows):
            logging.error(f"ERR Overflow Y: {in_y}")
            return False

        if (self.lls_matrix[in_x][in_y] == s_char):
            return True #match

        return False

    def print_matrix(self, ills_matrix: List[List[str]]) -> None:
        """
        Prints the matrix size, its elements, and coordinates with a spacing of three characters per element.
        """
        logging.info(f"Matrix size: {self.n_num_rows} rows x {self.n_num_cols} columns")
        
        # Print column indices
        header = "  " + " ".join(f"{i:3}" for i in range(self.n_num_cols))
        logging.info(header)
        print(header)
        
        # Print rows with row indices
        for i, row in enumerate(ills_matrix):
            row_string = f"{i:3} " + " ".join(f"{elem:3}" for elem in row)
            logging.info(row_string)
            print(row_string)

    def seek_letter_from_matrix(self, s_char: str) -> List[Tuple[int, int]]:
        """
        Search for all occurrences of a character within the matrix.

        Parameters:
        -----------
        s_char : str
            The character to search for in the matrix.

        Returns:
        --------
        List[Tuple[int, int]]
            A list of tuples where each tuple contains the row and column indices of an occurrence of the character.
        """
        ltn_result = list()
        if len(s_char) != 1:
            return ltn_result

        for row_index, row in enumerate(self.lls_matrix):
            for col_index, elem in enumerate(row):
                if elem == s_char:
                    ltn_result.append((row_index, col_index))
        logging.debug(f"Seek {s_char} {len(ltn_result)} | {ltn_result}")
        return ltn_result
    
    
    def seek_letter(self, s_char: str) -> List[Tuple[int, int]]:
        """
        Search for all occurrences of a character within the matrix using the dictionary.

        Parameters:
        -----------
        s_char : str
            The character to search for in the matrix.

        Returns:
        --------
        List[Tuple[int, int]]
            A list of tuples where each tuple contains the row and column indices of an occurrence of the character.
        """
        ltn_result = [tn_coordinate for tn_coordinate, s_letter in self.dtn_matrix.items() if s_letter == s_char]
        logging.debug(f"Seek {s_char} {len(ltn_result)} | {ltn_result}")
        return ltn_result

    def find_neighbour( self, iltn_first : List[Tuple[int, int]], iltn_second : List[Tuple[int, int]] ) -> List[Tuple[int, int, int, int]]:
        """
        given two lists of coordinates, find all the instances where one coordinate from the first list is 1 distance from one coordinate in the second 
        generate a list of touple with the X,Y coordinate of the first letter
        followed by the X increment and Y increment where the second letter is located
        this way following the increment you can match the rest of the word
        """
        ltn_result = list()
        for tn_first, tn_second in itertools.product(iltn_first, iltn_second):
            # Check if the distance between the two is 1 in any direction
            if abs(tn_first[0] - tn_second[0]) <= 1 and abs(tn_first[1] - tn_second[1]) <= 1:
                x_increment = tn_second[0] - tn_first[0]
                y_increment = tn_second[1] - tn_first[1]
                ltn_result.append((tn_first[0], tn_first[1], x_increment, y_increment))
        logging.debug(f"Neighbour: {len(ltn_result)} | {ltn_result}")
        return ltn_result

    def compute_index( self, itn_vector : Tuple[int,int,int,int], in_index: int) -> Tuple[int,int]:
        """
        From a vector, compute the coordinate given an index distance
        """

        n_x = itn_vector[0]
        n_y = itn_vector[1]
        n_delta_x = itn_vector[2]
        n_delta_y = itn_vector[3]

        return (n_x+n_delta_x*in_index, n_y+n_delta_y*in_index)

    def detect_cross_angle( self, itn_first : Tuple[int,int,int,int], itn_second : Tuple[int,int,int,int] ):
        n_delta_ax = itn_first[2]
        n_delta_ay = itn_first[3]
        n_delta_bx = itn_second[2]
        n_delta_by = itn_second[3]
        
        n_sum = n_delta_ax+n_delta_bx +n_delta_ay +n_delta_by
        b_ninety_degree = (abs(n_sum) == 2)
        #test using expensive ATAN. I know if sum is 2 in abs it's 90°.
        #n_angle_a = math.atan2( n_delta_ay, n_delta_ax )
        #n_angle_b = math.atan2( n_delta_by, n_delta_bx )
        #logging.debug(f"Sum: {n_sum} | Angle: {(n_angle_a - n_angle_b)*360/2/math.pi}")
        return b_ninety_degree

    def match_sequence( self, itn_origin_direction : Tuple[int,int,int,int], s_sequence : str ) -> bool:
        """
        From an origin and a direction, try to match a whole sequence. First two characters already match.
        """
        
        if (len(s_sequence) == 2):
            return True #already a match
        elif (len(s_sequence) < 1):
            raise False #algorithm error
                
        for n_cnt in range( 2, len(s_sequence) ):
            tn_coordinate = self.compute_index( itn_origin_direction, n_cnt )

            if (0 <= tn_coordinate[0] < self.n_num_cols) and (0 <= tn_coordinate[1] < self.n_num_rows):
                if (self.lls_matrix[tn_coordinate[0]][tn_coordinate[1]] != s_sequence[n_cnt]):
                    return False #do not match because letters are different
            else:
                return False #do not match because it overflows

        #logging.debug(f"match: {itn_origin_direction}")

        return True #match

    def seek_sequence( self, s_sequence : str ) -> List[Tuple[int,int,int,int]]:
        """
        Search for all the occurrences of a sequence within the matrix in eight directions
        """
        
        #find where the first letter appears
        ltn_first_char = self.seek_letter( s_sequence[0] )
        #find where the second letter appears
        ltn_second_char = self.seek_letter( s_sequence[1] )
        #now, find all pairs of first and second letter that are within 1 distance from each other
        ltn_neighbour = self.find_neighbour( ltn_first_char, ltn_second_char )
        #now I have a starting coordinate where at least two letters match, and a scan direction. I now match the whole sequence

        ltn_result = list()
        n_match = 0

        for tn_neighbour in ltn_neighbour:
            if self.match_sequence( tn_neighbour, s_sequence):
                n_match += 1
                ltn_result.append( tn_neighbour )

        logging.debug(f"Neighbour: {len(ltn_result)} | {ltn_result}")

        return ltn_result
    
    def seek_sequence_cross( self, s_sequence : str ) -> List[Tuple[int,int,int,int]]:
        """
        I launch the previous search, and get all the sequences
        works on example but overestimate on full list
        rather than fix I do a better algorithm
        """
        ltn_result = list()
        #Get all the sequences that match with coordinates and increments
        ltn_matches = self.seek_sequence( s_sequence )
        #I need to find all sequences that have the same center, and only count the pairs

        for tn_pair in itertools.combinations(ltn_matches, 2):
            #logging.debug(f"Pair: >{tn_pair[0]}< >{tn_pair[1]}< Origin 1: {self.compute_index(tn_pair[0],1)} Origin 2: {self.compute_index(tn_pair[1],1)}")
            #find all the sequences that cross at A
            if (self.compute_index(tn_pair[0],1) == self.compute_index(tn_pair[1],1)):
                #it's not just enough to get the center. I have to scan for 45° crossing.
                if (self.detect_cross_angle(tn_pair[0], tn_pair[1])):
                    #it's not just enough to search for crossing
                    #i need to filter out plus patter
                    if (tn_pair[0][2]== 0) or (tn_pair[0][3]== 0) or (tn_pair[1][2]== 0) or (tn_pair[0][3]== 0):
                        pass
                    #only allow diagonal patterns
                    else:
                        ltn_result.append(tn_pair)
        
        self.create_and_print_matrix(ltn_result, "day04\day_4_output.txt")

        logging.debug(f"Cross: {len(ltn_result)} | {ltn_result}")
        return ltn_result

    def seek_cross_pattern( self, itn_center : Tuple[int,int,int,int] ) -> bool:
        """
        I have the coordinate of the center, I search for pattern
        """

        (n_x, n_y) = itn_center

        #prevent OOB by matching A one away from the border
        if (n_x < 1) or (n_x > self.n_num_cols-2) or (n_y < 1) or (n_y > self.n_num_rows-2):
            return False #can't match because OOB

        n_diagonals = 0

        if self.is_coordinate_letter( n_x-1, n_y-1, "M") and self.is_coordinate_letter( n_x+1, n_y+1, "S"):
            n_diagonals += 1
        if self.is_coordinate_letter( n_x-1, n_y-1, "S") and self.is_coordinate_letter( n_x+1, n_y+1, "M"):
            n_diagonals += 1
        if self.is_coordinate_letter( n_x-1, n_y+1, "M") and self.is_coordinate_letter( n_x+1, n_y-1, "S"):
            n_diagonals += 1
        if self.is_coordinate_letter( n_x-1, n_y+1, "S") and self.is_coordinate_letter( n_x+1, n_y-1, "M"):
            n_diagonals += 1
        
        #if I matche exactly two diagonals
        if (n_diagonals == 2):
            #logging.debug(f"Cross match found: {itn_center}")
            return True

        return False

    def seek_sequence_cross_v2( self, s_sequence : str ) -> List[Tuple[int,int]]:
        """
        I do a better algorithm, I think I shouldn't find plus shapes
        I search all "A"
        I search for patterns around the A
        M.M
        .A.
        S.S
        """

        ltn_letter_a = self.seek_letter( "A" )
        logging.debug(f"Find A: {len(ltn_letter_a)} | {ltn_letter_a}")

        ltn_result = list()

        for tn_center in ltn_letter_a:
            print(tn_center)
            if self.seek_cross_pattern( tn_center ) == True:
                ltn_result.append(tn_center)

        logging.debug(f"MAS Patterns: {len(ltn_letter_a)} | {ltn_letter_a}")

        return ltn_result

    def create_and_print_matrix(self, coordinates: List[Tuple[Tuple[int, int, int, int], Tuple[int, int, int, int]]], filename: str):
        """
        Creates an empty matrix of the same size and writes 'M' at the specified coordinates.
        Prints the matrix to a file.
        
        Parameters:
        -----------
        coordinates : Tuple
            A tuple containing two tuples with the coordinates and increments.
        filename : str
            The name of the file to print the matrix to.
        """
        # Create an empty matrix of the same size
        empty_matrix = [[' ' for _ in range(self.n_num_cols)] for _ in range(self.n_num_rows)]

        for coordinate in coordinates:
            # Extract the coordinates
            (x1, y1, _, _), (x2, y2, _, _) = coordinate

            # Place 'M' at the specified coordinates
            if 0 <= x1 < self.n_num_rows and 0 <= y1 < self.n_num_cols:
                empty_matrix[x1][y1] = 'M'
            if 0 <= x2 < self.n_num_rows and 0 <= y2 < self.n_num_cols:
                empty_matrix[x2][y2] = 'M'
            
            # Print the matrix to a file
            with open(filename, 'w') as file:
                for row in empty_matrix:
                    file.write(''.join(row) + '\n')

        self.print_matrix( empty_matrix )

        logging.info(f"Matrix with 'M' printed to {filename}")

def day_4( s_filename: str ):
    cl_matrix = Matrix()
    cl_matrix.load_matrix(s_filename)
    ltn_result = cl_matrix.seek_sequence("XMAS")
    print(f"XMAS Matches: {len(ltn_result)}")

    ltn_result_part_2 = cl_matrix.seek_sequence_cross("MAS")
    print(f"CROSS MAS Matches: {len(ltn_result_part_2)}")
    ltn_result_part_2 = cl_matrix.seek_sequence_cross_v2("MAS")
    print(f"CROSS MAS Matches (V2): {len(ltn_result_part_2)}")

#--------------------------------------------------------------------------------------------------------------------------------
#   MAIN
#--------------------------------------------------------------------------------------------------------------------------------

# Example usage
gs_filename_example = 'day04\day_4_example.txt'
gs_filename = 'day04\day_4.txt'
#   if interpreter has the intent of executing this file
if __name__ == "__main__":
    logging.basicConfig(
        filename='day04\day_4.log',
        # Specify the log file name
        level=logging.DEBUG,
        # Set the level of debug to show
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("Begin") 

    #day_4( gs_filename_example )
    #2004 is too high!
    #I filter out PLUS patterns, when one direction is zero
    #now i get 1998 filtering one zero
    #now I get 1992 filtering ALL zero delta coordinates

    #try as well with algorithm V2, funds 1992 matches as well
    day_4( gs_filename )




