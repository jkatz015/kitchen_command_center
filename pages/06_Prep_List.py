"""
Kitchen Command Center - Prep List
Checklist with quantities and completion tracking for kitchen prep
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta

# Page configuration
st.set_page_config(
    page_title="Prep List",
    page_icon="📝",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .prep-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        border-left: 4px solid #0ea5e9;
    }
    .prep-urgent {
        border-left-color: #ef4444;
        background-color: #fef2f2;
    }
    .prep-high {
        border-left-color: #f59e0b;
        background-color: #fffbeb;
    }
    .prep-medium {
        border-left-color: #3b82f6;
        background-color: #eff6ff;
    }
    .prep-low {
        border-left-color: #10b981;
        background-color: #f0fdf4;
    }
    .prep-completed {
        border-left-color: #6b7280;
        background-color: #f9fafb;
        opacity: 0.7;
    }
    .category-header {
        background-color: #f8fafc;
        padding: 0.5rem;
        border-radius: 0.5rem;
        border: 2px solid #e2e8f0;
        text-align: center;
        font-weight: bold;
        margin: 1rem 0;
    }
    .quantity-input {
        width: 80px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'prep_items' not in st.session_state:
    st.session_state.prep_items = [
        {
            'id': 'PREP-001', 'name': 'Onions diced', 'category': 'mise-en-place',
            'quantity_needed': 2, 'unit': 'lbs', 'quantity_completed': 2,
            'status': 'completed', 'priority': 'medium', 'assigned_to': 'Chef Mike',
            'notes': 'For tonight\'s service', 'created_date': date.today()
        },
        {
            'id': 'PREP-002', 'name': 'Garlic minced', 'category': 'mise-en-place',
            'quantity_needed': 1, 'unit': 'cup', 'quantity_completed': 1,
            'status': 'completed', 'priority': 'medium', 'assigned_to': 'Chef Mike',
            'notes': '', 'created_date': date.today()
        },
        {
            'id': 'PREP-003', 'name': 'Chicken breast trimmed', 'category': 'protein',
            'quantity_needed': 15, 'unit': 'pieces', 'quantity_completed': 12,
            'status': 'in-progress', 'priority': 'high', 'assigned_to': 'Chef Sarah',
            'notes': 'Need 12 portions', 'created_date': date.today()
        },
        {
            'id': 'PREP-004', 'name': 'Salmon portioned', 'category': 'protein',
            'quantity_needed': 3, 'unit': 'lbs', 'quantity_completed': 0,
            'status': 'pending', 'priority': 'urgent', 'assigned_to': 'Chef Sarah',
            'notes': 'VIP table order', 'created_date': date.today()
        },
        {
            'id': 'PREP-005', 'name': 'Béarnaise sauce', 'category': 'sauce',
            'quantity_needed': 1, 'unit': 'batch', 'quantity_completed': 0,
            'status': 'behind', 'priority': 'urgent', 'assigned_to': 'Sauce Station',
            'notes': 'Running low', 'created_date': date.today()
        },
        {
            'id': 'PREP-006', 'name': 'Hollandaise ready', 'category': 'sauce',
            'quantity_needed': 1, 'unit': 'batch', 'quantity_completed': 0,
            'status': 'behind', 'priority': 'urgent', 'assigned_to': 'Sauce Station',
            'notes': '', 'created_date': date.today()
        },
        {
            'id': 'PREP-007', 'name': 'Carrots julienne', 'category': 'vegetables',
            'quantity_needed': 3, 'unit': 'lbs', 'quantity_completed': 1,
            'status': 'in-progress', 'priority': 'medium', 'assigned_to': 'Prep Station',
            'notes': 'For tonight\'s special', 'created_date': date.today()
        },
        {
            'id': 'PREP-008', 'name': 'Mushrooms sautéed', 'category': 'vegetables',
            'quantity_needed': 2, 'unit': 'lbs', 'quantity_completed': 0,
            'status': 'pending', 'priority': 'high', 'assigned_to': 'Prep Station',
            'notes': '', 'created_date': date.today()
        },
        {
            'id': 'PREP-009', 'name': 'Parsley garnish', 'category': 'garnish',
            'quantity_needed': 1, 'unit': 'bunch', 'quantity_completed': 1,
            'status': 'completed', 'priority': 'low', 'assigned_to': 'Garnish Station',
            'notes': '', 'created_date': date.today()
        },
        {
            'id': 'PREP-010', 'name': 'Lemon wedges', 'category': 'garnish',
            'quantity_needed': 50, 'unit': 'pieces', 'quantity_completed': 30,
            'status': 'in-progress', 'priority': 'medium', 'assigned_to': 'Garnish Station',
            'notes': '', 'created_date': date.today()
        }
    ]

def get_priority_color(priority):
    """Get color for prep priority"""
    colors = {
        'urgent': '#ef4444',
        'high': '#f59e0b',
        'medium': '#3b82f6',
        'low': '#10b981'
    }
    return colors.get(priority, '#6b7280')

def display_prep_overview(prep_items):
    """Display prep overview metrics"""
    st.subheader("📊 Prep Overview")

    total_items = len(prep_items)
    completed_items = len([item for item in prep_items if item['status'] == 'completed'])
    in_progress_items = len([item for item in prep_items if item['status'] == 'in-progress'])
    pending_items = len([item for item in prep_items if item['status'] == 'pending'])
    behind_items = len([item for item in prep_items if item['status'] == 'behind'])

    # Calculate completion percentage
    completion_percentage = (completed_items / total_items * 100) if total_items > 0 else 0

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total Items", total_items)

    with col2:
        st.metric("Completed", completed_items)

    with col3:
        st.metric("In Progress", in_progress_items)

    with col4:
        st.metric("Pending", pending_items)

    with col5:
        st.metric("Behind", behind_items, delta="Action needed" if behind_items > 0 else None)

    # Progress bar
    st.progress(completion_percentage / 100)
    st.caption(f"Overall Completion: {completion_percentage:.1f}%")

def display_prep_by_category(prep_items):
    """Display prep items grouped by category"""
    st.subheader("📋 Prep List by Category")

    # Group items by category
    categories = {}
    for item in prep_items:
        category = item['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(item)

    # Display each category
    for category, items in categories.items():
        st.markdown(f"""
        <div class="category-header">
            {category.replace('-', ' ').title()} ({len(items)} items)
        </div>
        """, unsafe_allow_html=True)

        # Sort items by priority and status
        priority_order = {'urgent': 0, 'high': 1, 'medium': 2, 'low': 3}
        status_order = {'behind': 0, 'pending': 1, 'in-progress': 2, 'completed': 3}

        items.sort(key=lambda x: (status_order.get(x['status'], 4), priority_order.get(x['priority'], 4)))

        for item in items:
            priority_color = get_priority_color(item['priority'])
            priority_class = f"prep-{item['priority']}"

            if item['status'] == 'completed':
                priority_class += " prep-completed"

            with st.container():
                col1, col2, col3, col4, col5 = st.columns([3, 2, 1, 1, 1])

                with col1:
                    st.markdown(f"""
                    <div class="prep-card {priority_class}">
                        <h4>{item['name']}</h4>
                        <p><strong>Assigned to:</strong> {item['assigned_to']}</p>
                        {f"<p><strong>Notes:</strong> {item['notes']}</p>" if item['notes'] else ""}
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    # Quantity tracking
                    st.markdown(f"**Quantity:** {item['quantity_completed']}/{item['quantity_needed']} {item['unit']}")

                    # Progress bar for quantity
                    if item['quantity_needed'] > 0:
                        progress = item['quantity_completed'] / item['quantity_needed']
                        st.progress(progress)

                    # Quantity input
                    new_quantity = st.number_input(
                        "Update",
                        min_value=0,
                        max_value=item['quantity_needed'] * 2,
                        value=item['quantity_completed'],
                        key=f"qty_{item['id']}"
                    )

                    if new_quantity != item['quantity_completed']:
                        item['quantity_completed'] = new_quantity
                        if new_quantity >= item['quantity_needed']:
                            item['status'] = 'completed'
                        elif new_quantity > 0:
                            item['status'] = 'in-progress'
                        else:
                            item['status'] = 'pending'
                        st.rerun()

                with col3:
                    st.markdown(f'<span style="color: {priority_color}">{item["priority"].title()}</span>',
                               unsafe_allow_html=True)

                with col4:
                    status_color = {
                        'completed': '#10b981',
                        'in-progress': '#3b82f6',
                        'pending': '#f59e0b',
                        'behind': '#ef4444'
                    }.get(item['status'], '#6b7280')

                    st.markdown(f'<span style="color: {status_color}">{item["status"].replace("-", " ").title()}</span>',
                               unsafe_allow_html=True)

                with col5:
                    if item['status'] != 'completed':
                        if st.button(f"Complete {item['id']}", key=f"complete_{item['id']}"):
                            item['status'] = 'completed'
                            item['quantity_completed'] = item['quantity_needed']
                            st.success(f"Completed {item['name']}")
                            st.rerun()
                    else:
                        st.success("✅ Done")

