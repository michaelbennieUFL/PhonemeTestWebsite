def edit_path_with_beam_search(dist_matrix, str1, str2, beam_width=3):
    """
    Perform a beam search to find the best edit path with the lowest cost and prioritize insertions.

    Parameters:
    - dist_matrix (list of lists): The distance matrix computed from the Levenshtein distance function.
    - str1 (list of lists): Original string as a list of characters (each character in its own list).
    - str2 (list of lists): New string as a list of characters (each character in its own list).
    - beam_width (int): The number of top paths to explore at each step (default is 3). ***It must be >1.***

    Returns:
    - dict: A dictionary containing separated string versions of the original and new strings.
    """

    nrows = len(dist_matrix)
    ncols = len(dist_matrix[0])

    # Each state in the beam will store (separated_str1, separated_str2, i, j, insertions_count)
    initial_state = ([], [], nrows - 1, ncols - 1, 0)  # Initial path with no inserts
    beam = [initial_state]  # Start with the initial state

    while beam:
        next_beam = []
        for separated_str1, separated_str2, i, j, insertions in beam:
            if i == 0 and j == 0:
                # If we reach (0, 0), return the current best solution
                separated_str1.reverse()
                separated_str2.reverse()
                return {
                    "separated_str1": separated_str1,
                    "separated_str2": separated_str2
                }

            if i > 0 and j > 0:
                # Possible moves: match/substitute, delete, insert
                moves = {
                    "match_or_substitute": (i - 1, j - 1),
                    "delete": (i - 1, j),
                    "insert": (i, j - 1),
                }
                costs = {
                    "match_or_substitute": dist_matrix[i - 1][j - 1],
                    "delete": dist_matrix[i - 1][j],
                    "insert": dist_matrix[i][j - 1],
                }

                # Generate next states for each possible move
                for move, (next_i, next_j) in moves.items():
                    next_separated_str1 = separated_str1[:]
                    next_separated_str2 = separated_str2[:]
                    next_insertions = insertions

                    if move == "match_or_substitute":
                        next_separated_str1.append(str1[i - 1])
                        next_separated_str2.append(str2[j - 1])
                    elif move == "delete":
                        next_separated_str1.append(str1[i - 1])
                        next_separated_str2.append("")
                    elif move == "insert":
                        next_separated_str1.append("")
                        next_separated_str2.append(str2[j - 1])
                        next_insertions += 1

                    next_beam.append((
                        next_separated_str1, next_separated_str2, next_i, next_j, next_insertions
                    ))

            elif j > 0:  # If we're at the first row, we can only insert
                next_separated_str1 = separated_str1[:]
                next_separated_str2 = separated_str2[:]
                next_separated_str1.append("")
                next_separated_str2.append(str2[j - 1])
                next_beam.append((next_separated_str1, next_separated_str2, i, j - 1, insertions + 1))

        # Sort the beam by the distance value at the matrix position, with priority to the most insertions
        next_beam = sorted(
            next_beam,
            key=lambda x: (dist_matrix[x[2]][x[3]], -x[4])  # Prioritize lower distance and more insertions
        )

        # Keep only the top beam_width paths
        beam = next_beam[:beam_width]

    # In case we never reach (0, 0), return the last best path (fallback)
    best_path = beam[0]
    best_path[0].reverse()
    best_path[1].reverse()
    return {
        "separated_str1": best_path[0],
        "separated_str2": best_path[1]
    }


def levenshtein_distance_for_inserts(original_string="", new_string="", mismatch_cost=1, delete_insert_cost=1,
                                     beam_width=3):
    """
    Compute the Levenshtein distance while using beam search to prioritize paths with the lowest cost
    and the most insertions.

    Parameters:
    - original_string (list of lists): Original string as a list of characters (each character in its own list).
    - new_string (list of lists): New string as a list of characters (each character in its own list).
    - mismatch_cost (int): The cost of a mismatch between characters (default is 1).
    - delete_insert_cost (int): The cost of a deletion or insertion (default is 1).
    - beam_width (int): The number of top paths to explore at each step (default is 3). ***It must be >1.***

    Returns:
    - dict: A dictionary containing the best distance, the separated original string, and the separated new string.
    """

    dist_matrix = [[None] * (len(new_string) + 1) for _ in range(len(original_string) + 1)]
    for i in range(len(original_string) + 1):
        for j in range(len(new_string) + 1):
            if i == 0:
                dist_matrix[i][j] = j * delete_insert_cost
            elif j == 0:
                dist_matrix[i][j] = i * delete_insert_cost
            else:
                current_dist = 0 if original_string[i - 1] == new_string[j - 1] else mismatch_cost
                mismatch_dist = current_dist + dist_matrix[i - 1][j - 1]
                delete_dist = delete_insert_cost + dist_matrix[i - 1][j]
                insert_dist = delete_insert_cost + dist_matrix[i][j - 1]
                dist_matrix[i][j] = min(mismatch_dist, delete_dist, insert_dist)

    best_dist = dist_matrix[len(original_string)][len(new_string)]
    edit_path_result = edit_path_with_beam_search(dist_matrix, original_string, new_string, beam_width)

    return {
        "best_dist": best_dist,
        "original_string_parts": edit_path_result["separated_str1"],
        "new_string_parts": edit_path_result["separated_str2"]
    }


if __name__ == "__main__":
    # Test case 1: nɪt -> maɪt
    word1 = "nɪt"
    word2 = "maɪt"

    # Convert each word into a list of lists of characters
    word1_list = [[char] for char in word1]
    word2_list = [[char] for char in word2]

    print("Test case 1:")
    result = levenshtein_distance_for_inserts(word1_list, word2_list, beam_width=2)
    print(result)

    # Test case 2: kit -> sitting
    word3 = "kit"
    word4 = "sitting"

    word3_list = [[char] for char in word3]
    word4_list = [[char] for char in word4]

    print("\nTest case 2:")
    result2 = levenshtein_distance_for_inserts(word3_list, word4_list, beam_width=3)
    print(result2)

    # Test case 3: abc -> aec
    word5 = "abc"
    word6 = "aec"

    word5_list = [[char] for char in word5]
    word6_list = [[char] for char in word6]

    print("\nTest case 3:")
    result3 = levenshtein_distance_for_inserts(word5_list, word6_list, beam_width=3)
    print(result3)
