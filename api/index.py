import os
import io
import logging
from sanic import Sanic
from sanic.response import json
from pydub import AudioSegment
import speech_recognition as sr

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Sanic("FileUploadApp")

# Ensure the uploads directory exists
UPLOAD_DIRECTORY = 'uploads'
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)
    logger.debug(f"Created directory: {UPLOAD_DIRECTORY}")

# Route for GET requests at /hello
@app.route('/hello', methods=['GET'], name='hello')
async def hello(request):
    logger.debug("Entered the hello route")
    return json({'message': 'Hello, Krishna!'})

# Route for POST requests to upload and transcribe audio files
@app.route('/upload', methods=['POST'], name='upload_file')
async def upload(request):
    logger.debug("Entered the upload route")
    logger.debug(f"Request files: {request.files}")

    if not request.files:
        logger.debug("No file uploaded")
        return json({"error": "No file uploaded"}, status=400)
    
    for file_key, file in request.files.items():
        uploaded_file = file[0]
        file_name = uploaded_file.name
        file_body = uploaded_file.body

        logger.debug(f"File key: {file_key}")
        logger.debug(f"File name: {file_name}")
        logger.debug(f"File body length: {len(file_body)}")

        file_path = os.path.join(UPLOAD_DIRECTORY, file_name)
        with open(file_path, 'wb') as f:
            logger.debug(f"Saving file to {file_path}")
            f.write(file_body)
        
        logger.debug(f"File {file_name} uploaded successfully")

        # Transcribe the audio file
        transcription = await transcribe_audio(file_path)
        if transcription is None:
            logger.debug(f"Transcription failed for {file_name}")
            return json({"message": f"File {file_name} uploaded successfully", "transcription": "Transcription failed"})
        
        logger.debug(f"Transcription success for {file_name}")
        return json({"message": f"File {file_name} uploaded successfully", "transcription": transcription})
    
    logger.debug("No files processed")
    return json({"error": "No files processed"}, status=500)

async def transcribe_audio(file_path):
    """Transcribe the audio file using local speech recognition"""
    try:
        logger.debug(f"Transcribing file: {file_path}")
        recognizer = sr.Recognizer()

        # Convert audio file to WAV format if necessary
        if not file_path.endswith('.wav'):
            logger.debug(f"File is not in WAV format: {file_path}")
            try:
                audio = AudioSegment.from_file(file_path)
                file_path_wav = file_path.rsplit('.', 1)[0] + '.wav'
                audio.export(file_path_wav, format='wav')
                file_path = file_path_wav
                logger.debug(f"Converted file to WAV format: {file_path}")
            except Exception as e:
                logger.error(f"Error converting file to WAV format: {e}")
                return None

        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)
            transcription = recognizer.recognize_google(audio_data)
            logger.debug(f"Transcription result: {transcription}")

        return transcription
    except sr.UnknownValueError:
        logger.error("Google Speech Recognition could not understand the audio")
        return None
    except sr.RequestError as e:
        logger.error(f"Could not request results from Google Speech Recognition service; {e}")
        return None
    except Exception as e:
        logger.error(f"Error transcribing audio: {e}")
        return None

# New route for testing deployment
@app.route('/test', methods=['POST'], name='test_endpoint')
async def test(request):
    logger.debug("Entered the test endpoint")
    data = request.json
    logger.debug(f"Received data: {data}")
    return json({"message": "Test successful", "received_data": data})

if __name__ == '__main__':
    logger.debug("Starting Sanic server")
    app.run(host='0.0.0.0', port=8000)
