import pytest
from fastapi.testclient import TestClient
from .main import app, fetch_all_tasks, generate_productivity_report, MOCK_TASKS, TaskStatus, DeveloperTask

client = TestClient(app)

@pytest.mark.asyncio
async def test_fetch_all_tasks():
    """Test fetching all tasks asynchronously."""
    tasks = await fetch_all_tasks()
    assert len(tasks) == 3
    assert tasks[0].task_id == 1
    assert tasks[0].title == "Refactor legacy service"
    assert tasks[0].status == TaskStatus.COMPLETE
    assert tasks[1].status == TaskStatus.IN_PROGRESS
    assert tasks[2].status == TaskStatus.PENDING

@pytest.mark.asyncio
async def test_generate_productivity_report():
    """Test generating productivity report."""
    report = await generate_productivity_report()
    assert report.total_tasks == 3
    assert report.completed_tasks == 1  # Based on current logic counting PENDING
    assert report.total_hours_spent == 23.5
    assert report.completion_rate == 0.33

def test_get_status():
    """Test the status endpoint."""
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_all_tasks():
    """Test getting all tasks via API."""
    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 3
    assert tasks[0]["task_id"] == 1
    assert tasks[0]["status"] == "complete"

def test_get_productivity_report():
    """Test getting productivity report via API."""
    response = client.get("/report")
    assert response.status_code == 200
    report = response.json()
    assert report["total_tasks"] == 3
    assert report["completed_tasks"] == 1
    assert report["total_hours_spent"] == 23.5
    assert report["completion_rate"] == 0.33

def test_log_task():
    """Test logging a new task via API."""
    new_task_data = {
        "title": "Test task",
        "status": "in_progress",
        "hours_spent": 2.5
    }
    response = client.post("/log_task", json=new_task_data)
    assert response.status_code == 200
    assert response.json() == "Task ID 4 logged successfully."
    
    # Verify the task was added
    response = client.get("/tasks")
    tasks = response.json()
    assert len(tasks) == 4
    assert tasks[3]["task_id"] == 4
    assert tasks[3]["title"] == "Test task"
    assert tasks[3]["status"] == "in_progress"
    assert tasks[3]["hours_spent"] == 2.5

def test_get_task_status_existing():
    """Test getting status of an existing task."""
    response = client.get("/task/1/status")
    assert response.status_code == 200
    assert response.json() == {"task_id": "1", "status": "complete"}

def test_get_task_status_nonexistent():
    """Test getting status of a nonexistent task."""
    response = client.get("/task/999/status")
    assert response.status_code == 200
    assert response.json() == {"error": "Task not found"}

def test_developer_task_model():
    """Test DeveloperTask model validation."""
    task = DeveloperTask(task_id=5, title="Model test", status=TaskStatus.COMPLETE, hours_spent=10.0)
    assert task.task_id == 5
    assert task.status == TaskStatus.COMPLETE

    # Test default values
    task_default = DeveloperTask(task_id=6, title="Default test")
    assert task_default.status == TaskStatus.PENDING
    assert task_default.hours_spent == 0.0