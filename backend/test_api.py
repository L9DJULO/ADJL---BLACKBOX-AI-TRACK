import pytest
import asyncio
from fastapi.testclient import TestClient
from app import app
import os
import json
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock

# Test client
client = TestClient(app)

# Test data
SAMPLE_CODE = """
def calculate_sum(a, b):
    return a + b

def main():
    result = calculate_sum(5, 3)
    print(f"Sum is: {result}")
"""

SAMPLE_COMMAND = "add error handling to this function"

class TestBasicEndpoints:
    """Test basic API endpoints"""
    
    def test_root_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "running"
        assert data["service"] == "AI Voice Code Assistant"
    
    def test_models_status(self):
        """Test models status endpoint"""
        response = client.get("/api/models/status")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Check if all required services are present
        service_names = [status["service_name"] for status in data]
        required_services = ["blackbox", "groq", "llama", "coral", "fetch", "git"]
        for service in required_services:
            assert service in service_names

class TestVoiceCommand:
    """Test voice command processing"""
    
    @patch('services.ai_orchestrator.AIOrchestrator.process_voice_command')
    @patch('services.git_service.GitService.create_branch_and_commit')
    def test_voice_command_success(self, mock_git, mock_ai):
        """Test successful voice command processing"""
        # Mock AI response
        mock_ai.return_value = asyncio.coroutine(lambda: {
            "intent_analysis": {
                "success": True,
                "content": {"action": "refactor"}
            },
            "code_generation": {
                "success": True,
                "code": "# Refactored code here"
            },
            "external_data": {},
            "coral_analysis": {"success": True}
        })()
        
        # Mock Git response
        mock_git.return_value = {
            "success": True,
            "branch_name": "ai-refactor-123456",
            "commit_hash": "abc123"
        }
        
        # Make request
        response = client.post(
            "/api/voice-command",
            data={
                "command": SAMPLE_COMMAND,
                "code_context": SAMPLE_CODE,
                "file_path": "test.py",
                "project_path": "/tmp/test-repo"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["transcription"] == SAMPLE_COMMAND
        assert data["command_type"] == "refactor"
        assert "ai_analysis" in data
        assert data["branch_name"] is not None
        assert data["git_status"]["success"] is True
    
    def test_voice_command_missing_params(self):
        """Test voice command with missing parameters"""
        response = client.post(
            "/api/voice-command",
            data={
                "command": SAMPLE_COMMAND
                # Missing other required fields
            }
        )
        assert response.status_code == 422  # Unprocessable Entity

class TestCodeAnalysis:
    """Test code analysis endpoints"""
    
    @patch('services.blackbox_service.BlackboxService.analyze_code')
    def test_analyze_code(self, mock_analyze):
        """Test code analysis"""
        mock_analyze.return_value = {
            "bugs": [],
            "security_issues": [],
            "improvements": ["Add docstrings", "Handle edge cases"],
            "success": True
        }
        
        response = client.post(
            "/api/analyze-code",
            data={
                "code": SAMPLE_CODE,
                "language": "python"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "analysis" in data
        assert data["service"] == "blackbox_ai"
    
    @patch('services.blackbox_service.BlackboxService.generate_tests')
    def test_generate_tests(self, mock_tests):
        """Test test generation"""
        mock_tests.return_value = {
            "tests": "def test_calculate_sum():\n    assert calculate_sum(2, 3) == 5",
            "framework": "pytest",
            "success": True
        }
        
        response = client.post(
            "/api/generate-tests",
            data={
                "code": SAMPLE_CODE,
                "language": "python"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "tests" in data
    
    @patch('services.blackbox_service.BlackboxService.refactor_code')
    def test_refactor_code(self, mock_refactor):
        """Test code refactoring"""
        mock_refactor.return_value = {
            "refactored_code": "# Improved code here",
            "changes": ["Added type hints", "Improved naming"],
            "success": True
        }
        
        response = client.post(
            "/api/refactor-code",
            data={
                "code": SAMPLE_CODE,
                "language": "python",
                "instructions": "Add type hints"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "refactored_code" in data

class TestGitIntegration:
    """Test Git integration"""
    
    def setUp(self):
        """Create a temporary Git repository for testing"""
        self.temp_dir = tempfile.mkdtemp()
        self.repo_path = os.path.join(self.temp_dir, "test-repo")
        os.makedirs(self.repo_path)
        
        # Initialize Git repo
        import git
        self.repo = git.Repo.init(self.repo_path)
        
        # Create initial commit
        test_file = os.path.join(self.repo_path, "test.py")
        with open(test_file, "w") as f:
            f.write(SAMPLE_CODE)
        
        self.repo.index.add(["test.py"])
        self.repo.index.commit("Initial commit")
    
    def tearDown(self):
        """Clean up temporary directory"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Setup and teardown for each test"""
        self.setUp()
        yield
        self.tearDown()
    
    def test_analyze_git_changes(self):
        """Test Git change analysis"""
        response = client.post(
            "/api/git/analyze-changes",
            data={
                "repo_path": self.repo_path,
                "file_path": "test.py"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "metrics" in data
        assert data["metrics"]["total_commits"] == 1

class TestFetchRoutes:
    """Test Fetch.ai routes"""
    
    @patch('services.fetch_service.FetchService.deploy_agent')
    async def test_deploy_agent(self, mock_deploy):
        """Test agent deployment"""
        mock_deploy.return_value = {
            "agent_id": "agent-123",
            "status": "deployed",
            "endpoint": "https://agent.fetch.ai/123"
        }
        
        response = client.post(
            "/api/fetch/agent/deploy",
            params={
                "agent_code": "# Agent code",
                "agent_name": "TestAgent",
                "description": "Test agent"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["source"] == "fetch_ai"
    
    @patch('services.fetch_service.FetchService.search_network_resources')
    async def test_search_resources(self, mock_search):
        """Test network resource search"""
        mock_search.return_value = {
            "success": True,
            "resources": [
                {"name": "Python docs", "url": "https://docs.python.org"},
                {"name": "Tutorial", "url": "https://example.com/tutorial"}
            ],
            "total": 2
        }
        
        response = client.post(
            "/api/fetch/network/search",
            params={
                "query": "python error handling",
                "resource_type": "documentation",
                "max_results": 10
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "result" in data

class TestIntegration:
    """Integration tests"""
    
    @pytest.mark.integration
    @patch('services.blackbox_service.BlackboxService.generate_code')
    @patch('services.groq_service.GroqService.analyze_code_intent')
    @patch('services.fetch_service.FetchService.fetch_data_for_command')
    async def test_full_workflow(self, mock_fetch, mock_groq, mock_blackbox):
        """Test complete workflow from command to code generation"""
        
        # Mock Fetch data
        mock_fetch.return_value = {
            "documentation": {
                "success": True,
                "content": "Error handling best practices..."
            }
        }
        
        # Mock Groq intent analysis
        mock_groq.return_value = {
            "success": True,
            "content": json.dumps({
                "action": "modify",
                "target": "function",
                "description": "Add error handling",
                "confidence": 0.9
            })
        }
        
        # Mock Blackbox code generation
        mock_blackbox.return_value = {
            "success": True,
            "code": """
def calculate_sum(a, b):
    try:
        return a + b
    except TypeError:
        print("Error: Invalid input types")
        return None
"""
        }
        
        # Create temporary repo
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = os.path.join(temp_dir, "test-repo")
            os.makedirs(repo_path)
            
            import git
            repo = git.Repo.init(repo_path)
            
            test_file = os.path.join(repo_path, "test.py")
            with open(test_file, "w") as f:
                f.write(SAMPLE_CODE)
            
            repo.index.add(["test.py"])
            repo.index.commit("Initial commit")
            
            # Make request
            response = client.post(
                "/api/voice-command",
                data={
                    "command": "add error handling to calculate_sum function",
                    "code_context": SAMPLE_CODE,
                    "file_path": "test.py",
                    "project_path": repo_path
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["command_type"] == "generate"
            assert "error handling" in data["ai_analysis"]["code_generation"]["code"]

# Pytest configuration
if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])