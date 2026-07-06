from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner(name="Jordan")

    mochi = Pet(name="Mochi", species="dog", age="3")
    luna = Pet(name="Luna", species="cat", age="2")

    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler(owner=owner)

    tasks_to_add = [
        ("Mochi", Task(description="Morning walk", scheduled_time="08:00", frequency="daily", priority="high")),
        ("Luna", Task(description="Play session", scheduled_time="08:00", frequency="daily", priority="low")),
        ("Mochi", Task(description="Feed breakfast", scheduled_time="07:30", frequency="daily", priority="high")),
        ("Luna", Task(description="Vet appointment", scheduled_time="14:00", frequency="once", priority="medium")),
    ]

    for pet_name, task in tasks_to_add:
        scheduler.add_task_to_pet(pet_name, task)

    recurring_task = tasks_to_add[0][1]
    next_task = scheduler.mark_task_complete(recurring_task, pet_name="Mochi", owner=owner)

    all_pending_tasks = scheduler.get_pending_tasks(owner)
    sorted_tasks = scheduler.sort_by_time(all_pending_tasks)
    mochi_tasks = scheduler.filter_tasks(all_pending_tasks, pet_name="Mochi", completed=False, owner=owner)

    print("Today's Schedule")
    print("================")
    print("Sorted pending tasks:")
    for task in sorted_tasks:
        print(f"- {task.scheduled_time}: {task.description} ({task.priority})")

    print("\nMochi pending tasks:")
    for task in scheduler.sort_by_time(mochi_tasks):
        print(f"- {task.scheduled_time}: {task.description} ({task.priority})")

    conflict_warning = scheduler.get_conflict_warning(owner=owner)
    if conflict_warning is not None:
        print(f"\n{conflict_warning}")

    if next_task is not None:
        print("\nCreated next occurrence:")
        print(f"- {next_task.scheduled_time}: {next_task.description} ({next_task.priority})")


if __name__ == "__main__":
    main()
