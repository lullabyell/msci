## Requirements
Python 3.7+
fastapi framework
uvicorn ASGI server
httpx for making asynchronous HTTP requests

## Setup
1. Create and Activate a Virtual Environment
- On macOS/Linux
python3 -m venv myenv
source myenv/bin/activate
- On Windows
python -m venv myenv
myenv\Scripts\activate

2. Install Dependencies
pip install fastapi uvicorn httpx

## Running the Application
uvicorn main:app --host 127.0.0.1 --port 8000

## Usage
API Endpoint
GET /versions

- Query Parameters:
name (required): The name of the package to check for vulnerabilities.

- Example Request:
curl -X GET "http://127.0.0.1:8000/versions?name=xz-utils"

- Example Response:
{
    "name": "xz-utils",
    "versions": [
        "5.2.2-1.2",
        "5.2.4-1",
        "5.2.5-2"
    ],
    "timestamp": "2024-06-17 14:44:04"
}