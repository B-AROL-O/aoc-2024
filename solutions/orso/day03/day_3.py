"""
--- Day 3: Mull It Over ---
"Our computers are having issues, so I have no idea if we have any Chief Historians in stock!
You're welcome to check the warehouse, though,"
says the mildly flustered shopkeeper at the North Pole Toboggan Rental Shop.
The Historians head out to take a look.

The shopkeeper turns to you
"Any chance you can see why our computers are having issues again?"

The computer appears to be trying to run a program, but its memory (your puzzle input) is corrupted.
All of the instructions have been jumbled up!

It seems like the goal of the program is just to multiply some numbers.
It does that with instructions like mul(X,Y), where X and Y are each 1-3 digit numbers.
For instance, mul(44,46) multiplies 44 by 46 to get a result of 2024.
Similarly, mul(123,4) would multiply 123 by 4.

However, because the program's memory has been corrupted, there are also many invalid characters that should be ignored
even if they look like part of a mul instruction.
Sequences like mul(4*, mul(6,9!, ?(12,34), or mul ( 2 , 4 ) do nothing.

For example, consider the following section of corrupted memory:

xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))

Only the four highlighted sections are real mul instructions.
Adding up the result of each instruction produces 161 (2*4 + 5*5 + 11*8 + 8*5).

Scan the corrupted memory for uncorrupted mul instructions. What do you get if you add up all of the results of the multiplications?
"""

"""
--- Part Two ---
As you scan through the corrupted memory, you notice that some of the conditional statements are also still intact.
If you handle some of the uncorrupted conditional statements in the program, you might be able to get an even more accurate result.

There are two new instructions you'll need to handle:

The do() instruction enables future mul instructions.
The don't() instruction disables future mul instructions.
Only the most recent do() or don't() instruction applies.
At the beginning of the program, mul instructions are enabled.

For example:

xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
This corrupted memory is similar to the example from before, but this time the mul(5,5) and mul(11,8)
instructions are disabled because there is a don't() instruction before them.
The other mul instructions function normally, including the one at the end that gets re-enabled by a do() instruction.

This time, the sum of the results is 48 (2*4 + 8*5).
"""

"""
ALGORITHM
do a finite state machine that matches
1) match "mul("
2) search an int
3) search ","
4) search an int
5) search )
6) return two operands X, Y
I also match
"do()"
"don't()"
that enable a flag
that false won't append the result
"""

import logging

from typing import Tuple, List

#enumeration support
from enum import Enum, auto

def load_string(is_filename: str) -> str:
    """
    From file, load the full string

    :param filename: The name of the file containing the location IDs.
    :return: string of the problem
    """
    s_sequence = str()

    with open(is_filename, 'r') as c_file:
        for s_line in c_file:
            s_sequence += s_line

    return s_sequence

