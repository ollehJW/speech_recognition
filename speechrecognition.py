import speech_recognition as sr
from glob import glob 
import os
import pandas as pd

AVAILABLE_LANGUAGE = ['Korean', 'English']

language = 'English'
data_dir = './data/english'
result_dir = './experiment/speechrecognition/english'

if language in AVAILABLE_LANGUAGE:
    print('{} is selected as language.'.format(language))
else:
    raise NotImplementedError('{} has not been implemented, use language in {}'.format(language, AVAILABLE_LANGUAGE))

data_list = glob(os.path.join(data_dir, '*.wav')) + glob(os.path.join(data_dir, '*.flac'))
if len(data_list) == 0:
    raise NotImplementedError('There is not [wav, flac] file.')
else:
    print('There are {} sound files.'.format(len(data_list)))

file_name_list = []
recognition_list = []

for data in data_list:
    file_name_list.append(os.path.basename(data))
    # audio file을 audio source로 사용합니다
    r = sr.Recognizer()
    with sr.AudioFile(data) as source:
        audio = r.record(source)  # 전체 audio file 읽기

    # 구글 웹 음성 API로 인식하기 (하루에 제한 50회)
    if language == 'Korean':
        recognition_list.append(r.recognize_google(audio, language='ko'))
    else:
        recognition_list.append(r.recognize_google(audio, language='en-US'))

result = pd.DataFrame({'File': file_name_list, 'Recognition': recognition_list})
result.to_csv(os.path.join(result_dir, 'recognition.csv'), index = False)

