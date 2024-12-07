"""
STORY:
Fortunately, the first location The Historians want to search isn't a long walk from the Chief Historian's office.
While the Red-Nosed Reindeer nuclear fusion/fission plant appears to contain no sign of the Chief Historian, the engineers there run up to you as soon as they see you.
Apparently, they still talk about the time Rudolph was saved through molecular synthesis from a single electron.
They're quick to add that - since you're already here - they'd really appreciate your help analyzing some unusual data from the Red-Nosed reactor.
You turn to check if The Historians are waiting for you, but they seem to have already divided into groups that are currently searching every corner of the facility.
You offer to help with the unusual data.

The unusual data (your puzzle input) consists of many reports, one report per line.
Each report is a list of numbers called levels that are separated by spaces.
For example:
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
This example data contains six reports each containing five levels.
The engineers are trying to figure out which reports are safe.
The Red-Nosed reactor safety systems can only tolerate levels that are either gradually increasing or gradually decreasing.
So, a report only counts as safe if both of the following are true:

The levels are either all increasing or all decreasing.
Any two adjacent levels differ by at least one and at most three.
In the example above, the reports can be found safe or unsafe by checking those rules:

7 6 4 2 1: Safe because the levels are all decreasing by 1 or 2.
1 2 7 8 9: Unsafe because 2 7 is an increase of 5.
9 7 6 2 1: Unsafe because 6 2 is a decrease of 4.
1 3 2 4 5: Unsafe because 1 3 is increasing but 3 2 is decreasing.
8 6 4 4 1: Unsafe because 4 4 is neither an increase or a decrease.
1 3 6 7 9: Safe because the levels are all increasing by 1, 2, or 3.
So, in this example, 2 reports are safe.

Analyze the unusual data from the engineers. How many reports are safe?
"""

"""
The engineers are surprised by the low number of safe reports until they realize they forgot to tell you about the Problem Dampener.

The Problem Dampener is a reactor-mounted module that lets the reactor safety systems tolerate a single bad level in what would otherwise be a safe report. It's like the bad level never happened!

Now, the same rules apply as before, except if removing a single level from an unsafe report would make it safe, the report instead counts as safe.

More of the above example's reports are now safe:
"""




"""
Algorithm
-rows are reports, col/elements are levels
-Open a file, and get a list of levels
    -check that levels comply with the rule
    -if so, add 1 to safe reports, otherwise add 1 to unsafe report
-safety rule
    -unsafe if delta level/next level changes sign
    -unsafe if delta exceed 4
    -unsafe if delta is exactly zero
-grace exceedance
    -try to remove one level and rerun?
"""

from typing import Tuple, List

def is_report_unsafe( iln_levels : List[int] ) -> bool:
    #memory of previous number
    n_old = 0
    #delta between numbers
    n_delta = 0
    n_cnt_positive = 0
    n_cnt_negative = 0
    n_cnt_overflow = 0
    n_cnt_zero = 0

    #scan numbers
    for n_index,n_value in enumerate(iln_levels):
        #exception for first value
        if (n_index == 0):
            pass
        #from second value start computing delta
        else:
            #compute new delta
            n_delta = n_value - n_old
            if (n_delta > 0):
                n_cnt_positive += 1
            if (n_delta < 0):
                n_cnt_negative += 1
            if (n_delta == 0):
                n_cnt_zero += 1
            if abs(n_delta) > 3:
                n_cnt_overflow += 1
            
        #memory
        n_old = n_value

    #count number of exceedances, if exceedances are exactly 1, it's safe
    n_cnt_violations = n_cnt_overflow + min(abs(n_cnt_positive),abs(n_cnt_negative)) +n_cnt_zero
    print(f"Levels: {iln_levels} Violations: {n_cnt_violations} | Overflow: {n_cnt_overflow} Sign: +{n_cnt_positive} | -{n_cnt_negative} Stationary: {n_cnt_zero}")

    #it's unsafe because of overflow rule
    if (n_cnt_overflow > 0):
        print(f"violate overflow rule: {n_cnt_overflow}")
        return True

    #it's unsafe because of sign change rule
    if (n_cnt_positive > 0) and (n_cnt_negative > 0):
        print(f"violate sign change rule: {n_cnt_positive} {n_cnt_negative}")
        return True
    
    if (n_cnt_zero > 0):
        print(f"violate no change rule: {n_cnt_zero}")
        return True
    
    #it's safe
    return False

import copy # Original list with nested elements original_list = [1, 2, [3, 4], 5] # Create a deep copy of the list copied_list = 

def remove_one_level( iln_levels : List[int] ) -> bool:
    #scan the report for all levels
    for n_index,n_value in enumerate(iln_levels):
        #create a deep copy
        ln_levels_copy = copy.deepcopy(iln_levels)
        #remove this level
        del ln_levels_copy[n_index]
        #rerun the unsafe detection on this list
        b_result = is_report_unsafe( ln_levels_copy )
        if (b_result == False):
            print(f"Report made safe by removing element: {n_value} index: {n_index}")
            return False

def day_2( is_filename: str ):
    n_cnt_report = 0
    n_cnt_safe = 0
    n_cnt_unsafe = 0
    n_cnt_safe_removing_level = 0
    with open(is_filename, 'r') as c_file:
        #scan the file and get a line string
        for s_line in c_file:
            n_cnt_report += 1
            #list of levels in a report
            ls_level = []
            ln_level = []
            #split the string into a list of string levels
            ls_level = s_line.split()
            #create a list of int levels from that list of strings
            for s_level in ls_level:
                ln_level.append(int(s_level))
            b_result = is_report_unsafe(ln_level)
            if (b_result == False):
                n_cnt_safe += 1
            else:
                #if unsafe, I can try to remove a level
                b_result = remove_one_level( ln_level )
                #b_result, n_index_first_violation = is_report_unsafe(ln_level)
                if (b_result == False):
                    n_cnt_safe_removing_level += 1
                else:
                    n_cnt_unsafe += 1
            
    print(f"Total reports: {n_cnt_report} | Safe reports: {n_cnt_safe} | Safe after removing one unsafe level: {n_cnt_safe_removing_level} Total: {n_cnt_safe+n_cnt_safe_removing_level} | Unsafe reports: {n_cnt_unsafe}")


#--------------------------------------------------------------------------------------------------------------------------------
#   MAIN
#--------------------------------------------------------------------------------------------------------------------------------

# Example usage
gs_filename_example = 'advent_of_code\day_2_example.csv'
gs_filename = 'advent_of_code\day_2.csv'
#   if interpreter has the intent of executing this file
if __name__ == "__main__":
    day_2( gs_filename_example )
    day_2( gs_filename )