def parse_sequence( s_sequence : str ) -> List[Tuple[int, int]]:
    """
    From a sequence, extract mul(X,Y)->[(X,Y)]
    :param s_sequence: sequence of characters
    """

    ltn_result = list()

    ls_state = ["m", "u", "l", "(", "X", ",", "Y", ")"]
    ls_state_do = ["d", "o", "(", ")"]
    ls_state_dont = ["d", "o", "n", "'", "t", "(", ")"]


    #detect special command, start from execute
    b_execute_mul = True

    #start from searching m
    
    n_arg_x = int(0)
    n_arg_y = int(0)
    n_index = 0
    n_max_index = len(s_sequence)

    while n_index < n_max_index:
        #fetch character
        s_char = s_sequence[n_index]
        #next character
        n_index += 1
        logging.debug(f"Char: {s_char} | State: {cl_state}")

        #not parsing a token
        if (state.e_state == state.E_TOKEN.IDLE.value):
            #match mul
            if (s_char == "m"):
                s_state = "u"
                e_state = E_TOKEN.PARSE_MUL.value
                logging.debug(f"match mul(X,Y) {s_char}")
            elif (s_char == "d"):
                s_state = "o"
                e_state = E_TOKEN.PARSE_DO.value
                logging.debug(f"match do()/don't() {s_char}")
            else:
                reset_fsm()
                
        elif (e_state == E_TOKEN.PARSE_MUL.value):
            if (s_state == "u"):
                if (s_char == s_state):
                    #match
                    s_state = "l"
                    logging.debug(f"match {s_char}")
                else:
                    logging.debug(f"Char: {s_char} | state: {s_state} | FSM error, reset.")
                    reset_fsm()
            elif (s_state == "l"):
                if (s_char == s_state):
                    s_state = "("
                    logging.debug(f"match {s_char}")
                else:
                    #reset
                    s_state = ls_state[0]
                    logging.debug(f"Char: {s_char} | state: {s_state} | FSM error, reset.")
            elif (s_state == ls_state[3]):
                if (s_char == s_state):
                    #detect number
                    s_state = ls_state[4]
                    s_number = ""
                    logging.debug(f"match {s_char}")
                else:
                    #reset
                    s_state = ls_state[0]
                    logging.debug(f"Char: {s_char} | state: {s_state} | FSM error, reset.")
            #match number, I eat all numbers and parse them into int when I get a non number
            elif (s_state == ls_state[4]):
                #number
                if (s_char >= "0") and (s_char <= "9"):
                    s_number += s_char
                    logging.debug(f"detecting number {s_char} ->{s_number}")
                #no numbers were eaten
                elif len(s_number) <= 0:
                    #reset
                    s_state = ls_state[0]
                    logging.debug(f"Char: {s_char} | state: {s_state} | FSM error, no number detected.")
                #parse number to int
                else:
                    n_arg_x = int(s_number)
                    logging.debug(f"Detected X {n_arg_x}")
                    #I need to reprocess this character
                    n_index -= 1
                    #next state
                    s_state = ls_state[5]
            elif (s_state == ls_state[5]):
                if (s_char == s_state):
                    #detect number
                    s_state = ls_state[6]
                    s_number = ""
                    logging.debug(f"match {s_char}")
                else:
                    #reset
                    logging.debug(f"Char: {s_char} | state: {s_state} | FSM error, reset.")
                    s_state = ls_state[0]
            #match number, I eat all numbers and parse them into int when I get a non number
            elif (s_state == ls_state[6]):
                #number
                if (s_char >= "0") and (s_char <= "9"):
                    s_number += s_char
                    logging.debug(f"detecting number {s_char} ->{s_number}")
                #no numbers were eaten
                elif len(s_number) <= 0:
                    #reset
                    s_state = ls_state[0]
                    logging.debug(f"Char: {s_char} | state: {s_state} | FSM error, no number detected.")
                #parse number to int
                else:
                    n_arg_y = int(s_number)
                    logging.debug(f"Detected Y {n_arg_y}")
                    #I need to reprocess this character
                    n_index -= 1
                    #next state
                    s_state = ls_state[7]
            elif (s_state == ls_state[7]):
                if (s_char == s_state):
                    #detect number
                    logging.debug(f"FINAL MATCH, VALID X: {n_arg_x} Y: {n_arg_y}")
                    tn_mul = (n_arg_x,n_arg_y)
                    ltn_result.append(tn_mul)
                    #reset
                    s_state = ls_state[0]
                else:
                    #reset
                    logging.debug(f"Char: {s_char} | state: {s_state} | FSM error, reset.")
                    s_state = ls_state[0]
            else:
                s_state = ls_state[0]
                logging.debug("ERR:ALGORITHM: ask the dev to finish his job")    

        elif (e_state == E_TOKEN.PARSE_MUL.value):
            if (s_state == "o"):
                if (s_char == "o"):
                    s_state = "n"
                    s_number = ""
                    logging.debug(f"match {s_char}")
                else:
                    #reset
                    logging.debug(f"Char: {s_char} | state: {s_state} | FSM error, reset.")
                    s_state = ls_state[0]
            else:
                reset_fsm()
        else:
            logging.debug("ERR:ALGORITHM: ask the dev to finish his job")
            logging.debug(f"Char: {s_char} | state: {s_state} {e_state} | FSM error, reset.")
            s_state = ""
            e_state = E_TOKEN.PARSE_IDLE

    return ltn_result


