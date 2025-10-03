"""
Kitchen Command Center - Order Guide Items
Running list that can be compiled into orders for kitchen operations
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta

# Page configuration
st.set_page_config(
    page_title="Order Guide Items",
    page_icon="📦",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .order-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        border-left: 4px solid #0ea5e9;
    }
    .order-urgent {
        border-left-color: #ef4444;
        background-color: #fef2f2;
    }
    .order-high {
        border-left-color: #f59e0b;
        background-color: #fffbeb;
    }
    .order-medium {
        border-left-color: #3b82f6;
        background-color: #eff6ff;
    }
    .order-low {
        border-left-color: #10b981;
        background-color: #f0fdf4;
    }
    .order-completed {
        border-left-color: #6b7280;
        background-color: #f9fafb;
        opacity: 0.7;
    }
    .supplier-card {
        background-color: #f8fafc;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px solid #e2e8f0;
        text-align: center;
    }
    .supplier-selected {
        border-color: #0ea5e9;
        background-color: #eff6ff;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'order_items' not in st.session_state:
    st.session_state.order_items = [
        {
            'id': 'ORD-001', 'item_name': 'Chicken Breast', 'category': 'Protein',
            'quantity': 50, 'unit': 'lbs', 'supplier': 'Fresh Farms',
            'priority': 'high', 'status': 'pending', 'notes': 'For weekend rush',
            'created_date': date.today(), 'needed_date': date.today() + timedelta(days=1),
            'estimated_cost': 225.00
        },
        {
            'id': 'ORD-002', 'item_name': 'Salmon Fillet', 'category': 'Protein',
            'quantity': 20, 'unit': 'lbs', 'supplier': 'Ocean Fresh',
            'priority': 'medium', 'status': 'pending', 'notes': 'Special order',
            'created_date': date.today(), 'needed_date': date.today() + timedelta(days=2),
            'estimated_cost': 240.00
        },
        {
            'id': 'ORD-003', 'item_name': 'Organic Onions', 'category': 'Vegetables',
            'quantity': 25, 'unit': 'lbs', 'supplier': 'Local Farm',
            'priority': 'low', 'status': 'pending', 'notes': 'Weekly order',
            'created_date': date.today(), 'needed_date': date.today() + timedelta(days=3),
            'estimated_cost': 30.00
        },
        {
            'id': 'ORD-004', 'item_name': 'Olive Oil', 'category': 'Pantry',
            'quantity': 5, 'unit': 'gallons', 'supplier': 'Mediterranean Imports',
            'priority': 'urgent', 'status': 'pending', 'notes': 'Running low',
            'created_date': date.today(), 'needed_date': date.today(),
            'estimated_cost': 75.00
        },
        {
            'id': 'ORD-005', 'item_name': 'Flour', 'category': 'Pantry',
            'quantity': 20, 'unit': 'lbs', 'supplier': 'Baker Supply',
            'priority': 'medium', 'status': 'pending', 'notes': 'Bread making',
            'created_date': date.today(), 'needed_date': date.today() + timedelta(days=1),
            'estimated_cost': 56.00
        },
        {
            'id': 'ORD-006', 'item_name': 'Tomatoes', 'category': 'Vegetables',
            'quantity': 30, 'unit': 'lbs', 'supplier': 'Garden Fresh',
            'priority': 'high', 'status': 'pending', 'notes': 'Sauce preparation',
            'created_date': date.today(), 'needed_date': date.today() + timedelta(days=1),
            'estimated_cost': 75.00
        }
    ]

if 'suppliers' not in st.session_state:
    st.session_state.suppliers = [
        {'name': 'Fresh Farms', 'contact': '(555) 100-2000', 'delivery_days': 'Mon, Wed, Fri'},
        {'name': 'Ocean Fresh', 'contact': '(555) 200-3000', 'delivery_days': 'Tue, Thu'},
        {'name': 'Local Farm', 'contact': '(555) 300-4000', 'delivery_days': 'Mon, Wed, Fri'},
        {'name': 'Mediterranean Imports', 'contact': '(555) 400-5000', 'delivery_days': 'Daily'},
        {'name': 'Baker Supply', 'contact': '(555) 500-6000', 'delivery_days': 'Mon, Thu'},
        {'name': 'Garden Fresh', 'contact': '(555) 600-7000', 'delivery_days': 'Tue, Fri'}
    ]

def get_priority_color(priority):
    """Get color for order priority"""
    colors = {
        'urgent': '#ef4444',
        'high': '#f59e0b',
        'medium': '#3b82f6',
        'low': '#10b981'
    }
    return colors.get(priority, '#6b7280')

def display_order_overview(order_items):
    """Display order overview metrics"""
    st.subheader("📊 Order Overview")

    total_items = len(order_items)
    pending_items = len([item for item in order_items if item['status'] == 'pending'])
    urgent_items = len([item for item in order_items if item['priority'] == 'urgent'])
    total_cost = sum(item['estimated_cost'] for item in order_items if item['status'] == 'pending')

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Items", total_items)

    with col2:
        st.metric("Pending Orders", pending_items)

    with col3:
        st.metric("Urgent Items", urgent_items, delta="Action needed" if urgent_items > 0 else None)

    with col4:
        st.metric("Total Cost", f"${total_cost:,.2f}")

def display_order_list(order_items, filter_supplier=None, filter_priority=None):
    """Display order items list"""
    st.subheader("📋 Order Items")

    # Apply filters
    filtered_items = order_items
    if filter_supplier and filter_supplier != "All":
        filtered_items = [item for item in filtered_items if item['supplier'] == filter_supplier]
    if filter_priority and filter_priority != "All":
        filtered_items = [item for item in filtered_items if item['priority'] == filter_priority]

    if not filtered_items:
        st.info("No items match the current filters.")
        return

    # Sort by priority and needed date
    priority_order = {'urgent': 0, 'high': 1, 'medium': 2, 'low': 3}
    filtered_items.sort(key=lambda x: (priority_order.get(x['priority'], 4), x['needed_date']))

    for item in filtered_items:
        priority_color = get_priority_color(item['priority'])
        priority_class = f"order-{item['priority']}"

        if item['status'] == 'completed':
            priority_class += " order-completed"

        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 2, 1, 1, 1])

            with col1:
                st.markdown(f"""
                <div class="order-card {priority_class}">
                    <h4>{item['item_name']}</h4>
                    <p><strong>Category:</strong> {item['category']}</p>
                    <p><strong>Quantity:</strong> {item['quantity']} {item['unit']}</p>
                    <p><strong>Supplier:</strong> {item['supplier']}</p>
                    {f"<p><strong>Notes:</strong> {item['notes']}</p>" if item['notes'] else ""}
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"**Needed Date:** {item['needed_date']}")
                st.markdown(f"**Created:** {item['created_date']}")
                st.markdown(f"**Estimated Cost:** ${item['estimated_cost']:.2f}")

                # Show overdue warning
                if item['needed_date'] < date.today() and item['status'] == 'pending':
                    st.error("⚠️ Overdue!")

            with col3:
                st.markdown(f'<span style="color: {priority_color}">{item["priority"].title()}</span>',
                           unsafe_allow_html=True)

            with col4:
                status_color = {
                    'pending': '#f59e0b',
                    'ordered': '#3b82f6',
                    'received': '#10b981',
                    'completed': '#6b7280'
                }.get(item['status'], '#6b7280')

                st.markdown(f'<span style="color: {status_color}">{item["status"].title()}</span>',
                           unsafe_allow_html=True)

            with col5:
                if item['status'] == 'pending':
                    if st.button(f"Order {item['id']}", key=f"order_{item['id']}"):
                        item['status'] = 'ordered'
                        st.success(f"Ordered {item['item_name']}")
                        st.rerun()
                elif item['status'] == 'ordered':
                    if st.button(f"Receive {item['id']}", key=f"receive_{item['id']}"):
                        item['status'] = 'received'
                        st.success(f"Received {item['item_name']}")
                        st.rerun()
                elif item['status'] == 'received':
                    if st.button(f"Complete {item['id']}", key=f"complete_{item['id']}"):
                        item['status'] = 'completed'
                        st.success(f"Completed {item['item_name']}")
                        st.rerun()
                elif item['status'] == 'completed':
                    st.success("✅ Done")

