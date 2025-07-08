# AI Voice Code Assistant - Testing Guide

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone the repository
git clone <your-repo-url>
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env and add your API keys
```

### 2. Run the Application

```bash
# Start the FastAPI server
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Or using Python directly
python app.py
```

The API will be available at: http://localhost:8000

## 📋 API Documentation

Once running, access the interactive API docs:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Testing the API

### Using cURL

1. **Health Check**
```bash
curl http://localhost:8000/
```

2. **Check Models Status**
```bash
curl http://localhost:8000/api/models/status
```

3. **Process Voice Command**
```bash
curl -X POST http://localhost:8000/api/voice-command \
  -F "command=add error handling to this function" \
  -F "code_context=def calculate(a, b): return a + b" \
  -F "file_path=test.py" \
  -F "project_path=/path/to/your/project"
```

4. **Analyze Code**
```bash
curl -X POST http://localhost:8000/api/analyze-code \
  -F "code=def hello(): print('world')" \
  -F "language=python"
```

### Using Python Requests

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000"

# Test voice command
response = requests.post(
    f"{BASE_URL}/api/voice-command",
    data={
        "command": "refactor this function to use type hints",
        "code_context": "def add(a, b):\n    return a + b",
        "file_path": "math_utils.py",
        "project_path": "/home/user/project"
    }
)

print(response.json())
```

### Using Postman

1. Import the following collection:

```json
{
  "info": {
    "name": "AI Voice Code Assistant",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/"
      }
    },
    {
      "name": "Process Voice Command",
      "request": {
        "method": "POST",
        "url": "{{base_url}}/api/voice-command",
        "body": {
          "mode": "formdata",
          "formdata": [
            {"key": "command", "value": "add documentation to this function"},
            {"key": "code_context", "value": "def process_data(data):\n    return data * 2"},
            {"key": "file_path", "value": "processor.py"},
            {"key": "project_path", "value": "/workspace/myproject"}
          ]
        }
      }
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8000"
    }
  ]
}
```

## 🔧 Running Unit Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=services --cov=routes

# Run specific test file
pytest test_api.py

# Run with verbose output
pytest -v -s

# Run only integration tests
pytest -m integration
```

## 🐛 Debugging Tips

### 1. Enable Debug Logging

In your `.env`:
```
APP_DEBUG=true
LOG_LEVEL=DEBUG
```

### 2. Check Service Status

```python
# Debug script to check services
import os
from dotenv import load_dotenv

load_dotenv()

print("BLACKBOX_API_KEY:", "Set" if os.getenv('BLACKBOX_API_KEY') else "Missing")
print("GROQ_API_KEY:", "Set" if os.getenv('GROQ_API_KEY') else "Missing")
print("CORAL_API_KEY:", "Set" if os.getenv('CORAL_API_KEY') else "Missing")
print("FETCH_API_KEY:", "Set" if os.getenv('FETCH_API_KEY') else "Missing")
```

### 3. Test Individual Services

```python
# Test BLACKBOX.AI service
from services.blackbox_service import BlackboxService

blackbox = BlackboxService()
result = blackbox.analyze_code("def test(): pass", "python")
print(result)
```

## 📊 Expected Responses

### Successful Voice Command Response
```json
{
  "success": true,
  "transcription": "add error handling to this function",
  "command_type": "refactor",
  "ai_analysis": {
    "intent_analysis": {...},
    "code_generation": {
      "success": true,
      "code": "def calculate(a, b):\n    try:\n        return a + b\n    except Exception as e:\n        print(f'Error: {e}')\n        return None"
    }
  },
  "branch_name": "ai-refactor-1234567890",
  "git_status": {
    "success": true,
    "branch_name": "ai-refactor-1234567890"
  },
  "services_used": ["blackbox", "groq", "llama", "coral", "fetch"],
  "execution_time": 2.5
}
```

### Error Response
```json
{
  "detail": "Error message describing what went wrong"
}
```

## 🚨 Common Issues

### 1. Missing API Keys
**Error**: `500 Internal Server Error`
**Solution**: Ensure all required API keys are set in `.env`

### 2. Git Repository Not Found
**Error**: `Repository not found`
**Solution**: Ensure the `project_path` points to a valid Git repository

### 3. Model Loading Timeout
**Error**: `Llama model loading timeout`
**Solution**: Set `LLAMA_PRELOAD=false` in `.env` for faster startup

### 4. WebSocket Connection Failed
**Error**: `Failed to connect to Coral`
**Solution**: Check Coral API key and endpoint configuration

## 🎯 Testing Checklist

- [ ] API starts without errors
- [ ] Health check endpoint responds
- [ ] All services show as "ready" in `/api/models/status`
- [ ] Voice command processing works
- [ ] Code analysis returns results
- [ ] Git branch creation succeeds
- [ ] Fetch.ai integration works (if configured)
- [ ] Coral Protocol connects (if configured)

## 💡 Advanced Testing

### Load Testing
```bash
# Using Apache Bench
ab -n 100 -c 10 http://localhost:8000/

# Using locust
locust -f locustfile.py --host=http://localhost:8000
```

### Integration Testing
```python
# Test with real Git repository
import tempfile
import git

with tempfile.TemporaryDirectory() as tmpdir:
    # Create test repo
    repo = git.Repo.init(tmpdir)
    
    # Create test file
    test_file = os.path.join(tmpdir, "test.py")
    with open(test_file, "w") as f:
        f.write("def hello():\n    print('world')")
    
    repo.index.add(["test.py"])
    repo.index.commit("Initial commit")
    
    # Test voice command
    response = requests.post(
        "http://localhost:8000/api/voice-command",
        data={
            "command": "add type hints",
            "code_context": open(test_file).read(),
            "file_path": "test.py",
            "project_path": tmpdir
        }
    )
    
    print(response.json())
```

## 📞 Support

If you encounter issues:
1. Check the logs in the console
2. Verify all API keys are correctly set
3. Ensure all dependencies are installed
4. Check the GitHub issues page

Happy testing! 🚀