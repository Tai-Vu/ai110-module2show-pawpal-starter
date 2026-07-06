from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner(name="Jordan")

    mochi = Pet(name="Mochi", species="dog", age="3")
    luna = Pet(name="Luna", species="cat", age="2")

    owner.add_pet(mochi)
    owner.add_pet(luna)

    tasks = [
        Task(description="Morning walk", scheduled_time="08:00", frequency="daily", priority="high"),
        Task(description="Feed breakfast", scheduled_time="07:30", frequency="daily", priority="high"),
        Task(description="Vet appointment", scheduled_time="14:00", frequency="once", priority="medium"),
        Task(description="Play session", scheduled_time="18:00", frequency="daily", priority="low"),
    ]

    scheduler = Scheduler(owner=owner)
    for task in tasks:
        if task.description == "Morning walk":
            scheduler.add_task_to_pet("Mochi", task)
        elif task.description == "Feed breakfast":
            scheduler.add_task_to_pet("Mochi", task)
        elif task.description == "Vet appointment":
            scheduler.add_task_to_pet("Luna", task)
        else:
            scheduler.add_task_to_pet("Luna", task)

    print("Today's Schedule")
    print("================")
    for task in scheduler.build_daily_plan(owner):
        print(f"- {task.scheduled_time}: {task.description} ({task.priority})")


if __name__ == "__main__":
    main()
