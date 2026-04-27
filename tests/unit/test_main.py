import pytest

from app.main import (
    DeveloperTask,
    TaskStatus,
    fetch_all_tasks,
    generate_productivity_report,
)


@pytest.mark.asyncio
async def test_fetch_all_tasks_returns_all_tasks():
    tasks = await fetch_all_tasks()

    assert isinstance(tasks, list)
    assert len(tasks) == 3
    assert tasks[0].task_id == 1
    assert tasks[0].title == "Refactor legacy service"
    assert tasks[0].status == TaskStatus.COMPLETE
    assert tasks[1].status == TaskStatus.IN_PROGRESS
    assert tasks[2].status == TaskStatus.PENDING


@pytest.mark.asyncio
async def test_generate_productivity_report_computes_metrics():
    report = await generate_productivity_report()

    assert report.total_tasks == 3
    assert report.completed_tasks == 1
    assert report.total_hours_spent == 23.5
    assert report.completion_rate == 0.33


def test_developer_task_default_values():
    task = DeveloperTask(task_id=5, title="Model test")

    assert task.status == TaskStatus.PENDING
    assert task.hours_spent == 0.0
