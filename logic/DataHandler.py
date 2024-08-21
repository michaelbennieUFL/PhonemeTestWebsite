import os
import random
import threading
from playsound import playsound

class SingleWordDataHandler:
    def __init__(self, directory='Data/phoneticData/'):
        """初始化，設置數據集目錄"""
        self.directory = directory

    def list_languages(self):
        """列出所有語言目錄"""
        return [name for name in os.listdir(self.directory) if os.path.isdir(os.path.join(self.directory, name))]

    def list_wav_files(self, language, fullPath=False):
        """列出指定語言的所有wav文件"""
        if fullPath:
            language_dir = os.path.join(self.directory, language, 'audio')
            return [os.path.join(language_dir, name) for name in os.listdir(language_dir) if name.endswith('.wav')]
        language_dir = os.path.join(self.directory, language, 'audio')
        return [name for name in os.listdir(language_dir) if name.endswith('.wav')]

    def get_random_audio(self, language, fullPath=True):
        wav_files = self.list_wav_files(language, fullPath)
        if wav_files:
            return random.choice(wav_files)
        return None

    def play_audio(self, audio_path):
        if audio_path:
            print(f"Playing audio: {audio_path}")
            playsound(audio_path)

    def play_random_audio(self, language):
        audio_path = self.get_random_audio(language, fullPath=True)
        if audio_path:
            threading.Thread(target=self.play_audio, args=(audio_path,)).start()
        return [audio_path,
                self.get_transcription(language, os.path.basename(audio_path))[1],
                self.get_transcription(language, os.path.basename(audio_path), transcription_type='loose')[1]]

    def play_specific_audio(self, language, file_name):
        if file_name in self.list_wav_files(language, fullPath=False):
            audio_path = os.path.join(self.directory, language, 'audio', file_name)
            threading.Thread(target=self.play_audio, args=(audio_path,)).start()
            return [audio_path,
                    self.get_transcription(language, file_name)[1],
                    self.get_transcription(language, file_name, transcription_type='loose')[1]]
        return None

    def get_transcription(self, language, wav_file, transcription_type='strict'):
        """給定語言和wav文件，輸出wav文件位置和對應的轉錄文本"""
        language_dir = os.path.join(self.directory, language)
        wav_file_path = os.path.join(language_dir, 'audio', wav_file)

        if transcription_type == 'strict':
            transcription_file = os.path.join(language_dir, 'raw')
        elif transcription_type == 'loose':
            transcription_file = os.path.join(language_dir, 'text.txt')
        else:
            raise ValueError("Invalid transcription type. Use 'strict' or 'loose'.")

        with open(transcription_file, 'r', encoding='utf-8') as file:
            transcriptions = file.readlines()

        transcription_dict = {}
        for line in transcriptions:
            parts = line.strip().split(maxsplit=1)
            if len(parts) == 2:
                transcription_dict[parts[0]] = parts[1]

        transcription_key = os.path.splitext(wav_file)[0]
        transcription = transcription_dict.get(transcription_key, "Transcription not found")

        return wav_file_path, transcription

if __name__ == '__main__':
    # 示例使用
    handler = SingleWordDataHandler()

    # 1. 列出所有語言
    languages = handler.list_languages()
    print("語言目錄：", languages)

    # 2. 列出某個語言的所有wav文件
    language = 'abk'
    wav_files = handler.list_wav_files(language)
    print(f"{language} 語言的wav文件：", wav_files)

    # 3. 給定語言和wav文件，輸出wav文件位置和對應的轉錄文本
    wav_file = 'abk-002-000.wav'
    wav_file_path, transcription = handler.get_transcription(language, wav_file, transcription_type='strict')
    print(f"wav文件位置：{wav_file_path}")
    print(f"對應的轉錄文本：{transcription}")
    print("測試播放聲音：", handler.play_random_audio(language), handler.play_specific_audio(language, wav_file))
