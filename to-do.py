import streamlit as st

# --- Functions to manage state ---
def add_todo():
    """Adds a new task to the active list."""
    new_task = st.session_state["new_task"]
    if new_task:
        st.session_state.todos.append(new_task)
        st.session_state["new_task"] = ""  # Clear input

def complete_todo(index):
    """Moves a task from active list to history."""
    task = st.session_state.todos.pop(index)
    st.session_state.history.append(task)

def delete_active_task(index):
    """Permanently removes a task from the active list."""
    st.session_state.todos.pop(index)

def delete_history_task(index):
    """Permanently removes a task from the history list."""
    st.session_state.history.pop(index)

def clear_all_active():
    """Clears all active tasks."""
    st.session_state.todos = []

def clear_all_history():
    """Clears all history."""
    st.session_state.history = []

# --- App Configuration ---
st.set_page_config(page_title="Streamlit To-Do")
st.title("Streamlit To-Do App")

# --- Initialize State ---
if "todos" not in st.session_state:
    st.session_state.todos = []
if "history" not in st.session_state:
    st.session_state.history = []

# --- Input Section ---
st.text_input("Add a new task:", on_change=add_todo, key="new_task")

# --- Active Tasks Section ---
st.subheader("Current Tasks")

if st.session_state.todos:
    # Add a Clear All button for active tasks
    if st.button("Clear All Active Tasks", type="primary"):
        clear_all_active()
        st.rerun()

    st.markdown("---")
    
    # Loop through tasks
    # We use enumerate to get the index needed for callbacks
    for i, task in enumerate(st.session_state.todos):
        col1, col2 = st.columns([0.8, 0.2])
        
        with col1:
            # The checkbox acts as the "Complete" trigger
            st.checkbox(
                label=task,
                key=f"active_{i}",
                value=False,
                on_change=complete_todo,
                args=(i,)
            )
        with col2:
            # A separate button to delete without moving to history
            if st.button("🗑", key=f"del_active_{i}"):
                delete_active_task(i)
                st.rerun()
else:
    st.info("No active tasks! Add one above.")

# --- History Section ---
if st.session_state.history:
    st.markdown("---")
    st.subheader("History (Completed)")
    
    # Add a Clear All button for history
    if st.button("Clear All History"):
        clear_all_history()
        st.rerun()

    for i, task in enumerate(st.session_state.history):
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            st.markdown(f"~~{task}~~") # Strikethrough text
        with col2:
            if st.button("❌", key=f"del_hist_{i}"):
                delete_history_task(i)
                st.rerun()