def display_prep_summary(prep_items):
    """Display prep summary by category"""
    st.subheader("📈 Prep Summary")

    # Group by category and calculate stats
    category_stats = {}
    for item in prep_items:
        category = item['category']
        if category not in category_stats:
            category_stats[category] = {
                'total': 0, 'completed': 0, 'in_progress': 0, 'pending': 0, 'behind': 0
            }

        category_stats[category]['total'] += 1
        category_stats[category][item['status']] += 1

    # Display category summary
    cols = st.columns(len(category_stats))

    for i, (category, stats) in enumerate(category_stats.items()):
        with cols[i]:
            completion_rate = (stats['completed'] / stats['total'] * 100) if stats['total'] > 0 else 0

            st.metric(
                category.replace('-', ' ').title(),
                f"{stats['completed']}/{stats['total']}",
                f"{completion_rate:.1f}%"
            )

            # Progress bar
            st.progress(completion_rate / 100)

def display_prep_form():
    """Display form to add new prep items"""
    st.subheader("➕ Add New Prep Item")

    with st.form("add_prep_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Item Name", placeholder="e.g., Onions diced")
            category = st.selectbox("Category", ["mise-en-place", "protein", "sauce", "vegetables", "garnish", "other"])
            quantity_needed = st.number_input("Quantity Needed", min_value=1, value=1)
            unit = st.text_input("Unit", placeholder="e.g., lbs, cups, pieces")

        with col2:
            assigned_to = st.selectbox("Assign to", ["Chef Mike", "Chef Sarah", "Chef Alex", "Sauce Station", "Prep Station", "Garnish Station"])
            priority = st.selectbox("Priority", ["low", "medium", "high", "urgent"])
            status = st.selectbox("Status", ["pending", "in-progress"])
            notes = st.text_area("Notes", placeholder="Any special instructions...")

        submitted = st.form_submit_button("Add Prep Item", type="primary")

        if submitted:
            if name and unit:
                new_prep_item = {
                    'id': f'PREP-{len(st.session_state.prep_items) + 1:03d}',
                    'name': name,
                    'category': category,
                    'quantity_needed': quantity_needed,
                    'unit': unit,
                    'quantity_completed': 0,
                    'status': status,
                    'priority': priority,
                    'assigned_to': assigned_to,
                    'notes': notes,
                    'created_date': date.today()
                }

                st.session_state.prep_items.append(new_prep_item)
                st.success("Prep item added successfully!")
                st.rerun()
            else:
                st.error("Please fill in item name and unit")

