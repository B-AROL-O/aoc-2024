"""
--- Day 5: Print Queue ---

Satisfied with their search on Ceres, the squadron of scholars suggests subsequently scanning the stationery stacks of sub-basement 17.

The North Pole printing department is busier than ever this close to Christmas, and while The Historians continue their search of this historically significant facility,
an Elf operating a very familiar printer beckons you over.

The Elf must recognize you, because they waste no time explaining that the new sleigh launch safety manual updates won't print correctly.
Failure to update the safety manuals would be dire indeed, so you offer your services.

Safety protocols clearly indicate that new pages for the safety manuals must be printed in a very specific order.
The notation X|Y means that if both page number X and page number Y are to be produced as part of an update, page number X must be printed at some point before page number Y.
The Elf has for you both the page ordering rules and the pages to produce in each update (your puzzle input),
but can't figure out whether each update has the pages in the right order.

For example:

47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47

The first section specifies the page ordering rules, one per line.
The first rule, 47|53, means that if an update includes both page number 47 and page number 53, then page number 47 must be printed at some point before page number 53.
(47 doesn't necessarily need to be immediately before 53; other pages are allowed to be between them.)

The second section specifies the page numbers of each update. Because most safety manuals are different, the pages needed in the updates are different too.
The first update, 75,47,61,53,29, means that the update consists of page numbers 75, 47, 61, 53, and 29.

To get the printers going as soon as possible, start by identifying which updates are already in the right order.

In the above example, the first update (75,47,61,53,29) is in the right order:

    75 is correctly first because there are rules that put each other page after it: 75|47, 75|61, 75|53, and 75|29.
    47 is correctly second because 75 must be before it (75|47) and every other page must be after it according to 47|61, 47|53, and 47|29.
    61 is correctly in the middle because 75 and 47 are before it (75|61 and 47|61) and 53 and 29 are after it (61|53 and 61|29).
    53 is correctly fourth because it is before page number 29 (53|29).
    29 is the only page left and so is correctly last.

Because the first update does not include some page numbers, the ordering rules involving those missing page numbers are ignored.

The second and third updates are also in the correct order according to the rules. Like the first update, they also do not include every page number, and so only some of the ordering rules apply - within each update, the ordering rules that involve missing page numbers are not used.

The fourth update, 75,97,47,61,53, is not in the correct order: it would print 75 before 97, which violates the rule 97|75.

The fifth update, 61,13,29, is also not in the correct order, since it breaks the rule 29|13.

The last update, 97,13,75,29,47, is not in the correct order due to breaking several rules.

For some reason, the Elves also need to know the middle page number of each update being printed.
Because you are currently only printing the correctly-ordered updates, you will need to find the middle page number of each correctly-ordered update.
In the above example, the correctly-ordered updates are:

75,47,61,53,29
97,61,53,29,13
75,29,13

These have middle page numbers of 61, 53, and 29 respectively. Adding these page numbers together gives 143.

Of course, you'll need to be careful: the actual list of page ordering rules is bigger and more complicated than the above example.

Determine which updates are already in the correct order. What do you get if you add up the middle page number from those correctly-ordered updates?
"""

"""
11470 is too high
Total Central Value: 11470 | Already Correct Central Value 5991
DAMN!! I need to accumulate just the correctly page, not fix them -.-


SCORE! I already made part two, I just need to tell the difference now
5479
"""
"""
--- Part Two ---

While the Elves get to work printing the correctly-ordered updates, you have a little time to fix the rest of them.

For each of the incorrectly-ordered updates, use the page ordering rules to put the page numbers in the right order. For the above example, here are the three incorrectly-ordered updates and their correct orderings:

    75,97,47,61,53 becomes 97,75,47,61,53.
    61,13,29 becomes 61,29,13.
    97,13,75,29,47 becomes 97,75,47,29,13.

After taking only the incorrectly-ordered updates and ordering them correctly, their middle page numbers are 47, 29, and 47. Adding these together produces 123.

Find the updates which are not in the correct order. What do you get if you add up the middle page numbers after correctly ordering just those updates?

"""



"""
Section 1
X|Y rule. X must come before Y
Section 2
update
A,B,C,D,E...
sort so that the list comply with section 1 rules
return the middle number
sum all the middle numbers
"""

"""
Algorithm
I make a dictionary to remap a number to it's ordering
I process rules
97|13
    97>1 13>2
97|61
    97>1 61>3
61|13
    collision!
    both are inside and not compliant
75|53

"""

"""
different idea.
I extract all the number that appears on the rules
I check them against the rules and move them until it complies
With a list that is compliant, I can just arrange it according to 
"""


