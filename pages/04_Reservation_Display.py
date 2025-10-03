"""
Kitchen Command Center - Reservation Display
Calendar view and list view with time slots for reservations
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import calendar

# Page configuration
st.set_page_config(
    page_title="Reservation Display",
    page_icon="📅",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .reservation-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        border-left: 4px solid #0ea5e9;
    }
    .reservation-confirmed {
        border-left-color: #10b981;
        background-color: #f0fdf4;
    }
    .reservation-pending {
        border-left-color: #f59e0b;
        background-color: #fffbeb;
    }
    .reservation-seated {
        border-left-color: #3b82f6;
        background-color: #eff6ff;
    }
    .reservation-completed {
        border-left-color: #6b7280;
        background-color: #f9fafb;
    }
    .time-slot {
        background-color: #f8fafc;
        padding: 0.5rem;
        border-radius: 0.25rem;
        border: 1px solid #e2e8f0;
        margin: 0.25rem 0;
        text-align: center;
    }
    .time-slot-occupied {
        background-color: #fef2f2;
        border-color: #fecaca;
    }
    .time-slot-available {
        background-color: #f0fdf4;
        border-color: #bbf7d0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'reservations' not in st.session_state:
    st.session_state.reservations = [
        {
            'id': 'RES-001', 'party_name': 'Smith Party', 'phone': '(555) 123-4567',
            'date': date.today(), 'time': '18:30', 'duration': 120,
            'table_number': 12, 'guest_count': 4, 'status': 'confirmed',
            'special_requests': ['Birthday celebration', 'High chair needed'],
            'notes': 'VIP customer'
        },
        {
            'id': 'RES-002', 'party_name': 'Johnson Family', 'phone': '(555) 234-5678',
            'date': date.today(), 'time': '19:15', 'duration': 90,
            'table_number': 8, 'guest_count': 6, 'status': 'pending',
            'special_requests': ['Vegetarian options'],
            'notes': ''
        },
        {
            'id': 'RES-003', 'party_name': 'Williams', 'phone': '(555) 345-6789',
            'date': date.today(), 'time': '20:00', 'duration': 120,
            'table_number': 5, 'guest_count': 2, 'status': 'seated',
            'special_requests': ['Anniversary dinner'],
            'notes': 'Window table preferred'
        },
        {
            'id': 'RES-004', 'party_name': 'Brown Group', 'phone': '(555) 456-7890',
            'date': date.today() + timedelta(days=1), 'time': '19:00', 'duration': 150,
            'table_number': 15, 'guest_count': 8, 'status': 'confirmed',
            'special_requests': ['Business dinner', 'Quiet table preferred'],
            'notes': 'Corporate account'
        },
        {
            'id': 'RES-005', 'party_name': 'Martinez Family', 'phone': '(555) 567-8901',
            'date': date.today() + timedelta(days=1), 'time': '18:00', 'duration': 120,
            'table_number': 3, 'guest_count': 5, 'status': 'confirmed',
            'special_requests': ['Wheelchair accessible'],
            'notes': ''
        }
    ]

def get_status_color(status):
    """Get color for reservation status"""
    colors = {
        'confirmed': '#10b981',
        'pending': '#f59e0b',
        'seated': '#3b82f6',
        'completed': '#6b7280',
        'cancelled': '#ef4444'
    }
    return colors.get(status, '#6b7280')

def display_reservation_overview(reservations):
    """Display reservation overview metrics"""
    st.subheader("📊 Reservation Overview")

    today_reservations = [r for r in reservations if r['date'] == date.today()]
    tomorrow_reservations = [r for r in reservations if r['date'] == date.today() + timedelta(days=1)]

    total_today = len(today_reservations)
    confirmed_today = len([r for r in today_reservations if r['status'] == 'confirmed'])
    seated_today = len([r for r in today_reservations if r['status'] == 'seated'])
    total_guests_today = sum(r['guest_count'] for r in today_reservations)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Today's Reservations", total_today)

    with col2:
        st.metric("Confirmed Today", confirmed_today)

    with col3:
        st.metric("Currently Seated", seated_today)

    with col4:
        st.metric("Total Guests Today", total_guests_today)

def display_calendar_view(reservations, selected_date):
    """Display calendar view of reservations"""
    st.subheader("📅 Calendar View")

    # Create calendar
    cal = calendar.monthcalendar(selected_date.year, selected_date.month)

    # Group reservations by date
    reservations_by_date = {}
    for res in reservations:
        res_date = res['date']
        if res_date.year == selected_date.year and res_date.month == selected_date.month:
            if res_date not in reservations_by_date:
                reservations_by_date[res_date] = []
            reservations_by_date[res_date].append(res)

    # Display calendar
    month_name = calendar.month_name[selected_date.month]
    st.markdown(f"### {month_name} {selected_date.year}")

    # Calendar header
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    cols = st.columns(7)
    for i, day in enumerate(days):
        with cols[i]:
            st.markdown(f"**{day}**")

    # Calendar body
    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day == 0:
                    st.write("")
                else:
                    current_date = date(selected_date.year, selected_date.month, day)
                    is_today = current_date == date.today()
                    is_selected = current_date == selected_date

                    # Style for today and selected date
                    style = ""
                    if is_today:
                        style = "background-color: #fef3c7; border: 2px solid #f59e0b;"
                    elif is_selected:
                        style = "background-color: #dbeafe; border: 2px solid #3b82f6;"

                    # Count reservations for this date
                    res_count = len(reservations_by_date.get(current_date, []))

                    if res_count > 0:
                        st.markdown(f"""
                        <div style="{style} padding: 0.5rem; border-radius: 0.25rem; text-align: center;">
                            <strong>{day}</strong><br>
                            <small>{res_count} reservation{'s' if res_count != 1 else ''}</small>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="{style} padding: 0.5rem; border-radius: 0.25rem; text-align: center;">
                            {day}
                        </div>
                        """, unsafe_allow_html=True)

def display_list_view(reservations, selected_date):
    """Display list view of reservations"""
    st.subheader("📋 List View")

    # Filter reservations for selected date
    day_reservations = [r for r in reservations if r['date'] == selected_date]

    if not day_reservations:
        st.info(f"No reservations for {selected_date.strftime('%B %d, %Y')}")
        return

    # Sort by time
    day_reservations.sort(key=lambda x: x['time'])

    # Display reservations
    for res in day_reservations:
        status_color = get_status_color(res['status'])
        status_class = f"reservation-{res['status']}"

        with st.container():
            col1, col2, col3, col4 = st.columns([2, 2, 1, 1])

            with col1:
                st.markdown(f"""
                <div class="reservation-card {status_class}">
                    <h4>{res['party_name']}</h4>
                    <p><strong>Time:</strong> {res['time']} ({res['duration']} min)</p>
                    <p><strong>Table:</strong> {res['table_number']} | <strong>Guests:</strong> {res['guest_count']}</p>
                    <p><strong>Phone:</strong> {res['phone']}</p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                if res['special_requests']:
                    st.markdown("**Special Requests:**")
                    for request in res['special_requests']:
                        st.markdown(f"• {request}")

                if res['notes']:
                    st.markdown(f"**Notes:** {res['notes']}")

            with col3:
                st.markdown(f'<span style="color: {status_color}">{res["status"].title()}</span>',
                           unsafe_allow_html=True)

            with col4:
                if res['status'] == 'confirmed':
                    if st.button(f"Seat {res['id']}", key=f"seat_{res['id']}"):
                        res['status'] = 'seated'
                        st.success(f"Seated {res['party_name']}")
                        st.rerun()
                elif res['status'] == 'seated':
                    if st.button(f"Complete {res['id']}", key=f"complete_{res['id']}"):
                        res['status'] = 'completed'
                        st.success(f"Completed {res['party_name']}")
                        st.rerun()

