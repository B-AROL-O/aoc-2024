#--------------------------------------------------------------------------------------------------------------------------------
#   INCLUDE
#--------------------------------------------------------------------------------------------------------------------------------

import logging

from itertools import product

import copy

from typing import Generator, Dict, Tuple, List

#--------------------------------------------------------------------------------------------------------------------------------
#   RULES
#--------------------------------------------------------------------------------------------------------------------------------

"""
Rules:
-You have a result
-You have a list of arguments
-In between arguments you can insert either + or *
-Arguments are evaluated STRICTLY left to right
    81 + 40 * 27
        81+40 = 121
    121 * 27 = 3267
Objective:
-Find the equations that can be made true
-Sum the result of the equations that can be made true
"""

#--------------------------------------------------------------------------------------------------------------------------------
#   ALGORITHM
#--------------------------------------------------------------------------------------------------------------------------------

"""
Can I just try all combinations of operators?
Better, I start with MUL. If it overflow, demote to PLUS?
"""


#--------------------------------------------------------------------------------------------------------------------------------
#   MAIN
#--------------------------------------------------------------------------------------------------------------------------------

class Operator_finder:
    class Equation:
        n_result : int = 0
        n_num_arg : int = 0
        ln_arguments : List[int] = list()
        s_operators : str = str()
        #PLUS and MUL
        #cs_operations = "+*"
        #PLUS MUL AND PIPE
        cs_operations = "+*|"

        def set( self, in_result: int, iln_argument : List[int] ) -> bool:
            self.n_result = in_result
            self.ln_arguments = iln_argument
            self.n_num_arg = len(iln_argument)
            return False #OK

        def generate_operators(self, in_num_operators) -> List[List[str]]:
            """
            Knowing the number of arguments
            I generate all possible combination of operators
            """
            if in_num_operators <= 0:
                return list() #FAIL
            combinations = list(product("{self.cs_operations}", repeat=in_num_operators))
            lln_operators = [''.join(combo) for combo in combinations]
            
            return lln_operators
        
        def operation_generator(self, in_num_operators) -> Generator[str, None, None]:
            """
            generator that will give a new operator combination every time it is called
            """     

            if in_num_operators <= 0:
                return list() #FAIL
            
            combinations = list(product(f"{self.cs_operations}", repeat=in_num_operators))
            for combo in combinations:
                yield ''.join(combo)
            
            return list() #FAIL

        def show(self):
            s_str = f"Result: {self.n_result} | Arguments: "
            for n_arg in self.ln_arguments:
                s_str += f"{n_arg} - "
            logging.debug(f"{s_str}")

        def evaluate(self, s_operators : str ) -> int:
            """
            the equation will b evaluated using the operators given

            """
            n_len_arg = len(self.ln_arguments)
            n_len_op = len(s_operators)
            if (n_len_arg != n_len_op +1):
                logging.error(f"ERROR: inconsistent length: arguments: {n_len_arg} operators: {n_len_op}")
                return -1
            
            #initialize accumulator
            n_accumulator = self.ln_arguments[0]
            for n_index, s_operator in enumerate(s_operators):
                if s_operator == "+":
                    n_accumulator += self.ln_arguments[n_index+1]
                elif s_operator == "*":
                    n_accumulator *= self.ln_arguments[n_index+1]
                #pipe operator will concatenate a number of arguments to the accumulator
                elif s_operator == "|":
                    s_concatenate = f"{n_accumulator}{self.ln_arguments[n_index+1]}"
                    n_accumulator = int(s_concatenate)
                else:
                    logging.error("ERROR: invalid operator {s_operator}")
                    return 0
            return n_accumulator

        def solve(self) -> bool:
            """
            ask this equation to solve itself
            return True mean FAIL
            retunrr False mean found a solution
            the solution is in the operator list
            """

            #create an operator generator

            #print(st_equation.generate_operators(st_equation.n_num_arg))

            if self.n_num_arg <= 1:
                return True #FAIL
            #Create a generator that will spit out the next combo of opetrators
            gen_operators = self.operation_generator(self.n_num_arg -1)

            b_continue = True
            while b_continue:
                try:
                    s_operation = next(gen_operators)
                    n_result = self.evaluate( s_operation )
                    logging.debug(f"Operators: {s_operation} -> Result: {n_result} Expected Result: {self.n_result}")
                    if n_result == self.n_result:
                        self.s_operators = s_operation
                        return False #Found solution
                except StopIteration:
                    b_continue = False  #solution not found           
            return True #FAIL  

        def get_equation_string(self)->str:
            """
            generate a string of the equation: "5=3+2"
            """
            if len(self.s_operators) <= 0:
                return str()
            s_result = f"{self.n_result}={self.ln_arguments[0]}"
            for n_index, s_operator in enumerate(self.s_operators):
                s_result += f" {s_operator} {self.ln_arguments[n_index+1]}"
            logging.debug(f"{s_result}")
            return s_result

    def __init__(self):
        """
        Initialize the Patrol_route class
        """
        self.glst_equation : List[self.Equation]= list()

    def load_equations(self, s_filename: str):
        """
        Load equations from a file and populate the lst_equation list
        """
        with open(s_filename, 'r') as file:
            for line in file:
                parts = line.split(':')
                n_result = int(parts[0].strip())
                ln_arguments = list(map(int, parts[1].split()))
                st_equation = self.Equation()
                st_equation.set(n_result, ln_arguments)
                self.glst_equation.append( st_equation )

    def show(self):
        for st_equation in self.glst_equation:
            st_equation.show()

    def solve(self) -> int:
        n_accumulator_result = 0
        for n_index, st_equation in enumerate(self.glst_equation):
            print(f"solving {n_index} of {len(self.glst_equation)}")
            logging.debug("SOLVE:")
            st_equation.show()
            b_fail = st_equation.solve()
            if (b_fail == False):
                n_accumulator_result += st_equation.n_result
                logging.debug(f"SOLUTION: {st_equation.s_operators} {st_equation.n_result} -> Accumulator: {n_accumulator_result}")
            else:
                logging.debug(f"NOT SOLVABLE:")
        return n_accumulator_result
    
    def save_results( self, s_filename : str ) -> bool:
        try:
            with open(s_filename, 'w') as file:
                for st_equation in self.glst_equation:
                    s_equation = st_equation.get_equation_string()
                    print(s_equation)
                    if (len(s_equation) > 0):
                        file.write(s_equation + '\n')
        except Exception as e:
            logging.error(f"Save Failed: {e}")

#--------------------------------------------------------------------------------------------------------------------------------
#   MAIN
#--------------------------------------------------------------------------------------------------------------------------------

# Example usage
#gs_filename_output = 'day07\day_7_map_output.txt'
gs_filename_example = 'day07\day_7_example.txt'
gs_filename_data = 'day07\day_7_data.txt'
#   if interpreter has the intent of executing this file
if __name__ == "__main__":
    logging.basicConfig(
        filename='day07\day_7.log',
        # Specify the log file name
        level=logging.DEBUG,
        # Set the level of debug to show
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("Begin") 

    cl_operator_finder = Operator_finder()
    #cl_operator_finder.load_equations(gs_filename_example)
    cl_operator_finder.load_equations(gs_filename_data)
    cl_operator_finder.show()
    n_accumulator_result = cl_operator_finder.solve()
    #cl_operator_finder.save_results('day07\day_7_output_part_1.txt')
    cl_operator_finder.save_results('day07\day_7_output_part_2.txt')
    print(f"accumulator: {n_accumulator_result}")