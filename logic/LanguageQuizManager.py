import os.path
import random
import statistics

from iso639 import Lang
from iso639.exceptions import InvalidLanguageValue, DeprecatedLanguageValue
import panphon.distance
import panphon.segment
from logic.DataHandler import SingleWordDataHandler
from logic.Levenshtein import levenshtein_distance

class Tester:
    def __init__(self, handler=SingleWordDataHandler()):
        """
        Initializes the Tester class.

        :param handler: An instance of SingleWordDataHandler, default is SingleWordDataHandler().
        """
        self.handler = handler
        self.distance = panphon.distance.Distance()
        self.ft = panphon.featuretable.FeatureTable()

    def list_languages_with_full_names(self) -> list:
        """
        Lists languages with their full names.

        :returns: A list of tuples where each tuple contains the language code and its full name.
        """
        languages = self.handler.list_languages()
        full_names = []
        for lang in languages:
            try:
                lang_obj = Lang(lang)
                full_name = lang_obj.name
            except InvalidLanguageValue:
                full_name = "Unknown"

                print("failed unknown: ",lang)
            except DeprecatedLanguageValue:

                if lang == "ajp":
                    # TODO: merge ajp with apc according to https://iso639-3.sil.org/sites/iso639-3/files/change_requests/2022/2022-006.pdf
                    full_name="South Levantine Arabic"
                else:
                    print("failed: ", lang, lang_obj)
                    full_name = lang_obj.name

            full_names.append((lang, full_name))
        return full_names

    def list_all_samples(self, selected_languages=None) -> list:
        """
        Lists all samples with their transcriptions.

        :param selected_languages: Optional list of language ISO codes to filter the samples.
        :returns: A list of tuples containing language code, full name, WAV file name, strict transcription, and loose transcription.
        """
        all_samples = []
        languages = self.handler.list_languages()

        for lang in languages:
            if selected_languages and lang not in selected_languages:
                continue

            try:
                lang_obj = Lang(lang)
                full_name = lang_obj.name
            except InvalidLanguageValue:
                full_name = "Unknown"
            except DeprecatedLanguageValue:
                full_name = lang_obj.name

            wav_files = self.handler.list_wav_files(lang)
            for wav_file in wav_files:
                wav_path, strict_transcription = self.handler.get_transcription(
                    lang, wav_file, transcription_type='strict')
                _, loose_transcription = self.handler.get_transcription(
                    lang, wav_file, transcription_type='loose')
                all_samples.append(
                    (lang, full_name, wav_file, strict_transcription, loose_transcription))

        all_samples.sort(key=lambda x: (x[0], x[2]))
        return all_samples

    def play_audio(self, languages=None, language=None, file_name: str = "") -> tuple:
        """
        Plays an audio file and returns its name and transcription.

        :param languages: List of selected languages.
        :param language: The language code of the audio file to play. If not provided, a random one will be chosen.
        :param file_name: The name of the audio file to play. If not provided, a random file will be chosen.
        :returns: A tuple containing the audio file name and its transcription.
        """
        if not languages and not language:
            language = random.choice(self.handler.list_languages())
        elif not language:
            language = random.choice(languages)
        if file_name:
            return self.handler.play_specific_audio(language, file_name)
        else:
            return self.handler.play_random_audio(language)

    def calculate_distance(self, input_string: str, language: str, wav_file: str, strict: bool = True) -> tuple:
        """
        Calculates the phonetic distance and accuracy between an input string and a reference transcription.

        :param input_string: The input string to compare.
        :param language: The language code of the reference transcription.
        :param wav_file: The WAV file name of the reference transcription.
        :param strict: A boolean indicating whether to use strict or loose transcription. Default is True (strict).
        :returns: A tuple containing the phonetic distance and the accuracy percentage.
        """
        transcription_type = 'strict' if strict else 'loose'
        _, reference_transcription = self.handler.get_transcription(language, wav_file, transcription_type)
        distance = self.distance.dolgo_prime_distance(input_string, reference_transcription) * 1 / 3 \
                   + self.distance.hamming_feature_edit_distance(input_string, reference_transcription)

        max_length = max(len(input_string), len(reference_transcription))
        accuracy = max((1 - distance / max_length) * 100, 0)
        return distance, accuracy

    def _select_random_indices(self, matrix, n, valid_columns=[4, 6, 8, 9, 15, 16, 17, 18,20,22, 23], include_zeroes=False):
        useable_indicies = [(i, j) for i, row in enumerate(matrix)
                            for j in valid_columns
                            if row[j] != 0 or include_zeroes]

        if len(useable_indicies) < n:
            raise ValueError("Non-zero indices are fewer than the number of indices to select")

        rows_dict = {}
        for idx in useable_indicies:
            row_idx = idx[0]
            if row_idx not in rows_dict:
                rows_dict[row_idx] = []
            rows_dict[row_idx].append(idx)

        sorted_rows = sorted(rows_dict.keys())

        selected_indices = []
        for _ in range(n):
            while True:
                row_idx = random.choice(sorted_rows)
                if rows_dict[row_idx]:
                    selected_idx = random.choice(rows_dict[row_idx])
                    rows_dict[row_idx].remove(selected_idx)
                    selected_indices.append(selected_idx)
                    break
                else:
                    sorted_rows.remove(row_idx)
        print(selected_indices)
        return selected_indices

    def _update_ft(self, matrix, random_indices, edit_vector):
        assert len(edit_vector) == len(random_indices)

        for idx, (i, j) in enumerate(random_indices):
            matrix[i][j] = edit_vector[idx] * matrix[i][j]
        return matrix

    def _modify_random_index(self,word_vector):
        # 隨機選擇一個行和列的索引
        row = random.randint(0, len(word_vector) - 1)
        col = random.randint(0, len(word_vector[0]) - 1)

        # 隨機選擇 -1, 0, 或 1
        new_value = random.choice([-1, 0, 1])

        # 將選定的值賦予矩陣中選中的位置
        word_vector[row][col] = new_value

        return word_vector

    def generate_equally_phonetically_spaced_words(self, word: str, num_words: int, hamming_distance=2) -> list[str]:
        if num_words < 2:
            return [word]

        word_vector = self.ft.word_to_vector_list(word, numeric=True)

        number_of_values_to_change = hamming_distance // 2 * num_words
        print("word:",word)
        try:
            indicies_to_change = self._select_random_indices(word_vector, number_of_values_to_change)
        except ValueError:
            indicies_to_change = self._select_random_indices(word_vector, number_of_values_to_change, include_zeroes=True)
        results = [word]

        #used if there arent enough indicies to change
        for i, j in indicies_to_change:
            if word_vector[i][j] == 0:
                word_vector[i][j] = random.choice([-1, 1])

        word_index: int = 0
        while word_index < num_words - 1:
            offset = hamming_distance // 2 * word_index
            change_vector = [-1 if offset <= i < hamming_distance + offset else 1 for i in
                             range(number_of_values_to_change)]

            word_vector = self._update_ft(word_vector, indicies_to_change, change_vector)
            generated_word=self.ft.vector_list_to_word(word_vector, fuzzy_search=True)
            i:int=0
            while generated_word in results and i<128:
                modified_word_vector= self._modify_random_index(word_vector)
                generated_word = self.ft.vector_list_to_word(modified_word_vector, fuzzy_search=True)
                print(generated_word,"failed",i)
                i+=1
            results.append(generated_word)
            word_index += 1

        return results

    def generate_words_for_question(self, number=10, selected_languages=None) -> list:
        """
        Generates a specified number of random questions from the available languages.

        :param number: The number of questions to generate. Default is 10.
        :param selected_languages: List of selected languages.
        :returns: A list of generated questions.
        """
        if not isinstance(number, int) or number < 1:
            return []

        all_samples = self.list_all_samples(selected_languages)
        if len(all_samples) < number:
            raise ValueError("Not enough samples to generate the requested number of questions.")

        questions = random.sample(all_samples, number)
        return questions

    def get_multiple_choice_question(self,  question: str, number_of_answers=1,hamming_distance = 2) -> list:
        number_of_words = number_of_answers
        word = question[3]
        word = self.ft.standardize_tones(word)
        options = self.generate_equally_phonetically_spaced_words(word, num_words=number_of_words, hamming_distance=hamming_distance)
        return options

    def check_answer(self,  answer: str, question: list, multiple_choice=False) -> float:
        distance = self.calculate_distance(answer, question[0], question[2])[1]
        if multiple_choice:
            distance = 100 * (distance > 99)
        return distance

    def get_average_score(self, answers: list) -> float:
        if not answers:
            return 0
        return statistics.mean(answers)

    def get_standard_deviation(self, answers: list) -> float:
        if not answers:
            return 0
        return statistics.stdev(answers) if len(answers) > 1 else 0

    def generate_segment_list(self,ipa_word:str)->list[str]:
        standardized_tone_word = self.ft.standardize_tones(ipa_word)
        ipa_segments = self.ft.ipa_segs(standardized_tone_word)
        return ipa_segments

    def get_fill_in_the_blank_question(self, question: str, number_of_answers=1, hamming_distance=2) -> list:
        ipa_segments=self.generate_segment_list(question[3])
        number_of_letters_to_blank = max((len(ipa_segments) -1) // 2 + 1, 1)
        start_blank_index = random.randint(0, len(ipa_segments) - number_of_letters_to_blank)
        end_index = start_blank_index + number_of_letters_to_blank

        selected_section_to_blank = ipa_segments[start_blank_index:end_index]

        # 將 `selected_section_to_blank` 合併為一個字串
        selected_section_to_blank_str = ''.join(selected_section_to_blank)

        # 使用切片拼接成新的字串
        question_word_with_blank = (
                ''.join(ipa_segments[:start_blank_index]) +
                " " * number_of_letters_to_blank +
                ''.join(ipa_segments[end_index:])
        )

        blank_options = self.generate_equally_phonetically_spaced_words(
            selected_section_to_blank_str,  # 這裡使用合併後的字串
            num_words=number_of_answers,
            hamming_distance=hamming_distance
        )

        blank_options=[':'.join(self.generate_segment_list(word)) for word in blank_options]
        return question_word_with_blank, blank_options

    def get_organize_sounds_question(self,question: str, number_of_answers=1,hamming_distance = 2)->list:
        question_word = question[4]
        correct_options=question_word.split(" ")
        options=correct_options

        random_indicies = random.sample(range(len(correct_options)), min(len(correct_options), 3+random.randrange(0,3)))

        for index in random_indicies:
            options=options+(self.generate_equally_phonetically_spaced_words(correct_options[index], num_words=number_of_answers, hamming_distance=hamming_distance))[1:]

        return correct_options,question_word,options


    def generate_questions(self,selected_languages,number=5,question_types=['fill_in_the_blank', 'multiple_choice', 'organize_sounds']) -> list[dict[str]]:
        selected_words = self.generate_words_for_question(number, selected_languages)
        questions = []
        for question in selected_words:

            question_type = random.choice(question_types)

            match question_type:
                case 'multiple_choice':
                    answer_choices=self.get_multiple_choice_question(question,number_of_answers=6,hamming_distance=2)
                    correct_answer = answer_choices[0]
                    word_to_find = correct_answer
                case 'fill_in_the_blank':
                    word_to_find, answer_choices=self.get_fill_in_the_blank_question(question,number_of_answers=6,hamming_distance=2)
                    correct_answer=answer_choices[0]
                case 'organize_sounds':
                    correct_answer,word_to_find, answer_choices=self.get_organize_sounds_question(question,number_of_answers=3,hamming_distance=2)

            formatted_question={
                "language_id" :question[0],
                "language_name" : question[1],
                "audio_path": os.path.join( "phoneticData",question[0],"audio",question[2]),
                "question_type" : question_type,
                "word_to_find": word_to_find,
                "correct_answer" : correct_answer,
                "answer_choices": answer_choices,
                "user_answer":"",
                "percent_correct":''
            }
            questions.append(formatted_question)
        return questions

    def calculate_consonat_vowel_errors(self, correct_word: str, incorrect_word: str) -> tuple[dict[str:dict]]:
        consonant_errors = {}
        vowel_errors = {}

        correct_feature_table = self.ft.word_to_vector_list(correct_word, numeric=True)
        incorrect_feature_table = self.ft.word_to_vector_list(incorrect_word, numeric=True)

        spaced_words = levenshtein_distance(correct_feature_table, incorrect_feature_table,delete_insert_cost=0.92)

        for phone_index in range(len(spaced_words["original_string_parts"])):
            original_sound = tuple(spaced_words["original_string_parts"][phone_index])
            new_sound = tuple(spaced_words["new_string_parts"][phone_index])

            if original_sound == new_sound:
                continue

            consonant_index = 2

            # 確定應該更新的字典
            if (original_sound and original_sound[consonant_index] == 1):
                target_dict = consonant_errors
            elif original_sound:
                target_dict = vowel_errors
            elif new_sound[consonant_index] == 1:
                target_dict = consonant_errors
            else:
                target_dict = vowel_errors

            # 確定鍵和值
            if len(original_sound):
                key = original_sound
            else:
                key = ""
            if len(new_sound):
                value = new_sound
            else:
                value = ""

            # 如果鍵已經存在於字典中，更新其值
            if key in target_dict:
                if value in target_dict[key]:
                    target_dict[key][value] += 1
                else:
                    target_dict[key][value] = 1
            else:
                target_dict[key] = {value: 1}

        return consonant_errors, vowel_errors

    def calculate_combined_errors(self, word_pairs: list[tuple[str, str]]) -> tuple[dict[str:dict]]:
        combined_consonant_errors = {}
        combined_vowel_errors = {}

        for correct_word, incorrect_word in word_pairs:
            consonant_errors, vowel_errors = self.calculate_consonat_vowel_errors(correct_word, incorrect_word)

            # 合併子音錯誤
            for key, value_dict in consonant_errors.items():
                if key not in combined_consonant_errors:
                    combined_consonant_errors[key] = value_dict
                else:
                    for value_key, count in value_dict.items():
                        if value_key in combined_consonant_errors[key]:
                            combined_consonant_errors[key][value_key] += count
                        else:
                            combined_consonant_errors[key][value_key] = count

            # 合併母音錯誤
            for key, value_dict in vowel_errors.items():
                if key not in combined_vowel_errors:
                    combined_vowel_errors[key] = value_dict
                else:
                    for value_key, count in value_dict.items():
                        if value_key in combined_vowel_errors[key]:
                            combined_vowel_errors[key][value_key] += count
                        else:
                            combined_vowel_errors[key][value_key] = count

        return combined_consonant_errors, combined_vowel_errors


if __name__ == '__main__':

    # 示例使用
    tester = Tester(SingleWordDataHandler(directory="../Data/phoneticData"))



    tester.calculate_consonat_vowel_errors("aa","ced")

    exit()

    print(tester.list_languages_with_full_names())

    # 設置語言並生成問題
    selected_languages = ['nan', 'abk']
    questions = tester.generate_words_for_question(number=5, selected_languages=selected_languages)
    print("題目：", questions)

    # 獲取多選題
    difficulty = 'medium'
    difficulty_map = {'easy': 1, 'medium': 2, 'hard': 3}
    options = tester.get_multiple_choice_question(questions[0], number_of_answers=6)

    # 檢查答案
    answer = options[2]
    score = tester.check_answer(answer, questions[0])

    print(f"選項: {options}")
    print(f"選擇的答案: {answer}")
    print(f"得分: {score}")

    # 計算平均分和標準差
    answers = [score]
    avg_score = tester.get_average_score(answers)
    std_dev = tester.get_standard_deviation(answers)

    print(f"平均分: {avg_score}")
    print(f"標準差: {std_dev}")

    # 設置測試語言
    selected_languages = ['nan', 'abk']  # 假設我們的數據集中有這些語言

    # 測試 generate_questions 方法
    number_of_questions = 5
    question_types = ['fill_in_the_blank', 'multiple_choice', 'organize_sounds']

    generated_questions = tester.generate_questions(selected_languages, number=number_of_questions,
                                                    question_types=question_types)

    # 驗證輸出
    print(f"生成的 {number_of_questions} 個問題如下：")
    for i, question in enumerate(generated_questions):
        print(f"問題 {i + 1}:")
        print(f"  語言 ID: {question['language_id']}")
        print(f"  語言名稱: {question['language_name']}")
        print(f"  音頻位置: {question['audio_path']}")
        print(f"  問題類型: {question['question_type']}")
        print(f"  需要填寫的詞: {question['word_to_find']}")
        print(f"  正確答案: {question['correct_answer']}")
        print(f"  選擇題選項: {question['answer_choices']}")
        print("-" * 30)

    # 檢查 generate_equally_phonetically_spaced_words with "ʔ˨"
    print("Testing generate_equally_phonetically_spaced_words with 'ʔ˨'")
    test_word = "ʔ˨"
    spaced_words = tester.generate_equally_phonetically_spaced_words(test_word, num_words=6, hamming_distance=2)
    print(f"Generated phonetically spaced words for '{test_word}':")
    for word in spaced_words:
        print(word)