def display_order_filters(order_items):
    """Display order filters"""
    st.subheader("🔍 Filters")

    col1, col2, col3 = st.columns(3)

    with col1:
        supplier_options = ["All"] + list(set(item['supplier'] for item in order_items))
        filter_supplier = st.selectbox("Filter by Supplier", supplier_options)

    with col2:
        priority_options = ["All"] + list(set(item['priority'] for item in order_items))
        filter_priority = st.selectbox("Filter by Priority", priority_options)

    with col3:
        status_options = ["All"] + list(set(item['status'] for item in order_items))
        filter_status = st.selectbox("Filter by Status", status_options)

    return filter_supplier, filter_priority, filter_status

def display_supplier_orders(order_items):
    """Display orders grouped by supplier"""
    st.subheader("🏢 Orders by Supplier")

    # Group items by supplier
    supplier_orders = {}
    for item in order_items:
        if item['status'] == 'pending':
            supplier = item['supplier']
            if supplier not in supplier_orders:
                supplier_orders[supplier] = []
            supplier_orders[supplier].append(item)

    if not supplier_orders:
        st.info("No pending orders to group by supplier.")
        return

    # Display each supplier's orders
    for supplier, items in supplier_orders.items():
        total_cost = sum(item['estimated_cost'] for item in items)

        with st.expander(f"{supplier} - {len(items)} items - ${total_cost:.2f}"):
            for item in items:
                col1, col2, col3 = st.columns([3, 1, 1])

                with col1:
                    st.write(f"**{item['item_name']}** - {item['quantity']} {item['unit']}")
                    if item['notes']:
                        st.write(f"*{item['notes']}*")

                with col2:
                    st.write(f"${item['estimated_cost']:.2f}")

                with col3:
                    if st.button(f"Order {item['id']}", key=f"supplier_order_{item['id']}"):
                        item['status'] = 'ordered'
                        st.success(f"Ordered {item['item_name']}")
                        st.rerun()

