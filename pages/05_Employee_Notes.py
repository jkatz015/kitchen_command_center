"""
Kitchen Command Center - Employee Notes
Task management system with assignments for kitchen staff
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta

# Page configuration
st.set_page_config(
    page_title="Employee Notes",
    page_icon="👥",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .task-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        border-left: 4px solid #0ea5e9;
    }
    .task-urgent {
        border-left-color: #ef4444;
        background-color: #fef2f2;
    }
    .task-high {
        border-left-color: #f59e0b;
        background-color: #fffbeb;
    }
    .task-medium {
        border-left-color: #3b82f6;
        background-color: #eff6ff;
    }
    .task-low {
        border-left-color: #10b981;
        background-color: #f0fdf4;
    }
    .task-completed {
        border-left-color: #6b7280;
        background-color: #f9fafb;
        opacity: 0.7;
    }
    .employee-card {
        background-color: #f8fafc;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px solid #e2e8f0;
        text-align: center;
    }
    .employee-busy {
        border-color: #ef4444;
        background-color: #fef2f2;
    }
    .employee-available {
        border-color: #10b981;
        background-color: #f0fdf4;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'tasks' not in st.session_state:
    st.session_state.tasks = [
        {
            'id': 'TASK-001', 'title': 'Deep clean grill station',
            'description': 'Complete deep cleaning of grill station including grates, burners, and surrounding area',
            'assigned_to': 'Chef Mike', 'priority': 'high', 'status': 'pending',
            'due_date': date.today(), 'created_date': date.today() - timedelta(days=1),
            'estimated_duration': 60, 'category': 'cleaning'
        },
        {
            'id': 'TASK-002', 'title': 'Inventory count - protein section',
            'description': 'Count and record all protein items in walk-in cooler',
            'assigned_to': 'Chef Sarah', 'priority': 'medium', 'status': 'in-progress',
            'due_date': date.today() + timedelta(days=1), 'created_date': date.today() - timedelta(days=2),
            'estimated_duration': 30, 'category': 'inventory'
        },
        {
            'id': 'TASK-003', 'title': 'Prep mise en place for tomorrow',
            'description': 'Prepare all mise en place items for tomorrow\'s service',
            'assigned_to': 'Chef Alex', 'priority': 'urgent', 'status': 'pending',
            'due_date': date.today(), 'created_date': date.today(),
            'estimated_duration': 120, 'category': 'prep'
        },
        {
            'id': 'TASK-004', 'title': 'Fix broken dishwasher',
            'description': 'Call maintenance and coordinate dishwasher repair',
            'assigned_to': 'Manager Lisa', 'priority': 'urgent', 'status': 'completed',
            'due_date': date.today() - timedelta(days=1), 'created_date': date.today() - timedelta(days=3),
            'estimated_duration': 45, 'category': 'maintenance'
        },
        {
            'id': 'TASK-005', 'title': 'Update menu boards',
            'description': 'Update daily specials on all menu boards',
            'assigned_to': 'Server John', 'priority': 'low', 'status': 'pending',
            'due_date': date.today(), 'created_date': date.today(),
            'estimated_duration': 15, 'category': 'service'
        }
    ]

if 'employees' not in st.session_state:
    st.session_state.employees = [
        {'name': 'Chef Mike', 'role': 'Head Chef', 'status': 'available', 'current_tasks': 2},
        {'name': 'Chef Sarah', 'role': 'Sous Chef', 'status': 'busy', 'current_tasks': 3},
        {'name': 'Chef Alex', 'role': 'Line Cook', 'status': 'available', 'current_tasks': 1},
        {'name': 'Manager Lisa', 'role': 'Kitchen Manager', 'status': 'available', 'current_tasks': 1},
        {'name': 'Server John', 'role': 'Server', 'status': 'busy', 'current_tasks': 2},
        {'name': 'Dishwasher Tom', 'role': 'Dishwasher', 'status': 'available', 'current_tasks': 0}
    ]

def get_priority_color(priority):
    """Get color for task priority"""
    colors = {
        'urgent': '#ef4444',
        'high': '#f59e0b',
        'medium': '#3b82f6',
        'low': '#10b981'
    }
    return colors.get(priority, '#6b7280')

def display_task_overview(tasks):
    """Display task overview metrics"""
    st.subheader("📊 Task Overview")

    total_tasks = len(tasks)
    pending_tasks = len([t for t in tasks if t['status'] == 'pending'])
    in_progress_tasks = len([t for t in tasks if t['status'] == 'in-progress'])
    completed_tasks = len([t for t in tasks if t['status'] == 'completed'])
    overdue_tasks = len([t for t in tasks if t['status'] != 'completed' and t['due_date'] < date.today()])

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total Tasks", total_tasks)

    with col2:
        st.metric("Pending", pending_tasks)

    with col3:
        st.metric("In Progress", in_progress_tasks)

    with col4:
        st.metric("Completed", completed_tasks)

    with col5:
        st.metric("Overdue", overdue_tasks, delta="Action needed" if overdue_tasks > 0 else None)

def display_employee_status(employees):
    """Display employee status"""
    st.subheader("👥 Employee Status")

    cols = st.columns(len(employees))

    for i, employee in enumerate(employees):
        with cols[i]:
            status_class = "employee-busy" if employee['status'] == 'busy' else "employee-available"
            status_color = "#ef4444" if employee['status'] == 'busy' else "#10b981"

            st.markdown(f"""
            <div class="employee-card {status_class}">
                <h4>{employee['name']}</h4>
                <p><strong>Role:</strong> {employee['role']}</p>
                <p><strong>Status:</strong> <span style="color: {status_color}">{employee['status'].title()}</span></p>
                <p><strong>Tasks:</strong> {employee['current_tasks']}</p>
            </div>
            """, unsafe_allow_html=True)

def display_task_list(tasks, filter_status=None, filter_employee=None):
    """Display task list with filters"""
    st.subheader("📋 Task List")

    # Apply filters
    filtered_tasks = tasks
    if filter_status and filter_status != "All":
        filtered_tasks = [t for t in filtered_tasks if t['status'] == filter_status]
    if filter_employee and filter_employee != "All":
        filtered_tasks = [t for t in filtered_tasks if t['assigned_to'] == filter_employee]

    if not filtered_tasks:
        st.info("No tasks match the current filters.")
        return

    # Sort by priority and due date
    priority_order = {'urgent': 0, 'high': 1, 'medium': 2, 'low': 3}
    filtered_tasks.sort(key=lambda x: (priority_order.get(x['priority'], 4), x['due_date']))

    for task in filtered_tasks:
        priority_color = get_priority_color(task['priority'])
        priority_class = f"task-{task['priority']}"

        if task['status'] == 'completed':
            priority_class += " task-completed"

        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])

            with col1:
                st.markdown(f"""
                <div class="task-card {priority_class}">
                    <h4>{task['title']}</h4>
                    <p>{task['description']}</p>
                    <p><strong>Category:</strong> {task['category'].title()} | <strong>Duration:</strong> {task['estimated_duration']} min</p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"**Assigned to:** {task['assigned_to']}")
                st.markdown(f"**Due Date:** {task['due_date']}")
                st.markdown(f"**Created:** {task['created_date']}")

                # Show overdue warning
                if task['status'] != 'completed' and task['due_date'] < date.today():
                    st.error("⚠️ Overdue!")

            with col3:
                st.markdown(f'<span style="color: {priority_color}">{task["priority"].title()}</span>',
                           unsafe_allow_html=True)
                st.markdown(f"**Status:** {task['status'].replace('-', ' ').title()}")

            with col4:
                if task['status'] == 'pending':
                    if st.button(f"Start {task['id']}", key=f"start_{task['id']}"):
                        task['status'] = 'in-progress'
                        st.success(f"Started task: {task['title']}")
                        st.rerun()
                elif task['status'] == 'in-progress':
                    if st.button(f"Complete {task['id']}", key=f"complete_{task['id']}"):
                        task['status'] = 'completed'
                        st.success(f"Completed task: {task['title']}")
                        st.rerun()
                elif task['status'] == 'completed':
                    st.success("✅ Done")

