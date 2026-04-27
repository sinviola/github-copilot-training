import pytest
from copy import deepcopy

from app.main import MOCK_TASKS


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_status_endpoint(async_client):
    response = await async_client.get("/status")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_all_tasks_endpoint(async_client):
    response = await async_client.get("/tasks")

    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    assert len(tasks) == 3
    assert tasks[0]["task_id"] == 1
    assert tasks[0]["status"] == "complete"


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_productivity_report_endpoint(async_client):
    response = await async_client.get("/report")

    assert response.status_code == 200
    report = response.json()
    assert report["total_tasks"] == 3
    assert report["completed_tasks"] == 1
    assert report["total_hours_spent"] == 23.5
    assert report["completion_rate"] == 0.33


@pytest.mark.asyncio
@pytest.mark.integration
async def test_log_task_endpoint_adds_new_task(async_client):
    original_tasks = deepcopy(MOCK_TASKS)

    try:
        new_task_payload = {
            "task_id": 0,
            "title": "Test task",
            "status": "in_progress",
            "hours_spent": 2.5,
        }

        response = await async_client.post("/log_task", json=new_task_payload)
        assert response.status_code == 200
        assert response.json() == "Task ID 4 logged successfully."

        response = await async_client.get("/tasks")
        tasks = response.json()
        assert len(tasks) == 4
        assert tasks[-1]["task_id"] == 4
        assert tasks[-1]["title"] == "Test task"
        assert tasks[-1]["status"] == "in_progress"
        assert tasks[-1]["hours_spent"] == 2.5
    finally:
        MOCK_TASKS.clear()
        MOCK_TASKS.update(original_tasks)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_task_status_endpoint_returns_existing_status(async_client):
    response = await async_client.get("/task/1/status")

    assert response.status_code == 200
    assert response.json() == {"task_id": "1", "status": "complete"}


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_task_status_endpoint_returns_not_found(async_client):
    response = await async_client.get("/task/999/status")

    assert response.status_code == 200
    assert response.json() == {"error": "Task not found"}
