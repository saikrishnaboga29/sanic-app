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

# Remove the file upload code to avoid errors related to file system

if __name__ == '__main__':
    logger.debug("Starting Sanic server")
    app.run(host='0.0.0.0', port=8000)