def display_task_filters(tasks, employees):
    """Display task filters"""
    st.subheader("🔍 Filters")

    col1, col2, col3 = st.columns(3)

    with col1:
        status_options = ["All"] + list(set(task['status'] for task in tasks))
        filter_status = st.selectbox("Filter by Status", status_options)

    with col2:
        employee_options = ["All"] + list(set(task['assigned_to'] for task in tasks))
        filter_employee = st.selectbox("Filter by Employee", employee_options)

    with col3:
        category_options = ["All"] + list(set(task['category'] for task in tasks))
        filter_category = st.selectbox("Filter by Category", category_options)

    return filter_status, filter_employee, filter_category

def display_task_form():
    """Display form to add new tasks"""
    st.subheader("➕ Add New Task")

    with st.form("add_task_form"):
        col1, col2 = st.columns(2)

        with col1:
            title = st.text_input("Task Title", placeholder="e.g., Clean prep station")
            description = st.text_area("Description", placeholder="Detailed description of the task...")
            assigned_to = st.selectbox("Assign to", [emp['name'] for emp in st.session_state.employees])
            priority = st.selectbox("Priority", ["low", "medium", "high", "urgent"])

        with col2:
            due_date = st.date_input("Due Date", value=date.today())
            estimated_duration = st.number_input("Estimated Duration (minutes)", min_value=5, max_value=480, value=30)
            category = st.selectbox("Category", ["cleaning", "prep", "inventory", "maintenance", "service", "other"])
            status = st.selectbox("Status", ["pending", "in-progress"])

        submitted = st.form_submit_button("Add Task", type="primary")

        if submitted:
            if title and description:
                new_task = {
                    'id': f'TASK-{len(st.session_state.tasks) + 1:03d}',
                    'title': title,
                    'description': description,
                    'assigned_to': assigned_to,
                    'priority': priority,
                    'status': status,
                    'due_date': due_date,
                    'created_date': date.today(),
                    'estimated_duration': estimated_duration,
                    'category': category
                }

                st.session_state.tasks.append(new_task)
                st.success("Task added successfully!")
                st.rerun()
            else:
                st.error("Please fill in title and description")

