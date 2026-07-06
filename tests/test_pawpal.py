from pawpal_system import Owner, Pet, Scheduler, Task


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


def test_scheduler_returns_tasks_in_chronological_order():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    high_priority_late = Task(description="Evening play", scheduled_time="18:00", priority="high")
    high_priority_early = Task(description="Morning walk", scheduled_time="08:00", priority="high")
    medium_priority_mid = Task(description="Lunch feeding", scheduled_time="12:00", priority="medium")

    scheduler = Scheduler(owner=owner)
    pet.add_task(high_priority_late)
    pet.add_task(high_priority_early)
    pet.add_task(medium_priority_mid)

    ordered = scheduler.organize_tasks(owner)

    assert ordered[0].description == "Morning walk"
    assert ordered[1].description == "Lunch feeding"
    assert ordered[2].description == "Evening play"


def test_scheduler_detects_duplicate_scheduled_times():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    first_task = Task(description="Walk", scheduled_time="08:00", priority="high")
    second_task = Task(description="Feed", scheduled_time="08:00", priority="medium")

    pet.add_task(first_task)
    pet.add_task(second_task)

    scheduler = Scheduler(owner=owner)
    conflicts = scheduler.detect_conflicts(pet.get_tasks())

    assert len(conflicts) == 1
    assert conflicts[0][0].description == "Walk"
    assert conflicts[0][1].description == "Feed"


def test_scheduler_filters_tasks_by_pet_and_completion_status():
    owner = Owner(name="Jordan")
    mochi = Pet(name="Mochi", species="dog")
    luna = Pet(name="Luna", species="cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)

    pending_mochi_task = Task(description="Morning walk", scheduled_time="08:00")
    completed_luna_task = Task(description="Vet visit", scheduled_time="14:00")
    completed_mochi_task = Task(description="Brushing", scheduled_time="16:00")

    completed_luna_task.mark_complete()
    completed_mochi_task.mark_complete()

    mochi.add_task(pending_mochi_task)
    luna.add_task(completed_luna_task)
    mochi.add_task(completed_mochi_task)

    scheduler = Scheduler(owner=owner)
    filtered_tasks = scheduler.filter_tasks(owner.get_all_tasks(), pet_name="Mochi", completed=False, owner=owner)

    assert filtered_tasks == [pending_mochi_task]


def test_marking_daily_task_complete_creates_next_occurrence():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    task = Task(description="Morning walk", scheduled_time="08:00", frequency="daily", priority="high")
    pet.add_task(task)

    scheduler = Scheduler(owner=owner)
    next_task = scheduler.mark_task_complete(task, pet_name="Mochi", owner=owner)

    assert task.is_complete() is True
    assert next_task is not None
    assert next_task.is_complete() is False
    assert next_task.frequency == "daily"
    assert next_task in pet.get_tasks()
    assert len(pet.get_tasks()) == 2


def test_scheduler_returns_warning_for_conflicting_tasks():
    owner = Owner(name="Jordan")
    mochi = Pet(name="Mochi", species="dog")
    luna = Pet(name="Luna", species="cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)

    first_task = Task(description="Morning walk", scheduled_time="08:00", priority="high")
    second_task = Task(description="Vet visit", scheduled_time="08:00", priority="medium")

    mochi.add_task(first_task)
    luna.add_task(second_task)

    scheduler = Scheduler(owner=owner)
    warning = scheduler.get_conflict_warning(owner=owner)

    assert warning is not None
    assert "Warning" in warning
    assert "08:00" in warning


def test_scheduler_handles_case_insensitive_priority_when_sorting():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    low_priority_task = Task(description="Grooming", scheduled_time="12:00", priority="LOW")
    high_priority_task = Task(description="Walk", scheduled_time="09:00", priority="High")

    pet.add_task(low_priority_task)
    pet.add_task(high_priority_task)

    scheduler = Scheduler(owner=owner)
    ordered_tasks = scheduler.organize_tasks(owner)

    assert [task.description for task in ordered_tasks] == ["Walk", "Grooming"]


def test_scheduler_creates_next_occurrence_for_monthly_task():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    task = Task(description="Vet check", scheduled_time="15:00", frequency="monthly", priority="medium")
    pet.add_task(task)

    scheduler = Scheduler(owner=owner)
    next_task = scheduler.mark_task_complete(task, pet_name="Mochi", owner=owner)

    assert next_task is not None
    assert next_task.frequency == "monthly"
    assert next_task.is_complete() is False
    assert next_task in pet.get_tasks()


def test_scheduler_does_not_create_next_occurrence_for_non_recurring_task():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    task = Task(description="Brush teeth", scheduled_time="19:00", frequency="once", priority="low")
    pet.add_task(task)

    scheduler = Scheduler(owner=owner)
    next_task = scheduler.mark_task_complete(task, pet_name="Mochi", owner=owner)

    assert next_task is None
    assert len(pet.get_tasks()) == 1
