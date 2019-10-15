 # NetHope technical support SOW
Goal: Create script to do partial transcriptions of audio based on timestamps created by KoBoToolbox

## Requirements
- Python 3.6
- pip
- virtualenv

## Setup
````
pip install virtualenv
````
- Create a virtual environment
The following assumes that the global python is 3.6
````
virtualenv env
````
- Activate the virtual environment
    - In windows
        ````
        ./env/Scripts/activate
        ````
    - In linux/MAC OS
        ````
        source /env/bin/activate
        ````
- Download dependencies
  ````
  pip install -r requirements.txt
  ````
- Add GOOGLE_APPLICATION_CREDENTIALS environment variable file. This variable links to the json file
 containing the private key for google cloud

## Current Data Collection Process
1. Interviewer calls remote interviewee
2. AudioRecorder app begins recording
3. Interview opens up the KoBoCollect app on her phone
4. Interviewer asks questions, navigates from one question to the next. Each time she switches to a new question, kobo records new timestamps.
5. After finishing the interview, she saves the record which is submitted to the kobo server. This includes a JSON record of the data collected during the interview (that the interviewer entered herself), as well as an audit.csv file that contains all the timestamps
6. After she hangs up the phone, the recording is ended and uploaded to Dropbox

## Steps
- Set up Postgres
- Get details from raw audio recording
- For each audio file, transcribe and store result in database
- For each transcription, translate into English and store in database
- Export database to CSV or XLS
- Get specific epoch timestamps for each question’s start and end (created by kobo)
- For each required question, extract audio
- Repeat steps 2 and 3