def display_time_slots(reservations, selected_date):
    """Display time slot availability"""
    st.subheader("⏰ Time Slot Availability")

    # Define time slots (every 30 minutes from 5 PM to 10 PM)
    time_slots = []
    start_time = datetime.combine(selected_date, datetime.min.time().replace(hour=17))
    end_time = datetime.combine(selected_date, datetime.min.time().replace(hour=22))

    current_time = start_time
    while current_time <= end_time:
        time_slots.append(current_time.time())
        current_time += timedelta(minutes=30)

    # Check availability for each time slot
    cols = st.columns(4)
    for i, time_slot in enumerate(time_slots):
        with cols[i % 4]:
            # Check if time slot is occupied
            occupied = any(
                res['date'] == selected_date and
                res['time'] == time_slot.strftime('%H:%M') and
                res['status'] in ['confirmed', 'seated']
                for res in reservations
            )

            slot_class = "time-slot-occupied" if occupied else "time-slot-available"
            slot_text = "Occupied" if occupied else "Available"

            st.markdown(f"""
            <div class="time-slot {slot_class}">
                <strong>{time_slot.strftime('%H:%M')}</strong><br>
                <small>{slot_text}</small>
            </div>
            """, unsafe_allow_html=True)

def display_reservation_form():
    """Display form to add new reservations"""
    st.subheader("➕ Add New Reservation")

    with st.form("add_reservation_form"):
        col1, col2 = st.columns(2)

        with col1:
            party_name = st.text_input("Party Name", placeholder="e.g., Smith Family")
            phone = st.text_input("Phone Number", placeholder="(555) 123-4567")
            guest_count = st.number_input("Guest Count", min_value=1, max_value=20, value=2)
            table_number = st.number_input("Table Number", min_value=1, max_value=30, value=1)

        with col2:
            res_date = st.date_input("Date", value=date.today())
            res_time = st.time_input("Time", value=datetime.min.time().replace(hour=19))
            duration = st.number_input("Duration (minutes)", min_value=30, max_value=300, value=120)
            status = st.selectbox("Status", ["confirmed", "pending"])

        special_requests = st.text_area("Special Requests", placeholder="Any special requests or notes...")
        notes = st.text_area("Internal Notes", placeholder="Internal notes for staff...")

        submitted = st.form_submit_button("Add Reservation", type="primary")

        if submitted:
            if party_name and phone:
                new_reservation = {
                    'id': f'RES-{len(st.session_state.reservations) + 1:03d}',
                    'party_name': party_name,
                    'phone': phone,
                    'date': res_date,
                    'time': res_time.strftime('%H:%M'),
                    'duration': duration,
                    'table_number': table_number,
                    'guest_count': guest_count,
                    'status': status,
                    'special_requests': [req.strip() for req in special_requests.split('\n') if req.strip()],
                    'notes': notes
                }

                st.session_state.reservations.append(new_reservation)
                st.success("Reservation added successfully!")
                st.rerun()
            else:
                st.error("Please fill in party name and phone number")

def main():
    """Main reservation display function"""

    st.title("📅 Reservation Display")
    st.markdown("Calendar view and list view with time slots for reservations")

    # Date selector
    col1, col2 = st.columns([1, 3])

    with col1:
        selected_date = st.date_input("Select Date", value=date.today())

    with col2:
        view_mode = st.selectbox("View Mode", ["List View", "Calendar View", "Time Slots"])

    # Load data
    reservations = st.session_state.reservations

    # Display overview
    display_reservation_overview(reservations)

    st.markdown("---")

    # Display based on view mode
    if view_mode == "Calendar View":
        display_calendar_view(reservations, selected_date)
    elif view_mode == "Time Slots":
        display_time_slots(reservations, selected_date)
    else:  # List View
        display_list_view(reservations, selected_date)

    st.markdown("---")

    # Add new reservation form
    display_reservation_form()

    # Footer
    st.markdown("---")
    st.markdown(f"*Selected Date: {selected_date.strftime('%B %d, %Y')} | Last updated: {datetime.now().strftime('%H:%M:%S')}*")

if __name__ == "__main__":
    main()
