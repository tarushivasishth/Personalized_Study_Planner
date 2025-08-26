import streamlit as st
from utils import predict_time
from scheduler import Task, schedule_tasks

levels = {
    "Easy": 1,
    "Medium": 2,
    "Hard": 3
}

st.set_page_config(page_title="📚 Personalized Study Planner", layout="centered")

st.title("📅 Personalized Study Planner")

# --- Session state to store tasks & daily hours ---
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "hours_per_day" not in st.session_state:
    st.session_state.hours_per_day = None

# --- Fix daily hours once ---
if st.session_state.hours_per_day is None:
    st.session_state.hours_per_day = st.number_input(
        "⏱️ Study Hours per Day", min_value=1, max_value=12, value=6, step=1
    )

# --- Input Form ---
st.subheader("➕ Add a new subject")

with st.form("study_form", clear_on_submit=True):
    subject = st.text_input("Enter Subject")
    deadline = st.number_input("Enter Deadline (in days)", min_value=1, step=1)
    difficulty = st.selectbox("Select Difficulty", options=["Easy", "Medium", "Hard"])
    prev_score = st.number_input("Previous Score (%)", min_value=0, max_value=100, step=1)

    add_task = st.form_submit_button("➕ Add Task")

    if add_task:
        if not subject:
            st.warning("⚠️ Please enter a subject before adding.")
        else:
            # Predict study time
            predicted_time = predict_time(deadline, difficulty, prev_score)

            # Calculate max possible hours before deadline
            max_possible = deadline * st.session_state.hours_per_day
            if predicted_time > max_possible:
                st.warning(
                    f"⚠️ For **{subject}**, predicted {predicted_time} hrs "
                    f"cannot fit into {deadline} days × {st.session_state.hours_per_day} hrs/day. "
                    f"You may need ~{round(predicted_time/deadline,1)} hrs/day."
                )

            # Create task
            task = Task(
                subject,
                deadline,
                levels[difficulty],
                predicted_time,
                previous_score=prev_score
            )
            

            st.session_state.tasks.append(task)
            st.success(f"✅ Added task for **{subject}** (Predicted: {predicted_time} hrs)")

# --- Display added tasks ---
if st.session_state.tasks:
    st.subheader("📋 Added Subjects")
    for idx, t in enumerate(st.session_state.tasks, 1):
        st.write(
            f"**{idx}. {t.subject}** | Deadline: {t.deadline} days | "
            f"Difficulty: {t.difficulty} | Predicted: {t.predicted_time} hrs | "
            f"Prev Score: {t.previous_score}"
        )

# --- Generate Final Schedule ---
if st.button("🗓️ Generate Study Plan"):
    if not st.session_state.tasks:
        st.warning("⚠️ Please add at least one subject.")
    else:
        with st.spinner("🔮 Creating your personalized study schedule..."):
            schedule = schedule_tasks(
                st.session_state.tasks, hours_per_day=st.session_state.hours_per_day
            )

        st.success("✅ Study Plan Generated!")

        st.subheader("📌 Study Schedule")
        for day, tasks in schedule.items():
            total_hours = sum([t[1] for t in tasks])
            st.progress(min(total_hours / st.session_state.hours_per_day, 1.0))

            with st.expander(f"{day}"):
                for t in tasks:
                    st.write(f"📖 {t[0]} → {t[1]} hrs")
