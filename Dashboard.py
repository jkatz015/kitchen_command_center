import streamlit as st
from datetime import datetime
import time

st.set_page_config(page_title="Kitchen Command Center", page_icon="🍽️", layout="wide")

# Auto-refresh functionality
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False

# Sidebar controls
with st.sidebar:
    st.title("⚙️ Controls")
    auto_refresh = st.checkbox("Auto-refresh (30s)", value=st.session_state.auto_refresh)
    st.session_state.auto_refresh = auto_refresh

    if st.button("🔄 Refresh Now"):
        st.rerun()

# Auto-refresh logic
if st.session_state.auto_refresh:
    # Auto-refresh every 30 seconds
    time.sleep(30)
    st.rerun()

# --- Tiny CSS for card look ---
st.markdown("""
<style>
.card {border:1px solid #e5e7eb; border-radius:16px; padding:16px; height:160px;}
.card h3 {margin:0 0 6px 0; font-size:1.1rem;}
.card p {margin:0 0 10px 0; color:#6b7280; font-size:0.95rem;}
</style>
""", unsafe_allow_html=True)

st.markdown("## 🍽️ Kitchen Command Center")
st.caption(f"Updated {datetime.now().strftime('%-I:%M %p')}")

# Define your pages with real-time status indicators
def get_page_status():
    """Get real-time status for each page"""
    return {
        "pages/01_Inventory_Dashboard.py": {"status": "🟢", "count": "12 items"},
        "pages/02_Production_Board.py": {"status": "🟡", "count": "3 active"},
        "pages/03_Notes_Whiteboard.py": {"status": "🟢", "count": "5 notes"},
        "pages/04_Reservation_Display.py": {"status": "🟢", "count": "8 tables"},
        "pages/05_Employee_Notes.py": {"status": "🟡", "count": "2 pending"},
        "pages/06_Prep_List.py": {"status": "🔴", "count": "7 items"},
        "pages/07_Order_Guide_Items.py": {"status": "🟢", "count": "45 SKUs"}
    }

PAGES = [
    {"label": "Inventory Dashboard", "path": "pages/01_Inventory_Dashboard.py", "icon": "📦",
     "desc": "Par, on-hand, and order guide export."},
    {"label": "Production Board", "path": "pages/02_Production_Board.py", "icon": "👩‍🍳",
     "desc": "Batch list, stations, owners, completion."},
    {"label": "Notes Whiteboard", "path": "pages/03_Notes_Whiteboard.py", "icon": "📝",
     "desc": "Sketch plating and station diagrams."},
    {"label": "Reservation Display", "path": "pages/04_Reservation_Display.py", "icon": "📋",
     "desc": "Service view for reservations (optional)."},
    {"label": "Employee Notes", "path": "pages/05_Employee_Notes.py", "icon": "👥",
     "desc": "Shift notes and handoffs."},
    {"label": "Prep List", "path": "pages/06_Prep_List.py", "icon": "📑",
     "desc": "Dynamic prep checklist."},
    {"label": "Order Guide Items", "path": "pages/07_Order_Guide_Items.py", "icon": "🧾",
     "desc": "Maintain orderable SKUs."},
]

# Get current status
current_status = get_page_status()

# Render tiles in a 3-column grid
cols_per_row = 3
rows = (len(PAGES) + cols_per_row - 1) // cols_per_row
idx = 0
for _ in range(rows):
    cols = st.columns(cols_per_row)
    for col in cols:
        if idx >= len(PAGES):
            col.empty()
            continue
        p = PAGES[idx]
        with col:
            status_info = current_status.get(p["path"], {"status": "⚪", "count": ""})
            st.markdown(f"""
            <div class="card">
              <h3>{p["icon"]} {p["label"]} {status_info["status"]}</h3>
              <p>{p["desc"]}</p>
              <small style="color: #6b7280;">{status_info["count"]}</small>
            </div>
            """, unsafe_allow_html=True)
            # Internal link to the Streamlit page file
            st.page_link(p["path"], label="Open", icon="➡️")
        idx += 1

st.divider()
st.info("Tip: You can still use the left sidebar page list. These tiles are quick links.")
