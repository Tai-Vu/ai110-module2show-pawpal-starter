import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(135deg, #2b1630 0%, #5a2848 45%, #2f4b69 100%);
        }
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }
        .hero-card {
            background: linear-gradient(135deg, #ffd6e0 0%, #ffe4b5 100%);
            border-radius: 20px;
            padding: 1.5rem;
            color: #6a2e2e;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
            margin-bottom: 1rem;
        }
        .section-card {
            background: rgba(255, 255, 255, 0.95);
            border: 1px solid #f0b8c8;
            border-radius: 16px;
            padding: 1rem 1.2rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
            color: #3e2a2a;
        }
        .section-card p, .section-card li, .section-card .stMarkdown {
            color: #3e2a2a;
        }
        div.stButton > button {
            background: linear-gradient(135deg, #ff7aa2 0%, #ffb347 100%);
            color: white;
            border: none;
            border-radius: 999px;
            padding: 0.55rem 1rem;
            font-weight: 700;
        }
        div.stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-card">
        <h1>🐾 PawPal+</h1>
        <p>Your cheerful planner for keeping pet care simple, sweet, and on time.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-card">
        <strong>Welcome, pet lovers!</strong> This friendly planner helps you add pet tasks, view a tidy schedule,
        and spot conflicts before they become stressful.
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("Why PawPal+ helps", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner organize walks, feeding, appointments,
and daily routines with a playful, easy-to-follow experience.
"""
    )

with st.expander("What you can do here", expanded=True):
    st.markdown(
        """
- Add a pet and create care tasks in seconds
- Choose a time and priority for each task
- See your plan sorted by time and priority
- Notice scheduling conflicts with friendly warnings
"""
    )

st.divider()

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("🐶 Add a pet and plan their day")
st.caption("Create a happy routine for your furry friend with just a few clicks.")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
st.markdown('</div>', unsafe_allow_html=True)

if "owner" not in st.session_state or st.session_state.owner is None:
    st.session_state.owner = Owner(name=owner_name)
    st.session_state.scheduler = Scheduler(owner=st.session_state.owner)
else:
    st.session_state.owner.name = owner_name

owner = st.session_state.owner
scheduler = st.session_state.scheduler
scheduler.set_owner(owner)

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown("### 📝 Tasks")
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
    st.subheader("Current tasks")
    task_rows = []
    for task in all_tasks:
        pet_name_for_task = next(
            (pet.name for pet in owner.pets if task in pet.get_tasks()),
            "Unknown",
        )
        task_rows.append(
            {
                "pet": pet_name_for_task,
                "time": task.scheduled_time,
                "task": task.description,
                "priority": task.priority,
                "status": "Complete" if task.completed else "Pending",
            }
        )
    st.table(task_rows)
else:
    st.info("No tasks yet. Add one above.")

pending_tasks = scheduler.get_pending_tasks(owner)
if pending_tasks:
    sorted_pending_tasks = scheduler.sort_by_time(pending_tasks)
    st.success("Pending tasks are organized by scheduled time.")
    st.table(
        [
            {
                "time": task.scheduled_time,
                "task": task.description,
                "priority": task.priority,
            }
            for task in sorted_pending_tasks
        ]
    )

    pet_tasks = scheduler.filter_tasks(pending_tasks, pet_name=pet_name, completed=False, owner=owner)
    if pet_tasks:
        st.subheader(f"{pet_name}'s pending tasks")
        st.table(
            [
                {
                    "time": task.scheduled_time,
                    "task": task.description,
                    "priority": task.priority,
                }
                for task in scheduler.sort_by_time(pet_tasks)
            ]
        )

conflict_warning = scheduler.get_conflict_warning(owner=owner)
if conflict_warning is not None:
    st.warning(conflict_warning)

st.markdown('</div>', unsafe_allow_html=True)
st.divider()

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("✨ Build Schedule")
st.caption("This button uses the scheduler to create a daily plan.")

if st.button("Generate schedule"):
    plan = scheduler.build_daily_plan(owner)
    if plan:
        st.success("Today's schedule is ready.")
        st.table(
            [
                {
                    "time": task.scheduled_time,
                    "task": task.description,
                    "priority": task.priority,
                }
                for task in plan
            ]
        )
    else:
        st.info("No pending tasks to schedule yet.")

st.markdown('</div>', unsafe_allow_html=True)
