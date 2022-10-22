# Install and Import Dependencies

!pip install ibm_watson

from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Setup STT Service , speec text service

apikey = '' #from ibm cloud according to the plan(500 min of speech per month ) and the city
url = ''

authenticator = IAMAuthenticator(apikey)
stt = SpeechToTextV1(authenticator = authenticator)
stt.set_service_url(url)

# Compress and Split Audio
import subprocess #It lets you start new applications right from the Python program you are currently writing. So, 
#if you want to run external programs from a git repository or codes from C or C++ programs, you can use subprocess in Python
import os
command = 'ffmpeg -i audio.wav -vn -ar 44100 -ac 2 -b:a 192k audio.mp3'
subprocess.call(command, shell=True)# it causes subprocess to spawn an intermediate shell process, and tell it to run the command
command = 'ffmpeg -i audio.mp3 -f segment -segment_time 360 -c copy %03d.mp3'
subprocess.call(command, shell=True)

files = []
for filename in os.listdir('.'):
    if filename.endswith(".mp3") and filename !='audio.mp3':
        files.append(filename)
files.sort()

files

# Perform Conversion
results = []
for filename in files:
    with open(filename, 'rb') as f:
        res = stt.recognize(audio=f, content_type='audio/mp3', model='en-AU_NarrowbandModel', continuous=True, \
                           inactivity_timeout=360).get_result()
        results.append(res)

text = []
for file in results:
    for result in file['results']:
        text.append(result['alternatives'][0]['transcript'].rstrip() + '.\n')

text

with open('output.txt', 'w') as out:
    out.writelines(text)
