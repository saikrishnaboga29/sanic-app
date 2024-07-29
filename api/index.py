import logging
from sanic import Sanic
from sanic.response import json

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Sanic("FileUploadApp")

# Route for GET requests at /hello
@app.route('/hello', methods=['GET'], name='hello')
async def hello(request):
    logger.debug("Entered the hello route")
    return json({'message': 'Hello, world!'})

# New route for testing POST requests
@app.route('/test', methods=['POST'], name='test_endpoint')
async def test(request):
    logger.debug("Entered the test endpoint")
    data = request.json
    logger.debug(f"Received data: {data}")
    return json({"message": "Test successful", "received_data": data})

# If you want to add the upload route back later, you can uncomment the following code
# # Route for POST requests to upload and transcribe audio files
# @app.route('/upload', methods=['POST'], name='upload_file')
# async def upload(request):
#     logger.debug("Entered the upload route")
#     logger.debug(f"Request files: {request.files}")

#     if not request.files:
#         logger.debug("No file uploaded")
#         return json({"error": "No file uploaded"}, status=400)
    
#     for file_key, file in request.files.items():
#         uploaded_file = file[0]
#         file_name = uploaded_file.name
#         file_body = uploaded_file.body

#         logger.debug(f"File key: {file_key}")
#         logger.debug(f"File name: {file_name}")
#         logger.debug(f"File body length: {len(file_body)}")

#         # Process the audio file in memory
#         audio_segment = AudioSegment.from_file(io.BytesIO(file_body), format="mp3")
#         audio_wav = io.BytesIO()
#         audio_segment.export(audio_wav, format='wav')
#         audio_wav.seek(0)

#         # Transcribe the audio file
#         transcription = await transcribe_audio(audio_wav)
#         if transcription is None:
#             logger.debug(f"Transcription failed for {file_name}")
#             return json({"message": f"File {file_name} uploaded successfully", "transcription": "Transcription failed"})
        
#         logger.debug(f"Transcription success for {file_name}")
#         return json({"message": f"File {file_name} uploaded successfully", "transcription": transcription})
    
#     logger.debug("No files processed")
#     return json({"error": "No files processed"}, status=500)

# async def transcribe_audio(file_like):
#     """Transcribe the audio file using local speech recognition"""
#     try:
#         logger.debug(f"Transcribing file")
#         recognizer = sr.Recognizer()

#         with sr.AudioFile(file_like) as source:
#             audio_data = recognizer.record(source)
#             transcription = recognizer.recognize_google(audio_data)
#             logger.debug(f"Transcription result: {transcription}")

#         return transcription
#     except sr.UnknownValueError:
#         logger.error("Google Speech Recognition could not understand the audio")
#         return None
#     except sr.RequestError as e:
#         logger.error(f"Could not request results from Google Speech Recognition service; {e}")
#         return None
#     except Exception as e:
#         logger.error(f"Error transcribing audio: {e}")
#         return None

