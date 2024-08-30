from pickle import FALSE

import panphon
import random

ft = panphon.FeatureTable()


def _select_random_indices(matrix, n, valid_columns=[2, 4, 6, 8, 9, 11, 15, 16, 17, 18, 21,22,23]):
    # 找出所有的有效非零值索引
    non_zero_indices = [(i, j) for i, row in enumerate(matrix) for j in valid_columns if row[j] != 0]

    # 確保非零值索引數量不小於需要選擇的數量
    if len(non_zero_indices) < n:
        raise ValueError("Non-zero indices are fewer than the number of indices to select")

    # 將非零值索引按照行分組
    rows_dict = {}
    for idx in non_zero_indices:
        row_idx = idx[0]
        if row_idx not in rows_dict:
            rows_dict[row_idx] = []
        rows_dict[row_idx].append(idx)

    # 將所有行進行排序，以便於均勻選擇
    sorted_rows = sorted(rows_dict.keys())

    # 隨機選擇 n 個非零值索引，確保行上均勻分佈
    selected_indices = []
    for _ in range(n):
        while True:
            # 從排序好的行中隨機選擇一行
            row_idx = random.choice(sorted_rows)
            if rows_dict[row_idx]:
                # 如果該行有非零值索引可選，則選取一個並將其從該行的索引列表中移除
                selected_idx = random.choice(rows_dict[row_idx])
                rows_dict[row_idx].remove(selected_idx)
                selected_indices.append(selected_idx)
                break
            else:
                # 如果該行沒有可選的非零值索引，從可選行列表中移除該行
                sorted_rows.remove(row_idx)
    print(selected_indices)
    return selected_indices

def update(matrix, random_indices, edit_vector):
    assert len(edit_vector) == len(random_indices)

    for idx, (i, j) in enumerate(random_indices):
        matrix[i][j] = edit_vector[idx] * matrix[i][j]
    return matrix


def generate_equally_phonetically_spaced_words(self, word: str, num_words: int, hamming_distance=4) -> list[str]:
    #hamming distance must be even

    # Generate the list of what value should be different
    # For example, for the three phone word /fat/ with a hamming distance of 4 between
    # any word, we can choose four arbitrary values to manipulate and label them as such:
    # to be written

    if num_words < 2:
        return [word]

    word_vector = ft.word_to_vector_list(word, numeric=True)

    number_of_values_to_change = hamming_distance // 2 *num_words

    indicies_to_change = _select_random_indices(word_vector, number_of_values_to_change)

    results = [word]



    word_index:int=0
    print(word_vector)
    results.append(ft.vector_list_to_word(word_vector, fuzzy_search=True))
    while word_index < num_words-1:
        # vector storing which values to flip
        offset = hamming_distance // 2 * word_index
        change_vector = [-1 if offset<=i < hamming_distance+offset else 1 for i in range(number_of_values_to_change)]

        word_vector = update(word_vector, indicies_to_change, change_vector)
        results.append(ft.vector_list_to_word(word_vector,fuzzy_search=True))
        print(word_vector)
        word_index+=1

    return results








results = generate_equally_phonetically_spaced_words(0,u'abʸɛn',5, hamming_distance=2)

for r in results:
    print(r)
