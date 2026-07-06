from pawpal_system import Pet, Task


def test_task_completion_marks_task_complete():
    task = Task(description="Morning walk", scheduled_time="08:00")

    task.mark_complete()

    assert task.is_complete() is True
    assert task.is_pending() is False


def test_adding_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog")
    task = Task(description="Feed breakfast", scheduled_time="07:30")

    pet.add_task(task)

    assert len(pet.get_tasks()) == 1
    assert task in pet.get_tasks()