class Parser():
    class E_TOKEN( Enum ):
        IDLE = 0
        PARSE_MUL = auto()
        PARSE_DO = auto()
        PARSE_DONT = auto()

    def __init__(self):
        self.n_index = 0
        self.n_index_max = 0
        self.gltn_results = list()
        self.e_state = self.E_TOKEN.IDLE
        self.s_state = ""
        self.s_number = ""
        #"do()" and "don't()" can blank MUL
        self.b_allow_mul = True
        return

    def reset_fsm(self):
        self.e_state = self.E_TOKEN.IDLE
        self.s_state = ""
        self.s_number = ""
        return

    def next(self):
        self.n_index += 1

    def prev(self):
        self.n_index -= 1

    def parse_sequence( self,  s_sequence : str ) ->  List[Tuple[int, int]]:
        self.gltn_results = list()
        self.n_index = 0
        self.n_max_index = len(s_sequence)
        while self.n_index < self.n_max_index:
            #fetch character
            s_char = s_sequence[self.n_index]
            #next character
            self.next()
            logging.debug(f"Char: {s_char} | State: {self.e_state} - >{self.s_state}<")    
            #parse the character
            b_decoded = self.parse_char( s_char )

        return self.gltn_results

    def parse_char( self, s_char: str ) -> bool:

        if (self.e_state == self.E_TOKEN.IDLE):
            if (s_char == "m"):
                self.s_state = "u"
                self.e_state = self.E_TOKEN.PARSE_MUL
                logging.debug(f"match mul(X,Y) {s_char}")
            elif (s_char == "d"):
                self.s_state = "o"
                self.e_state = self.E_TOKEN.PARSE_DO
                logging.debug(f"match do() {s_char}")
            else:
                self.reset_fsm()

        elif (self.e_state == self.E_TOKEN.PARSE_MUL):
            #MATCH LETTER
            if (self.s_state == "u"):
                if (s_char == self.s_state):
                    self.s_state = "l"
                    logging.debug(f"matched character{s_char} , advance")
                else:
                    self.reset_fsm()
            #MATCH LETTER
            elif (self.s_state == "l"):
                if (s_char == self.s_state):
                    self.s_state = "("
                    logging.debug(f"matched character {s_char}, advance")
                else:
                    self.reset_fsm()
            #MATCH LETTER
            elif (self.s_state == "("):
                if (s_char == self.s_state):
                    #match number next
                    self.s_state = "X"
                    self.s_number = ""
                    logging.debug(f"matched character {s_char}, advance")
                else:
                    self.reset_fsm()
            #MATCH NUMBER
            elif (self.s_state == "X"):
                if (s_char >= "0") and (s_char <= "9"):
                    #append the value
                    self.s_number += s_char
                    logging.debug(f"detecting number {s_char} ->{self.s_number}")
                #no numbers were eaten
                elif len(self.s_number) <= 0:
                    logging.debug(f"Zero length number")
                    self.reset_fsm()
                #number is too long
                elif len(self.s_number) >= 4:
                    logging.debug(f"Number is too long")
                    self.reset_fsm()
                #parse number to int
                else:
                    self.n_arg_x = int(self.s_number)
                    logging.debug(f"Detected X {self.n_arg_x}")
                    #I need to reprocess this character
                    self.prev()
                    #next state
                    self.s_state = ","
            #MATCH LETTER
            elif (self.s_state == ","):
                if (s_char == self.s_state):
                    #match Y number next
                    self.s_state = "Y"
                    self.s_number = ""
                    logging.debug(f"matched character {s_char}, advance")
                else:
                    self.reset_fsm()
            #MATCH NUMBER
            elif (self.s_state == "Y"):
                if (s_char >= "0") and (s_char <= "9"):
                    #append the value
                    self.s_number += s_char
                    logging.debug(f"detecting number {s_char} ->{self.s_number}")
                #no numbers were eaten
                elif len(self.s_number) <= 0:
                    logging.debug(f"Zero length number")
                    self.reset_fsm()
                #number is too long
                elif len(self.s_number) >= 4:
                    logging.debug(f"Number is too long")
                    self.reset_fsm()
                #parse number to int
                else:
                    self.n_arg_y = int(self.s_number)
                    logging.debug(f"Detected Y {self.n_arg_y}")
                    #I need to reprocess this character
                    self.prev()
                    #next state
                    self.s_state = ")"
            #MATCH LETTER
            elif (self.s_state == ")"):
                if (s_char == self.s_state):
                    logging.debug(f"FINAL MATCH, VALID X: {self.n_arg_x} Y: {self.n_arg_y}")
                    if (self.b_allow_mul == False):
                        print("MUL DISALLOWED!!!")
                    else:
                        tn_mul = (self.n_arg_x,self.n_arg_y)
                        self.gltn_results.append(tn_mul)
                    self.reset_fsm()    
                else:
                    self.reset_fsm()
            else:
                logging.debug(f"ERR: Ask developer to finish the algorithm")    
                self.reset_fsm()
        elif (self.e_state == self.E_TOKEN.PARSE_DO):
            #MATCH LETTER
            if (self.s_state == "o"):
                if (s_char == self.s_state):
                    self.s_state = "("
                    logging.debug(f"matched character{s_char} , advance")
                else:
                    self.reset_fsm()
            #MATCH LETTER
            elif (self.s_state == "("):
                if (s_char == self.s_state):
                    self.s_state = ")"
                    logging.debug(f"matched character{s_char} , advance")
                #I might match the don't
                elif (s_char == "n"):
                    self.s_state = "'"
                    self.e_state = self.E_TOKEN.PARSE_DONT
                    logging.debug(f"matched character{s_char} , advance")
                else:
                    self.reset_fsm()
            #MATCH LETTER
            elif (self.s_state == ")"):
                if (s_char == self.s_state):
                    self.b_allow_mul = True
                    logging.debug(f"DO {self.b_allow_mul}")
                    self.reset_fsm()
                else:
                    self.reset_fsm()
            else:
                logging.debug(f"ERR: Ask developer to finish the algorithm")    
                self.reset_fsm()
        elif (self.e_state == self.E_TOKEN.PARSE_DONT):
            #MATCH LETTER
            if (self.s_state == "'"):
                if (s_char == self.s_state):
                    self.s_state = "t"
                    logging.debug(f"matched character{s_char} , advance")
                else:
                    self.reset_fsm()
            #MATCH LETTER
            elif (self.s_state == "t"):
                if (s_char == self.s_state):
                    self.s_state = "("
                    logging.debug(f"matched character{s_char} , advance")
                else:
                    self.reset_fsm()
            #MATCH LETTER
            elif (self.s_state == "("):
                if (s_char == self.s_state):
                    self.b_allow_mul = False
                    logging.debug(f"DONT {self.b_allow_mul}")
                    self.reset_fsm()
                else:
                    self.reset_fsm()
            else:
                logging.debug(f"ERR: Ask developer to finish the algorithm")    
                self.reset_fsm()
        else:
            logging.debug(f"ERR: Ask developer to finish the algorithm")    
            self.reset_fsm()

        return False