def display_supplier_info(suppliers):
    """Display supplier information"""
    st.subheader("📞 Supplier Information")

    cols = st.columns(len(suppliers))

    for i, supplier in enumerate(suppliers):
        with cols[i]:
            st.markdown(f"""
            <div class="supplier-card">
                <h4>{supplier['name']}</h4>
                <p><strong>Contact:</strong> {supplier['contact']}</p>
                <p><strong>Delivery Days:</strong> {supplier['delivery_days']}</p>
            </div>
            """, unsafe_allow_html=True)

def display_order_form():
    """Display form to add new order items"""
    st.subheader("➕ Add New Order Item")

    with st.form("add_order_form"):
        col1, col2 = st.columns(2)

        with col1:
            item_name = st.text_input("Item Name", placeholder="e.g., Chicken Breast")
            category = st.selectbox("Category", ["Protein", "Vegetables", "Pantry", "Dairy", "Beverages", "Other"])
            quantity = st.number_input("Quantity", min_value=1, value=1)
            unit = st.text_input("Unit", placeholder="e.g., lbs, gallons, pieces")

        with col2:
            supplier = st.selectbox("Supplier", [s['name'] for s in st.session_state.suppliers])
            priority = st.selectbox("Priority", ["low", "medium", "high", "urgent"])
            needed_date = st.date_input("Needed Date", value=date.today() + timedelta(days=1))
            estimated_cost = st.number_input("Estimated Cost", min_value=0.0, value=0.0, step=0.01)

        notes = st.text_area("Notes", placeholder="Any special instructions or notes...")

        submitted = st.form_submit_button("Add Order Item", type="primary")

        if submitted:
            if item_name and unit:
                new_order_item = {
                    'id': f'ORD-{len(st.session_state.order_items) + 1:03d}',
                    'item_name': item_name,
                    'category': category,
                    'quantity': quantity,
                    'unit': unit,
                    'supplier': supplier,
                    'priority': priority,
                    'status': 'pending',
                    'notes': notes,
                    'created_date': date.today(),
                    'needed_date': needed_date,
                    'estimated_cost': estimated_cost
                }

                st.session_state.order_items.append(new_order_item)
                st.success("Order item added successfully!")
                st.rerun()
            else:
                st.error("Please fill in item name and unit")

def display_order_analytics(order_items):
    """Display order analytics"""
    st.subheader("📊 Order Analytics")

    col1, col2 = st.columns(2)

    with col1:
        # Orders by status
        status_counts = pd.Series([item['status'] for item in order_items]).value_counts()
        st.bar_chart(status_counts)
        st.caption("Items by Status")

    with col2:
        # Orders by priority
        priority_counts = pd.Series([item['priority'] for item in order_items]).value_counts()
        st.bar_chart(priority_counts)
        st.caption("Items by Priority")

    # Cost analysis by category
    st.subheader("💰 Cost Analysis by Category")
    category_costs = {}

    for item in order_items:
        if item['status'] == 'pending':
            category = item['category']
            if category not in category_costs:
                category_costs[category] = 0
            category_costs[category] += item['estimated_cost']

    if category_costs:
        cost_data = []
        for category, cost in category_costs.items():
            cost_data.append({
                'Category': category,
                'Total Cost': cost
            })

        cost_df = pd.DataFrame(cost_data)
        st.bar_chart(cost_df.set_index('Category'))
        st.caption("Pending Order Costs by Category")

def main():
    """Main order guide items function"""

    st.title("📦 Order Guide Items")
    st.markdown("Running list that can be compiled into orders for kitchen operations")

    # Load data
    order_items = st.session_state.order_items
    suppliers = st.session_state.suppliers

    # Display overview
    display_order_overview(order_items)

    st.markdown("---")

    # Display filters
    filter_supplier, filter_priority, filter_status = display_order_filters(order_items)

    st.markdown("---")

    # Display order list
    display_order_list(order_items, filter_supplier, filter_priority)

    st.markdown("---")

    # Display supplier orders
    display_supplier_orders(order_items)

    st.markdown("---")

    # Display supplier information
    display_supplier_info(suppliers)

    st.markdown("---")

    # Display analytics
    display_order_analytics(order_items)

    st.markdown("---")

    # Add new order item form
    display_order_form()

    # Footer
    st.markdown("---")
    st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

if __name__ == "__main__":
    main()
