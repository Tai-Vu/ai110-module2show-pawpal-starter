import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Pet and Task Inputs")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if "owner" not in st.session_state or st.session_state.owner is None:
    st.session_state.owner = Owner(name=owner_name)
    st.session_state.scheduler = Scheduler(owner=st.session_state.owner)
else:
    st.session_state.owner.name = owner_name

owner = st.session_state.owner
scheduler = st.session_state.scheduler
scheduler.set_owner(owner)

st.markdown("### Tasks")
st.caption("Add a few tasks and build a daily plan using the backend logic.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    task_time = st.text_input("Scheduled time", value="09:00")
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    pet = owner.get_pet(pet_name)
    if pet is None:
        pet = Pet(name=pet_name, species=species)
        owner.add_pet(pet)

    task = Task(description=task_title, scheduled_time=task_time, priority=priority)
    pet.add_task(task)
    st.success(f"Added '{task_title}' to {pet.name}.")

all_tasks = owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    st.table([task.to_dict() for task in all_tasks])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button uses the scheduler to create a daily plan.")

if st.button("Generate schedule"):
    plan = scheduler.build_daily_plan(owner)
    if plan:
        st.write("Today's schedule")
        st.table([
            {
                "time": task.scheduled_time,
                "task": task.description,
                "priority": task.priority,
            }
            for task in plan
        ])
    else:
        st.info("No pending tasks to schedule yet.")