import logging

import itertools

from typing import Dict, Tuple, List

class Order:
    """
    Class to handle ordering rules and updates, ensuring compliance and processing as needed.

    load from file a set of ordering rules and a list of updates
    check that the updates are compliant with the rules
    sort non compliant updates according to rules
    get the middle number of each compliant update
    sum all the middle numbers
    Methods:
        load_from_file(file_path): Load ordering rules and updates from a specified file.
    """
    
    def __init__(self):
        """
        Initializes the Order object with empty rules and updates lists.
        """
        self.ltn_rules = list()
        self.lln_updates = list()
        #KEY must come before all numbers in the list
        self.gd_key_before_item = dict()
        #KEY must come after all numbers in the list
        self.gd_key_after_item = dict()


    def load_from_file(self, file_path) -> bool:
        """
        Loads ordering rules and updates from a specified file. 
        
        The file should be structured with rules as "X|Y" on separate lines, and updates as comma-separated numbers on other lines.
        
        Args:
            file_path (str): The path to the file containing the rules and updates.
            
        Returns:
            None
        """
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Parse rules and updates
        self.ltn_rules = [tuple(map(int, line.strip().split('|'))) for line in lines if '|' in line]
        logging.debug(f"Rules: {len(self.ltn_rules)} | {self.ltn_rules}")
        self.lln_updates = [list(map(int, line.strip().split(','))) for line in lines if ',' in line]
        logging.debug(f"Updates: {len(self.lln_updates)} | {self.lln_updates}")

        #self.process_rules()
        self.build_prev_next()

        return False #OK

    def build_prev_next(self) -> bool:
        """
        From a set of rules, build two dictionaries
        gd_prev: NUM | KEY must come before all numbers in the list
        gd_next: NUM | KEY must come after all the numbers in the list
        """

        #scan all the rules
        for (n_prev,n_next) in self.ltn_rules:
            #the KEY must come before the items in the list
            if (n_prev not in self.gd_key_before_item):
                self.gd_key_before_item[n_prev] = [n_next]
            else:
                ln_after_key = self.gd_key_before_item[n_prev]
                ln_after_key.append(n_next)
            #the KEY must come after the items in the list
            if (n_next not in self.gd_key_after_item):
                self.gd_key_after_item[n_next] = [n_prev]
            else:
                ln_before_key = self.gd_key_after_item[n_next]
                ln_before_key.append(n_prev)

        #scan all the items (list of numbers)
        #sort all the numbers in the list for convenience
        for ln_item in self.gd_key_before_item.items():    
            ln_item[1].sort()
        for ln_item in self.gd_key_after_item.items():    
            ln_item[1].sort()

        logging.debug(f"KEY PREV {len(self.gd_key_before_item)} | {self.gd_key_before_item}")
        logging.debug(f"KEY NEXT {len(self.gd_key_after_item)} | {self.gd_key_after_item}")

        return False #OK

    def test_update(self, iln_update: List[int]) -> Tuple[bool, List[int]]:
        """
        Test an update against the rules defined in the object's dictionaries.
        I return a motion vector, indicating how many violation a number has, and in which direction
        
        Parameters:
        iln_update (List[int]): A list of integers to be tested against the rules.

        Returns:
        Tuple[bool, List[int]]: A tuple where the first element is a boolean indicating if the update is invalid,
                                and the second element is a list indicating the motion for each key.
        """

        # Log the update being tested
        logging.debug(f"Update: {iln_update}")

        # Initialize the invalid flag
        b_invalid = False

        # Create a list of zeros the size of the input list
        ln_motion = [0] * len(iln_update)

        # Scan the update
        for (n_index, n_key) in enumerate(iln_update):
            # List all numbers that come BEFORE the key
            ln_before_key = iln_update[:n_index]

            # Create a list of all numbers that come AFTER the key
            ln_after_key = iln_update[n_index+1:]

            # If the key appears in the KEY BEFORE ITEM rules
            if (n_key in self.gd_key_before_item):
                # KEY should be BEFORE those items
                ln_prev = self.gd_key_before_item[n_key]

                # List of all items that are BEFORE the key but the key should be before those items
                ln_before_but_should_be_after = set(ln_before_key) & set(ln_prev)

                if len(ln_before_but_should_be_after) > 0:
                    logging.debug(f"Number {n_key} comes after a number that should be before {ln_before_but_should_be_after}")
                    b_invalid = True
                    # This key should be moved backward
                    #move priority is the number of violation
                    ln_motion[n_index] -= len(ln_before_but_should_be_after)
                    
            # If the key appears in the KEY AFTER ITEM rules
            if (n_key in self.gd_key_after_item):
                # KEY should be AFTER those items
                ln_next = self.gd_key_after_item[n_key]

                # List of all items that are AFTER the key but the key should be after those items
                ln_after_but_should_be_before = set(ln_after_key) & set(ln_next)

                if len(ln_after_but_should_be_before) > 0:
                    logging.debug(f"Number {n_key} comes before a number that should be after {ln_after_but_should_be_before}")
                    b_invalid = True
                    # This key should be moved forward
                    #move priority is the number of violation
                    ln_motion[n_index] += len(ln_after_but_should_be_before)

        if (sum(ln_motion) != 0):
            logging.error(f"ERROR: the sum of the motion vector should be zero!")

        # Log the motion list
        logging.debug(f"Motion: {ln_motion}")

        return b_invalid, ln_motion

    def show_motion( self, iln_vector: List[int], iln_motion: List[int], s_level = "debug" ) -> bool:

        s_str = f""

        return False #OK

    def get_central_value( self, iln_update : List[int] ) -> int:
        """
        find the central value of the update
        all sequences should be odd in length
        """

        n_len = len(iln_update)
        #check length
        if (n_len == 0) or (n_len%2 ==0):
            return None
        n_central_value = iln_update[ ((n_len-1)//2)]
        logging.debug(f"Central value: {n_central_value} | Update {iln_update}")
        return n_central_value

    def swap( self, iln_vector, n_a_index, n_b_index ) -> bool:
        iln_vector[n_a_index], iln_vector[n_b_index] = iln_vector[n_b_index], iln_vector[n_a_index]
        return False

    def swap_motion( self, iln_vector, iln_motion, n_a_index, n_b_index) -> bool:
        logging.debug(f"A: {n_a_index} | B: {n_b_index} | Update: {iln_vector} | Motion: {iln_motion}")
        if (n_a_index < 0) or (n_a_index > len(iln_vector)-1):
            return True #FAIL
        if (n_b_index < 0) or (n_b_index > len(iln_vector)-1):
            return True #FAIL
        
        #swap the values
        iln_vector[n_a_index], iln_vector[n_b_index] = iln_vector[n_b_index], iln_vector[n_a_index]
        #swap the motion values
        iln_motion[n_a_index], iln_motion[n_b_index] = iln_motion[n_b_index], iln_motion[n_a_index]
        #update the motion values
        n_delta = n_b_index -n_a_index
        iln_motion[n_a_index] += n_delta
        iln_motion[n_b_index] -= n_delta
        return False #OK

    def fix_update_swap_max( self, iln_update : List[int], iln_motion : List[int] ) -> bool:
        """
        given an update, and a motion vector indicating what needs to be fixed
        rearrange the order
        in order to fix the update:
        -I need to move positive numbers forward
        -I need to move negative numbers backward

        BUG: swap max algorith is unstable
        [2024-12-07 11:49:54,717] DEBUG day_5:279 > Motion: [4, 0, -2, 0, -2, 2, -1, 3, 1, -1, -4] 
        [2024-12-07 11:49:54,717] DEBUG day_5:229 > Update: [85, 57, 15, 24, 46, 97, 19, 89, 87, 44, 98] 
        [2024-12-07 11:49:54,717] DEBUG day_5:279 > Motion: [6, 0, -2, 0, -2, 2, -1, 3, 1, -1, -6] 
        [2024-12-07 11:49:54,717] DEBUG day_5:229 > Update: [98, 57, 15, 24, 46, 97, 19, 89, 87, 44, 85]
        I need to change the algorithm.
        Can I jut do a forward pass? move motion vectors by their motion vector?
        I think it's unstable too.
        Perhaps I need to move the smallest non zero first?
        Perhaps I just need to add a loop protection to not move numbers already moved?
        For now just add a infinite loop detection
        Sequences: 200 Errors: 83
        it seems to converge majority of sequences, I'm not that far off!
        [2024-12-07 12:02:59,145] DEBUG day_5:229 > Update: [98, 85, 15, 24, 46, 97, 19, 89, 87, 44, 57] 
        [2024-12-07 12:02:59,146] DEBUG day_5:279 > Motion: [4, 5, -2, 0, -2, 2, -1, 3, 1, -1, -9] 
        [2024-12-07 12:02:59,146] DEBUG day_5:229 > Update: [98, 57, 15, 24, 46, 97, 19, 89, 87, 44, 85] 
        Looking at it, I need to move 

        Sequences: 200 Errors: 83 Already Valid: 102
        No, 102 were valid to begin with.
        of the 98 invalid, 83 failed to converge
        swap max is a garbage algorithm



        """

        def find_priority_numbers( iln_motion : List[int] ):
            # Initialize variables to store the maximum positive and negative numbers and their indices
            (n_max_positive, n_max_positive_index) = (None,-1)
            (n_max_negative, n_max_negative_index) = (None,-1)

            # Iterate through the list
            for n_index, n_value in enumerate(iln_motion):
                if n_value > 0:
                    if n_max_positive is None or n_value > n_max_positive:
                        n_max_positive = n_value
                        n_max_positive_index = n_index
                elif n_value < 0:
                    if n_max_negative is None or n_value < n_max_negative:
                        n_max_negative = n_value
                        n_max_negative_index = n_index

            return (n_max_negative_index, n_max_positive_index)

        b_continue = True

        while b_continue:
            #find number with the highest priority of being moved forward
            #find the number with the highest priority of being moved backward
            (n_max_negative_index, n_max_positive_index) = find_priority_numbers(iln_motion)
            #if I couldn't find high priority numbers to move
            if (n_max_negative_index <0) or (n_max_positive_index < 0):
                b_continue = False    
            else:
                #check that I'm moving negative backward and positive forward
                n_delta = n_max_negative_index -n_max_positive_index
                if (n_delta > 0):
                    #perform the swap
                    iln_update[n_max_negative_index], iln_update[n_max_positive_index] = iln_update[n_max_positive_index], iln_update[n_max_negative_index]
                    #update the motion vector
                    iln_motion[n_max_negative_index] += n_delta
                    iln_motion[n_max_positive_index] -= n_delta
                #swap the highest priority 
                b_continue = False  
                return True
            
                
        logging.debug(f"Update: {iln_update} | Motion: {iln_motion}")
        return False

    def fix_update_move_all_once( self, iln_update : List[int], iln_motion : List[int] ) -> bool:
        """
        I scan the motion vector once, and move the items by their motion value
        """
        for n_index in range(len(iln_motion)):
            #if the motion vector is non zero
            if (iln_motion[n_index] != 0):
                n_delta = iln_motion[n_index]
                n_target = n_index+n_delta
                b_fail = self.swap_motion( iln_update, iln_motion, n_index, n_target )
                if b_fail:
                    logging.error(f"ERROR: failed swap {n_index} {n_target}")
                    return True #Fail
                
        return False #OK

    def test_updates( self ) -> int:
        n_accumulate_central_value = 0
        n_accumulate_already_correct = 0
        n_cnt_error = 0
        n_cnt_already_valid = 0
        for ln_update in self.lln_updates:
            n_infinite_loop_protection = 3*len(ln_update)
            b_invalid, ln_motion = self.test_update(ln_update)
            if (b_invalid == False):
                n_central_value = self.get_central_value( ln_update )
                n_accumulate_already_correct += n_central_value
                n_accumulate_central_value += n_central_value
                n_cnt_already_valid += 1
            else:
                while (b_invalid == True):
                    b_fail = self.fix_update_move_all_once( ln_update, ln_motion )
                    if (b_fail == True):
                        logging.error(f"failed swap")
                        n_cnt_error += 1
                        break
                    b_invalid, ln_motion = self.test_update(ln_update)
                    n_infinite_loop_protection -= 1
                    if (n_infinite_loop_protection <= 0):
                        logging.error(f"tripped infinite loop protection!")
                        n_cnt_error += 1
                        break
                n_central_value = self.get_central_value( ln_update )
                n_accumulate_central_value += n_central_value
            
        logging.debug(f"Total Central Value: {n_accumulate_central_value} | Already Correct Central Value {n_accumulate_already_correct}")
        print(f"Total Central Value: {n_accumulate_central_value} | Already Correct Central Value {n_accumulate_already_correct}")
        print(f"Sequences: {len(self.lln_updates)} Errors: {n_cnt_error} Already Valid: {n_cnt_already_valid}")
        return int

#--------------------------------------------------------------------------------------------------------------------------------
#   MAIN
#--------------------------------------------------------------------------------------------------------------------------------

# Example usage
gs_filename_example = 'day05\day_5_example.txt'
gs_filename = 'day05\day_5_data.txt'
#   if interpreter has the intent of executing this file
if __name__ == "__main__":
    logging.basicConfig(
        filename='day05\day_5.log',
        # Specify the log file name
        level=logging.DEBUG,
        # Set the level of debug to show
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("Begin") 

    cl_order = Order()
    #cl_order.load_from_file( gs_filename_example )
    cl_order.load_from_file( gs_filename )
    cl_order.test_updates()
    
    
    