def display_task_analytics(tasks, employees):
    """Display task analytics"""
    st.subheader("📈 Task Analytics")

    col1, col2 = st.columns(2)

    with col1:
        # Tasks by status
        status_counts = pd.Series([task['status'] for task in tasks]).value_counts()
        st.bar_chart(status_counts)
        st.caption("Tasks by Status")

    with col2:
        # Tasks by priority
        priority_counts = pd.Series([task['priority'] for task in tasks]).value_counts()
        st.bar_chart(priority_counts)
        st.caption("Tasks by Priority")

    # Employee workload
    st.subheader("👥 Employee Workload")
    employee_tasks = {}
    for task in tasks:
        if task['status'] != 'completed':
            employee = task['assigned_to']
            if employee not in employee_tasks:
                employee_tasks[employee] = 0
            employee_tasks[employee] += 1

    if employee_tasks:
        workload_df = pd.DataFrame(list(employee_tasks.items()), columns=['Employee', 'Active Tasks'])
        st.bar_chart(workload_df.set_index('Employee'))
        st.caption("Active Tasks per Employee")

def main():
    """Main employee notes function"""

    st.title("👥 Employee Notes")
    st.markdown("Task management system with assignments for kitchen staff")

    # Load data
    tasks = st.session_state.tasks
    employees = st.session_state.employees

    # Display overview
    display_task_overview(tasks)

    st.markdown("---")

    # Display employee status
    display_employee_status(employees)

    st.markdown("---")

    # Display filters
    filter_status, filter_employee, filter_category = display_task_filters(tasks, employees)

    st.markdown("---")

    # Display task list
    display_task_list(tasks, filter_status, filter_employee)

    st.markdown("---")

    # Display analytics
    display_task_analytics(tasks, employees)

    st.markdown("---")

    # Add new task form
    display_task_form()

    # Footer
    st.markdown("---")
    st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

if __name__ == "__main__":
    main()
