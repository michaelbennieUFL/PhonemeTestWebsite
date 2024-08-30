import csv

def filter_csv_by_phonemes(phonemes_file_path, csv_file_path, output_file_path):
    # 讀取音素文件中的音素
    with open(phonemes_file_path, 'r', encoding='utf-8') as phonemes_file:
        phonemes = set(line.strip() for line in phonemes_file if line.strip())

    # 打開要篩選的CSV文件
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        rows = list(reader)

    # 保留第一行（標題）
    filtered_rows = [rows[0]]

    # 遍歷CSV文件中的每一行，保留符合條件的行
    for row in rows[1:]:
        ipa = row[0]
        if ipa in phonemes or any(ipa == phoneme + symbol for phoneme in phonemes for symbol in ('˞', 'ː', '̥', '̩', '̃', '̰', '̈', '̆', '̝', '̞', '̤', '̠', '̟', '̠')):
            filtered_rows.append(row)

    # 將結果寫入新的CSV文件
    with open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
        writer = csv.writer(output_file)
        writer.writerows(filtered_rows)

# 使用範例
csv_file_path= '../.venv/lib/python3.10/site-packages/panphon/data/ipa_all.csv'
phonemes_file_path = '../allUniquePhones.txt'
output_file_path = '../.venv/lib/python3.10/site-packages/panphon/data/ipa_all.csv'

filter_csv_by_phonemes(phonemes_file_path, csv_file_path, output_file_path)