def display_prep_analytics(prep_items):
    """Display prep analytics"""
    st.subheader("📊 Prep Analytics")

    col1, col2 = st.columns(2)

    with col1:
        # Status distribution
        status_counts = pd.Series([item['status'] for item in prep_items]).value_counts()
        st.bar_chart(status_counts)
        st.caption("Items by Status")

    with col2:
        # Priority distribution
        priority_counts = pd.Series([item['priority'] for item in prep_items]).value_counts()
        st.bar_chart(priority_counts)
        st.caption("Items by Priority")

    # Category completion rates
    st.subheader("📈 Category Completion Rates")
    category_completion = {}

    for item in prep_items:
        category = item['category']
        if category not in category_completion:
            category_completion[category] = {'total': 0, 'completed': 0}

        category_completion[category]['total'] += 1
        if item['status'] == 'completed':
            category_completion[category]['completed'] += 1

    completion_data = []
    for category, stats in category_completion.items():
        completion_rate = (stats['completed'] / stats['total'] * 100) if stats['total'] > 0 else 0
        completion_data.append({
            'Category': category.replace('-', ' ').title(),
            'Completion Rate': completion_rate
        })

    if completion_data:
        completion_df = pd.DataFrame(completion_data)
        st.bar_chart(completion_df.set_index('Category'))
        st.caption("Completion Rate by Category")

def main():
    """Main prep list function"""

    st.title("📝 Prep List")
    st.markdown("Checklist with quantities and completion tracking for kitchen prep")

    # Load data
    prep_items = st.session_state.prep_items

    # Display overview
    display_prep_overview(prep_items)

    st.markdown("---")

    # Display prep by category
    display_prep_by_category(prep_items)

    st.markdown("---")

    # Display prep summary
    display_prep_summary(prep_items)

    st.markdown("---")

    # Display analytics
    display_prep_analytics(prep_items)

    st.markdown("---")

    # Add new prep item form
    display_prep_form()

    # Footer
    st.markdown("---")
    st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

if __name__ == "__main__":
    main()
