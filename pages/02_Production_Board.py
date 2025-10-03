"""
Kitchen Command Center - Production Board
Real-time kitchen operations and order management
"""

import streamlit as st
import pandas as pd
from datetime import date, datetime

# Page configuration
st.set_page_config(
    page_title="Production Board",
    page_icon="👩‍🍳",
    layout="wide"
)

# Initialize session state
if 'tasks' not in st.session_state:
    st.session_state.tasks = [
        {"Task":"Beer Cheese Soup","Batch":"2x","Station":"Sauce","Owner":"Alex","Done":False},
        {"Task":"Reuben Soup","Batch":"1x","Station":"Soup","Owner":"Sam","Done":False},
        {"Task":"Candied Pepitas","Batch":"3x","Station":"Garde Manger","Owner":"J","Done":True},
    ]

def main():
    """Main production board function"""

    st.title("👩‍🍳 Production Board")

    # Date input
    production_date = st.date_input("Production Date", value=date.today())

    # Task editor
    st.subheader("📋 Production Tasks")

    # Update tasks in session state
    updated_tasks = st.data_editor(
        st.session_state.tasks,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Task": st.column_config.TextColumn("Task", width="medium"),
            "Batch": st.column_config.TextColumn("Batch", width="small"),
            "Station": st.column_config.SelectboxColumn(
                "Station",
                options=["Sauce", "Soup", "Garde Manger", "Grill", "Fry", "Pasta", "Salad"],
                width="medium"
            ),
            "Owner": st.column_config.TextColumn("Owner", width="small"),
            "Done": st.column_config.CheckboxColumn("Done", width="small")
        }
    )

    # Update session state with changes
    st.session_state.tasks = updated_tasks

    # Display summary
    total_tasks = len(st.session_state.tasks)
    completed_tasks = sum(1 for task in st.session_state.tasks if task.get('Done', False))
    pending_tasks = total_tasks - completed_tasks

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Tasks", total_tasks)

    with col2:
        st.metric("Completed", completed_tasks)

    with col3:
        st.metric("Pending", pending_tasks)

    # Progress bar
    if total_tasks > 0:
        progress = completed_tasks / total_tasks
        st.progress(progress)
        st.caption(f"Progress: {progress:.1%}")

    # Success message
    st.success("Changes are saved in session. Hook this to a Google Sheet/DB later.")

    # Footer
    st.markdown("---")
    st.markdown(f"*Production Date: {production_date} | Last updated: {datetime.now().strftime('%H:%M:%S')}*")

if __name__ == "__main__":
    main()
