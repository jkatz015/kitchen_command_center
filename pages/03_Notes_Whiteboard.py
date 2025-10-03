"""
Kitchen Command Center - Notes & Whiteboard
Interactive whiteboard for kitchen notes and diagrams
"""

import streamlit as st
from streamlit_drawable_canvas import st_canvas
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Notes & Whiteboard",
    page_icon="📝",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .note-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        border-left: 4px solid #0ea5e9;
    }
    .urgent-note {
        border-left-color: #ef4444;
        background-color: #fef2f2;
    }
    .high-note {
        border-left-color: #f59e0b;
        background-color: #fffbeb;
    }
    .medium-note {
        border-left-color: #3b82f6;
        background-color: #eff6ff;
    }
    .low-note {
        border-left-color: #10b981;
        background-color: #f0fdf4;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'notes' not in st.session_state:
    st.session_state.notes = []
if 'canvas_data' not in st.session_state:
    st.session_state.canvas_data = None

def add_note(title, content, priority, author):
    """Add a new note to session state"""
    note = {
        'id': len(st.session_state.notes) + 1,
        'title': title,
        'content': content,
        'priority': priority,
        'author': author,
        'timestamp': datetime.now(),
        'category': 'general'
    }
    st.session_state.notes.append(note)

def display_notes():
    """Display existing notes"""
    st.subheader("📋 Kitchen Notes")

    if not st.session_state.notes:
        st.info("No notes yet. Add one below!")
        return

    # Sort notes by priority and timestamp
    priority_order = {'urgent': 0, 'high': 1, 'medium': 2, 'low': 3}
    sorted_notes = sorted(st.session_state.notes,
                         key=lambda x: (priority_order.get(x['priority'], 4), x['timestamp']),
                         reverse=True)

    for note in sorted_notes:
        priority_class = f"{note['priority']}-note"

        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.markdown(f"""
                <div class="note-card {priority_class}">
                    <h4>{note['title']}</h4>
                    <p>{note['content']}</p>
                    <small>By: {note['author']} | {note['timestamp'].strftime('%Y-%m-%d %H:%M')}</small>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"**Priority:** {note['priority'].title()}")

            with col3:
                if st.button(f"Delete {note['id']}", key=f"delete_{note['id']}"):
                    st.session_state.notes = [n for n in st.session_state.notes if n['id'] != note['id']]
                    st.rerun()

def add_note_form():
    """Form to add new notes"""
    st.subheader("➕ Add New Note")

    with st.form("add_note_form"):
        col1, col2 = st.columns(2)

        with col1:
            title = st.text_input("Note Title", placeholder="e.g., Special Prep for VIP Table")
            content = st.text_area("Note Content", placeholder="Details about the note...")

        with col2:
            priority = st.selectbox("Priority", ["low", "medium", "high", "urgent"])
            author = st.text_input("Author", placeholder="Your name")

        submitted = st.form_submit_button("Add Note", type="primary")

        if submitted:
            if title and content and author:
                add_note(title, content, priority, author)
                st.success("Note added successfully!")
                st.rerun()
            else:
                st.error("Please fill in all fields")

def display_whiteboard():
    """Display the interactive whiteboard"""
    st.subheader("🎨 Interactive Whiteboard")
    st.caption("Quick sketch pad for station diagrams, plating notes, etc.")

    # Canvas for drawing
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.2)",
        stroke_width=3,
        stroke_color="#111827",
        background_color="#fff",
        height=450,
        width=900,
        drawing_mode="freedraw",
        key="canvas",
    )

    # Save canvas data
    if canvas_result.json_data is not None:
        st.session_state.canvas_data = canvas_result.json_data

    # Canvas controls
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Clear Canvas", type="secondary"):
            st.session_state.canvas_data = None
            st.rerun()

    with col2:
        if st.button("Save Drawing", type="primary"):
            if st.session_state.canvas_data:
                # In a real app, you'd save this to a database
                st.success("Drawing saved to session!")
            else:
                st.warning("No drawing to save")

    with col3:
        if st.button("Load Template", type="secondary"):
            st.info("Template loading feature - implement as needed")

def display_quick_notes():
    """Display quick note templates"""
    st.subheader("⚡ Quick Notes")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("86 Items", type="secondary"):
            add_note("86 Items", "Items that are out of stock", "urgent", "Kitchen")
            st.rerun()

    with col2:
        if st.button("Special Prep", type="secondary"):
            add_note("Special Prep", "Special preparation needed", "high", "Kitchen")
            st.rerun()

    with col3:
        if st.button("Station Notes", type="secondary"):
            add_note("Station Notes", "Notes for specific station", "medium", "Kitchen")
            st.rerun()

def display_kitchen_announcements():
    """Display kitchen announcements"""
    st.subheader("📢 Kitchen Announcements")

    announcements = [
        {
            'title': 'VIP Table Alert',
            'content': 'Food critic expected around 8 PM - Table 12',
            'priority': 'high',
            'timestamp': datetime.now() - timedelta(hours=2)
        },
        {
            'title': 'Dishwasher Maintenance',
            'content': 'Dishwasher maintenance at 3 PM - Use backup machine',
            'priority': 'medium',
            'timestamp': datetime.now() - timedelta(hours=4)
        },
        {
            'title': 'Today\'s Special',
            'content': 'Pan-seared salmon with lemon butter sauce - $28',
            'priority': 'low',
            'timestamp': datetime.now() - timedelta(hours=6)
        }
    ]

    for announcement in announcements:
        priority_class = f"{announcement['priority']}-note"

        st.markdown(f"""
        <div class="note-card {priority_class}">
            <h4>{announcement['title']}</h4>
            <p>{announcement['content']}</p>
            <small>{announcement['timestamp'].strftime('%Y-%m-%d %H:%M')}</small>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main notes and whiteboard function"""

    st.title("📝 Notes & Whiteboard")
    st.markdown("Interactive whiteboard for kitchen notes and diagrams")

    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["Whiteboard", "Notes", "Quick Notes", "Announcements"])

    with tab1:
        display_whiteboard()

    with tab2:
        display_notes()
        st.markdown("---")
        add_note_form()

    with tab3:
        display_quick_notes()

    with tab4:
        display_kitchen_announcements()

    # Footer
    st.markdown("---")
    st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

if __name__ == "__main__":
    main()