def parse_sequence_b( s_sequence : str ) -> List[Tuple[int, int]]:
            
    cl_parser = Parser()        

    ltn_result = cl_parser.parse_sequence( s_sequence )

    print(ltn_result)
    return ltn_result

def process_mul( iltn_args : List[Tuple[int,int]] ) -> int:
    if (len(iltn_args) <=0):
        return -1
    n_result = 0
    for tn_arg in iltn_args:
        n_result += tn_arg[0] * tn_arg[1]
    return n_result

def day_3(is_filename: str) -> bool:
    #from file load the sequence
    s_sequence = load_string( is_filename )
    print(s_sequence)
    #ltn_args = parse_sequence( s_sequence )
    ltn_args = parse_sequence_b( s_sequence )
    print(ltn_args)
    n_result = process_mul( ltn_args )
    print(f"Result of valid mul(X,Y) = {n_result}")

#--------------------------------------------------------------------------------------------------------------------------------
#   MAIN
#--------------------------------------------------------------------------------------------------------------------------------

# Example usage
gs_filename_example = 'advent_of_code\day_3_example.txt'
gs_filename_example_conditional = 'advent_of_code\day_3_example_conditional.txt'
gs_filename = 'advent_of_code\day_3.txt'
#   if interpreter has the intent of executing this file
if __name__ == "__main__":
    logging.basicConfig(
        filename='debug.log',
        # Specify the log file name
        level=logging.DEBUG,
        # Set the level of debug to show
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.debug("Begin")  
    #day_3( gs_filename_example_conditional )
    day_3( gs_filename )