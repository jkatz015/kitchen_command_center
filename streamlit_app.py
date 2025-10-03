"""
Kitchen Command Center - Streamlit Version
A comprehensive kitchen management system with real-time updates
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import random
from typing import Dict, List, Any
import json

# Page configuration
st.set_page_config(
    page_title="Kitchen Command Center",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .status-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .urgent {
        border-left-color: #ff4444;
        background-color: #fff5f5;
    }
    .high {
        border-left-color: #ff8800;
        background-color: #fff8f0;
    }
    .medium {
        border-left-color: #ffaa00;
        background-color: #fffbf0;
    }
    .low {
        border-left-color: #00aa44;
        background-color: #f0fff5;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Sample data (equivalent to dummyData.ts)
@st.cache_data
def get_sample_data():
    """Load sample data for the kitchen management system"""

    reservations = [
        {
            'id': '1', 'partyName': 'Smith Party', 'time': '6:30 PM',
            'tableNumber': 12, 'guestCount': 4, 'status': 'confirmed',
            'specialRequests': ['Birthday celebration', 'High chair needed'],
            'phoneNumber': '(555) 123-4567'
        },
        {
            'id': '2', 'partyName': 'Johnson Family', 'time': '7:15 PM',
            'tableNumber': 8, 'guestCount': 6, 'status': 'pending',
            'specialRequests': ['Vegetarian options'],
            'phoneNumber': '(555) 234-5678'
        },
        {
            'id': '3', 'partyName': 'Williams', 'time': '8:00 PM',
            'tableNumber': 5, 'guestCount': 2, 'status': 'seated',
            'specialRequests': ['Anniversary dinner'],
            'phoneNumber': '(555) 345-6789'
        },
        {
            'id': '4', 'partyName': 'Brown Group', 'time': '8:45 PM',
            'tableNumber': 15, 'guestCount': 8, 'status': 'confirmed',
            'specialRequests': ['Business dinner', 'Quiet table preferred'],
            'phoneNumber': '(555) 456-7890'
        }
    ]

    prep_items = [
        {
            'id': '1', 'name': 'Onions diced', 'category': 'mise-en-place',
            'quantity': '2', 'unit': 'lbs', 'status': 'complete',
            'priority': 'medium', 'assignedTo': 'Chef Mike'
        },
        {
            'id': '2', 'name': 'Garlic minced', 'category': 'mise-en-place',
            'quantity': '1', 'unit': 'cup', 'status': 'complete',
            'priority': 'medium', 'assignedTo': 'Chef Mike'
        },
        {
            'id': '3', 'name': 'Chicken breast trimmed', 'category': 'protein',
            'quantity': '15', 'unit': 'pieces', 'status': 'complete',
            'priority': 'high', 'assignedTo': 'Chef Sarah'
        },
        {
            'id': '4', 'name': 'Salmon portioned', 'category': 'protein',
            'quantity': '3', 'unit': 'lbs', 'status': 'in-progress',
            'priority': 'high', 'assignedTo': 'Chef Sarah',
            'notes': 'Need 12 portions'
        },
        {
            'id': '5', 'name': 'Béarnaise sauce', 'category': 'sauce',
            'quantity': '1', 'unit': 'batch', 'status': 'behind',
            'priority': 'urgent', 'assignedTo': 'Sauce Station',
            'notes': 'Running low'
        }
    ]

    order_adds = [
        {
            'id': '1', 'tableNumber': 12, 'originalItem': 'Caesar Salad',
            'modification': 'Extra side salad - No dressing',
            'timestamp': datetime.now() - timedelta(minutes=2),
            'status': 'pending', 'priority': 'medium'
        },
        {
            'id': '2', 'tableNumber': 8, 'originalItem': 'Burger Deluxe',
            'modification': 'No onions - Extra pickles',
            'timestamp': datetime.now() - timedelta(minutes=5),
            'status': 'pending', 'priority': 'high'
        },
        {
            'id': '3', 'tableNumber': 5, 'originalItem': 'Fish and Chips',
            'modification': 'Substitute fries for sweet potato fries',
            'timestamp': datetime.now() - timedelta(minutes=8),
            'status': 'pending', 'priority': 'low'
        }
    ]

    housekeeping_notes = [
        {
            'id': '1', 'type': 'table-maintenance', 'title': 'Table 7 - Spill cleanup needed',
            'description': 'Large spill on table - needs immediate attention',
            'tableNumber': 7, 'status': 'pending', 'priority': 'urgent',
            'assignedTo': 'Housekeeping Team',
            'timestamp': datetime.now() - timedelta(minutes=15),
            'estimatedDuration': 10
        },
        {
            'id': '2', 'type': 'table-maintenance', 'title': 'Table 15 - Silverware missing',
            'description': 'Need 4 complete sets of silverware',
            'tableNumber': 15, 'status': 'pending', 'priority': 'high',
            'assignedTo': 'Housekeeping Team',
            'timestamp': datetime.now() - timedelta(minutes=20),
            'estimatedDuration': 5
        }
    ]

    whiteboard_notes = [
        {
            'id': '1', 'type': 'special', 'title': 'Special of the Day',
            'content': 'Pan-seared salmon with lemon butter sauce - $28',
            'priority': 'high',
            'timestamp': datetime.now() - timedelta(hours=1)
        },
        {
            'id': '2', 'type': '86-item', 'title': '86 Items',
            'content': 'Lobster bisque, Caesar salad, Chocolate cake',
            'priority': 'high',
            'timestamp': datetime.now() - timedelta(minutes=30)
        }
    ]

    return reservations, prep_items, order_adds, housekeeping_notes, whiteboard_notes

def get_priority_color(priority: str) -> str:
    """Get color class for priority level"""
    colors = {
        'urgent': 'urgent',
        'high': 'high',
        'medium': 'medium',
        'low': 'low'
    }
    return colors.get(priority, 'medium')

def get_status_color(status: str) -> str:
    """Get color for status"""
    colors = {
        'complete': '#00aa44',
        'in-progress': '#ffaa00',
        'pending': '#ff8800',
        'behind': '#ff4444',
        'confirmed': '#00aa44',
        'seated': '#0088cc',
        'completed': '#00aa44'
    }
    return colors.get(status, '#666666')

def display_reservations(reservations: List[Dict]):
    """Display reservations section"""
    st.subheader("📅 Reservations")

    for res in reservations:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.markdown(f"**{res['partyName']}** - {res['time']}")
                st.markdown(f"Table {res['tableNumber']} • {res['guestCount']} guests")
                if res['specialRequests']:
                    st.markdown(f"*Special requests: {', '.join(res['specialRequests'])}*")

            with col2:
                status_color = get_status_color(res['status'])
                st.markdown(f'<span style="color: {status_color}">{res["status"].title()}</span>',
                           unsafe_allow_html=True)

            with col3:
                if st.button(f"Update {res['id']}", key=f"res_{res['id']}"):
                    st.success(f"Updated {res['partyName']}")

def display_prep_items(prep_items: List[Dict]):
    """Display prep items section"""
    st.subheader("👨‍🍳 Prep Items")

    for item in prep_items:
        priority_class = get_priority_color(item['priority'])

        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.markdown(f"**{item['name']}** - {item['quantity']} {item['unit']}")
                if item.get('assignedTo'):
                    st.markdown(f"*Assigned to: {item['assignedTo']}*")
                if item.get('notes'):
                    st.markdown(f"*{item['notes']}*")

            with col2:
                status_color = get_status_color(item['status'])
                st.markdown(f'<span style="color: {status_color}">{item["status"].replace("-", " ").title()}</span>',
                           unsafe_allow_html=True)

            with col3:
                if st.button(f"Complete {item['id']}", key=f"prep_{item['id']}"):
                    st.success(f"Marked {item['name']} as complete")

def display_order_adds(order_adds: List[Dict]):
    """Display order modifications section"""
    st.subheader("🍽️ Order Modifications")

    for order in order_adds:
        priority_class = get_priority_color(order['priority'])

        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.markdown(f"**Table {order['tableNumber']}**")
                st.markdown(f"{order['originalItem']}")
                st.markdown(f"*{order['modification']}*")
                time_ago = datetime.now() - order['timestamp']
                st.markdown(f"*{int(time_ago.total_seconds() / 60)} minutes ago*")

            with col2:
                status_color = get_status_color(order['status'])
                st.markdown(f'<span style="color: {status_color}">{order["status"].title()}</span>',
                           unsafe_allow_html=True)

            with col3:
                if st.button(f"Accept {order['id']}", key=f"order_{order['id']}"):
                    st.success(f"Accepted modification for Table {order['tableNumber']}")

def display_housekeeping(housekeeping_notes: List[Dict]):
    """Display housekeeping section"""
    st.subheader("🧹 Housekeeping")

    for note in housekeeping_notes:
        priority_class = get_priority_color(note['priority'])

        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.markdown(f"**{note['title']}**")
                st.markdown(f"{note['description']}")
                if note.get('assignedTo'):
                    st.markdown(f"*Assigned to: {note['assignedTo']}*")
                if note.get('estimatedDuration'):
                    st.markdown(f"*Est. {note['estimatedDuration']} min*")

            with col2:
                status_color = get_status_color(note['status'])
                st.markdown(f'<span style="color: {status_color}">{note["status"].replace("-", " ").title()}</span>',
                           unsafe_allow_html=True)

            with col3:
                if st.button(f"Complete {note['id']}", key=f"house_{note['id']}"):
                    st.success(f"Completed {note['title']}")

def display_whiteboard(whiteboard_notes: List[Dict]):
    """Display whiteboard section"""
    st.subheader("📋 Whiteboard")

    for note in whiteboard_notes:
        priority_class = get_priority_color(note['priority'])

        with st.container():
            st.markdown(f"**{note['title']}**")
            st.markdown(f"{note['content']}")
            time_ago = datetime.now() - note['timestamp']
            st.markdown(f"*Posted {int(time_ago.total_seconds() / 3600)} hours ago*")

def display_metrics():
    """Display kitchen metrics"""
    st.subheader("📊 Kitchen Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Orders in Queue", random.randint(5, 20))

    with col2:
        st.metric("Prep Completion", f"{random.randint(70, 100)}%")

    with col3:
        st.metric("Avg Ticket Time", f"{random.randint(15, 25)} min")

    with col4:
        kitchen_status = random.choice(['Operational', 'Maintenance'])
        st.metric("Kitchen Status", kitchen_status)

def main():
    """Main application function"""

    # Header
    st.markdown('<h1 class="main-header">🍽️ Kitchen Command Center</h1>', unsafe_allow_html=True)

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    view_mode = st.sidebar.selectbox(
        "Select View",
        ["Display View", "Tablet View", "Metrics Dashboard"]
    )

    # Auto-refresh toggle
    auto_refresh = st.sidebar.checkbox("Auto-refresh (30s)", value=True)

    if auto_refresh:
        # Auto-refresh every 30 seconds
        time.sleep(30)
        st.rerun()

    # Load data
    reservations, prep_items, order_adds, housekeeping_notes, whiteboard_notes = get_sample_data()

    if view_mode == "Display View":
        # Display view - optimized for large screens
        st.markdown("### Kitchen Display - Real-time Status")

        col1, col2, col3 = st.columns(3)

        with col1:
            display_reservations(reservations)

        with col2:
            display_prep_items(prep_items)

        with col3:
            display_order_adds(order_adds)
            st.markdown("---")
            display_housekeeping(housekeeping_notes)

        # Kitchen metrics at bottom
        st.markdown("---")
        display_metrics()

    elif view_mode == "Tablet View":
        # Tablet view - touch-friendly interface
        st.markdown("### Tablet Management Interface")

        # Whiteboard section
        st.markdown("---")
        display_whiteboard(whiteboard_notes)

        # Management sections in tabs
        tab1, tab2, tab3, tab4 = st.tabs(["Reservations", "Prep", "Orders", "Housekeeping"])

        with tab1:
            display_reservations(reservations)

        with tab2:
            display_prep_items(prep_items)

        with tab3:
            display_order_adds(order_adds)

        with tab4:
            display_housekeeping(housekeeping_notes)

        # Quick actions
        st.markdown("---")
        st.subheader("Quick Actions")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Mark All Prep Complete", type="primary"):
                st.success("All prep items marked complete!")

        with col2:
            if st.button("Clear Completed Orders"):
                st.success("Completed orders cleared!")

        with col3:
            if st.button("Save Snapshot"):
                st.success("Kitchen snapshot saved!")

    elif view_mode == "Metrics Dashboard":
        # Metrics dashboard with charts
        st.markdown("### Kitchen Performance Dashboard")

        # Key metrics
        display_metrics()

        # Charts
        col1, col2 = st.columns(2)

        with col1:
            # Prep completion by category
            prep_df = pd.DataFrame(prep_items)
            if not prep_df.empty:
                category_counts = prep_df['category'].value_counts()
                fig = px.pie(values=category_counts.values, names=category_counts.index,
                           title="Prep Items by Category")
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Order status distribution
            order_df = pd.DataFrame(order_adds)
            if not order_df.empty:
                status_counts = order_df['status'].value_counts()
                fig = px.bar(x=status_counts.index, y=status_counts.values,
                           title="Order Status Distribution")
                st.plotly_chart(fig, use_container_width=True)

        # Timeline chart
        st.subheader("Order Timeline")
        timeline_data = []
        for order in order_adds:
            timeline_data.append({
                'Table': order['tableNumber'],
                'Time': order['timestamp'],
                'Item': order['originalItem'],
                'Status': order['status']
            })

        if timeline_data:
            timeline_df = pd.DataFrame(timeline_data)
            fig = px.scatter(timeline_df, x='Time', y='Table', color='Status',
                           title="Order Timeline")
            st.plotly_chart(fig, use_container_width=True)

    # Footer
    st.markdown("---")
    st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

if __name__ == "__main__":
    main()
