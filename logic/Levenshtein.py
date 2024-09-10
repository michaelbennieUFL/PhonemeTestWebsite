def edit_path(dist_matrix, str1, str2):
    separated_str1 = []
    separated_str2 = []
    nrows = len(dist_matrix)
    ncols = len(dist_matrix[0])


    i, j = nrows - 1, ncols - 1

    while i >= 1 and j >= 1:
        moves = {
            "m": (i - 1, j - 1),
            "d": (i - 1, j),
            "i": (i, j - 1),
        }
        costs = {
            "m": dist_matrix[i - 1][j - 1],
            "d": dist_matrix[i - 1][j],
            "i": dist_matrix[i][j - 1],
        }
        best_move = min(costs, key=costs.get)
        best_position = moves[best_move]
        if best_move == "m":
            separated_str1.append(str1[i - 1])
            separated_str2.append(str2[j - 1])
        elif best_move == "d":
            separated_str1.append(str1[i - 1])
            separated_str2.append("")
        elif best_move == "i":
            separated_str2.append(str2[j - 1])
            separated_str1.append("")
        i, j = best_position

    separated_str1.reverse()
    separated_str2.reverse()
    return {
        "separated_str1": separated_str1,
        "separated_str2": separated_str2
    }

def levenshtein_distance(original_string="", new_string="", mismatch_cost=1, delete_insert_cost=1, ):
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
    edit_path_result = edit_path(dist_matrix, original_string, new_string)

    return {
        "best_dist": best_dist,
        "original_string_parts": edit_path_result["separated_str1"],
        "new_string_parts": edit_path_result["separated_str2"]
    }
