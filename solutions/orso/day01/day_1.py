"""
You haven't even left yet and the group of Elvish Senior Historians has already hit a problem: their list of locations to check is currently empty.
Eventually, someone decides that the best place to check first would be the Chief Historian's office.

Upon pouring into the office, everyone confirms that the Chief Historian is indeed nowhere to be found.
Instead, the Elves discover an assortment of notes and lists of historically significant locations!
This seems to be the planning the Chief Historian was doing before he left.
Perhaps these notes can be used to determine which locations to search?
Throughout the Chief's office, the historically significant locations are listed not by name but by a unique number called the location ID.
To make sure they don't miss anything, The Historians split into two groups, each searching the office and trying to create their own complete list of location IDs.
There's just one problem: by holding the two lists up side by side (your puzzle input), it quickly becomes clear that the lists aren't very similar.
Maybe you can help The Historians reconcile their lists?

For example:
3   4
4   3
2   5
1   3
3   9
3   3
Maybe the lists are only off by a small amount! To find out, pair up the numbers and measure how far apart they are.
Pair up the smallest number in the left list with the smallest number in the right list, then the second-smallest left number with the second-smallest right number, and so on.
Within each pair, figure out how far apart the two numbers are; you'll need to add up all of those distances.

For example, if you pair up a 3 from the left list with a 7 from the right list, the distance apart is 4; if you pair up a 9 with a 3, the distance apart is 6.

In the example list above, the pairs and distances would be as follows:
The smallest number in the left list is 1, and the smallest number in the right list is 3. The distance between them is 2.
The second-smallest number in the left list is 2, and the second-smallest number in the right list is another 3. The distance between them is 1.
The third-smallest number in both lists is 3, so the distance between them is 0.
The next numbers to pair up are 3 and 4, a distance of 1.
The fifth-smallest numbers in each list are 3 and 5, a distance of 2.
Finally, the largest number in the left list is 4, while the largest number in the right list is 9; these are a distance 5 apart.
To find the total distance between the left list and the right list, add up the distances between all of the pairs you found.
In the example above, this is 2 + 1 + 0 + 1 + 2 + 5, a total distance of 11!

Your actual left and right lists contain many location IDs. What is the total distance between your lists?

To begin, get your puzzle input.
"""


"""
rt Two ---
Your analysis only confirmed what everyone feared: the two lists of location IDs are indeed very different.

Or are they?

The Historians can't agree on which group made the mistakes or how to read most of the Chief's handwriting, but in the commotion you notice an interesting detail: a lot of location IDs appear in both lists! Maybe the other numbers aren't location IDs at all but rather misinterpreted handwriting.

This time, you'll need to figure out exactly how often each number from the left list appears in the right list.
Calculate a total similarity score by adding up each number in the left list after multiplying it by the number of times that number appears in the right list.

Here are the same example lists again:

3   4
4   3
2   5
1   3
3   9
3   3
For these example lists, here is the process of finding the similarity score:

The first number in the left list is 3. It appears in the right list three times, so the similarity score increases by 3 * 3 = 9.
The second number in the left list is 4. It appears in the right list once, so the similarity score increases by 4 * 1 = 4.
The third number in the left list is 2. It does not appear in the right list, so the similarity score does not increase (2 * 0 = 0).
The fourth number, 1, also does not appear in the right list.
The fifth number, 3, appears in the right list three times; the similarity score increases by 9.
The last number, 3, appears in the right list three times; the similarity score again increases by 9.
So, for these example lists, the similarity score at the end of this process is 31 (9 + 4 + 0 + 0 + 9 + 9).

Once again consider your left and right lists. What is their similarity score?
"""

print("Day 1")

from typing import Tuple, List

def load_location_ids(is_filename: str) -> Tuple[List[int], List[int]]:
    """
    Load location IDs from a file into two separate lists.

    :param filename: The name of the file containing the location IDs.
    :return: A tuple of two lists containing the location IDs.
    """
    ln_left = []
    ln_right = []

    with open(is_filename, 'r') as c_file:
        for s_line in c_file:
            s_left, s_right = s_line.split()
            ln_left.append(int(s_left))
            ln_right.append(int(s_right))

    return ln_left, ln_right

def save_list_to_file(iln_data: List[int], is_filename: str) -> None:
    """
    Save a list of integers to a file.

    :param data: The list of integers to save.
    :param filename: The name of the file to save the data to.
    """
    with open(is_filename, 'w') as file:
        for n_value in iln_data:
            file.write(f"{n_value}\n")


def compute_frequency( iln_values: List[int] ) -> dict:
    
    d_frequency = dict()
    for n_value in iln_values:
        if n_value in d_frequency:
            d_frequency[n_value] += 1
        else:
            d_frequency[n_value] = 1
    return d_frequency

def compute_similarity_score( iln_left: List[int], iln_right: List[int]) -> int:
    """
    for each number on the right list, i multiply it by the times it appear on the right list
    """
    d_left = compute_frequency(iln_left)
    d_right = compute_frequency(iln_right)
    print(f"frequency left {d_left} | {d_right}")
    n_similarity = 0
    for n_value in d_left:
        if (n_value in d_right):
            n_sum = n_value *d_left[n_value] *d_right[n_value]
            #print(f"{n_sum}")
            n_similarity += n_sum
            
    return n_similarity

def day_1( is_filename: str ) -> int:
    """
    :param filename: The name of the file containing the location IDs.

    ALGORITHM:
    1) sort the two lists
    2) element by element, find the difference and build a list of differences
    3) sum all elements
    """

    #extract the left and right numbers as lists
    ln_left, ln_right = load_location_ids( is_filename )
    ln_left.sort()
    ln_right.sort()

    print("Left list: ", ln_left)
    print("Right list: ", ln_right)

    ln_result = list()
    #element by element, compute the difference into the result string
    for n_left, n_right in zip(ln_left, ln_right):
        ln_result.append( abs( n_left - n_right ) )

    n_result = sum(ln_result)

    save_list_to_file( ln_result, gs_filename_result )

    print(f"Result list: {ln_result} Result: {n_result}")

    n_similarity = compute_similarity_score( ln_left, ln_right )

    print(f"similarity score: {n_similarity}")
    return n_result

#--------------------------------------------------------------------------------------------------------------------------------
#   MAIN
#--------------------------------------------------------------------------------------------------------------------------------

# Example usage
gs_filename_example = 'day01\day_1_example.csv'
gs_filename = 'day01\day_1.csv'
gs_filename_result = 'day01\day_1_result.csv'
#   if interpreter has the intent of executing this file
if __name__ == "__main__":
    day_1( gs_filename_example )
    day_1( gs_filename )