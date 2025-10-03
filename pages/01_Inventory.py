"""
Kitchen Command Center - Inventory Dashboard
Real-time inventory tracking and management
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="Kitchen Command Center Dashboard",
    page_icon="📦",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        border-left: 4px solid #0ea5e9;
    }
    .low-stock {
        border-left-color: #ef4444;
        background-color: #fef2f2;
    }
    .critical-stock {
        border-left-color: #dc2626;
        background-color: #fee2e2;
    }
    .good-stock {
        border-left-color: #10b981;
        background-color: #f0fdf4;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def get_inventory_data():
    """Load inventory data"""

    inventory_items = [
        {
            'id': '1', 'name': 'Chicken Breast', 'category': 'Protein',
            'current_stock': 45, 'min_stock': 20, 'max_stock': 100,
            'unit': 'lbs', 'last_updated': datetime.now() - timedelta(hours=2),
            'supplier': 'Fresh Farms', 'cost_per_unit': 4.50
        },
        {
            'id': '2', 'name': 'Salmon Fillet', 'category': 'Protein',
            'current_stock': 12, 'min_stock': 15, 'max_stock': 50,
            'unit': 'lbs', 'last_updated': datetime.now() - timedelta(hours=1),
            'supplier': 'Ocean Fresh', 'cost_per_unit': 12.00
        },
        {
            'id': '3', 'name': 'Onions', 'category': 'Vegetables',
            'current_stock': 25, 'min_stock': 10, 'max_stock': 60,
            'unit': 'lbs', 'last_updated': datetime.now() - timedelta(minutes=30),
            'supplier': 'Local Farm', 'cost_per_unit': 1.20
        },
        {
            'id': '4', 'name': 'Garlic', 'category': 'Vegetables',
            'current_stock': 8, 'min_stock': 5, 'max_stock': 20,
            'unit': 'lbs', 'last_updated': datetime.now() - timedelta(hours=3),
            'supplier': 'Local Farm', 'cost_per_unit': 3.50
        },
        {
            'id': '5', 'name': 'Olive Oil', 'category': 'Pantry',
            'current_stock': 3, 'min_stock': 5, 'max_stock': 15,
            'unit': 'gallons', 'last_updated': datetime.now() - timedelta(hours=4),
            'supplier': 'Mediterranean Imports', 'cost_per_unit': 15.00
        },
        {
            'id': '6', 'name': 'Flour', 'category': 'Pantry',
            'current_stock': 18, 'min_stock': 10, 'max_stock': 40,
            'unit': 'lbs', 'last_updated': datetime.now() - timedelta(hours=6),
            'supplier': 'Baker Supply', 'cost_per_unit': 2.80
        },
        {
            'id': '7', 'name': 'Tomatoes', 'category': 'Vegetables',
            'current_stock': 35, 'min_stock': 15, 'max_stock': 50,
            'unit': 'lbs', 'last_updated': datetime.now() - timedelta(minutes=45),
            'supplier': 'Garden Fresh', 'cost_per_unit': 2.50
        },
        {
            'id': '8', 'name': 'Pasta', 'category': 'Pantry',
            'current_stock': 22, 'min_stock': 10, 'max_stock': 30,
            'unit': 'lbs', 'last_updated': datetime.now() - timedelta(hours=5),
            'supplier': 'Italian Imports', 'cost_per_unit': 3.20
        }
    ]

    return inventory_items

def get_stock_status(current, minimum):
    """Determine stock status"""
    if current <= minimum:
        return "critical"
    elif current <= minimum * 1.5:
        return "low"
    else:
        return "good"

def display_inventory_overview(inventory_items):
    """Display inventory overview metrics"""
    st.subheader("📊 Inventory Overview")

    total_items = len(inventory_items)
    low_stock_items = sum(1 for item in inventory_items if get_stock_status(item['current_stock'], item['min_stock']) == "low")
    critical_stock_items = sum(1 for item in inventory_items if get_stock_status(item['current_stock'], item['min_stock']) == "critical")
    total_value = sum(item['current_stock'] * item['cost_per_unit'] for item in inventory_items)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Items", total_items)

    with col2:
        st.metric("Low Stock Items", low_stock_items, delta=f"-{critical_stock_items} critical" if critical_stock_items > 0 else None)

    with col3:
        st.metric("Critical Stock", critical_stock_items, delta="Action needed" if critical_stock_items > 0 else None)

    with col4:
        st.metric("Total Inventory Value", f"${total_value:,.2f}")

def display_stock_alerts(inventory_items):
    """Display stock alerts"""
    st.subheader("🚨 Stock Alerts")

    critical_items = [item for item in inventory_items if get_stock_status(item['current_stock'], item['min_stock']) == "critical"]
    low_items = [item for item in inventory_items if get_stock_status(item['current_stock'], item['min_stock']) == "low"]

    if critical_items:
        st.error("**Critical Stock Items - Immediate Action Required:**")
        for item in critical_items:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{item['name']}** - {item['current_stock']} {item['unit']} remaining")
            with col2:
                st.write(f"Min: {item['min_stock']} {item['unit']}")
            with col3:
                if st.button(f"Order {item['id']}", key=f"critical_{item['id']}"):
                    st.success(f"Order placed for {item['name']}")

    if low_items:
        st.warning("**Low Stock Items - Consider Ordering:**")
        for item in low_items:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{item['name']}** - {item['current_stock']} {item['unit']} remaining")
            with col2:
                st.write(f"Min: {item['min_stock']} {item['unit']}")
            with col3:
                if st.button(f"Order {item['id']}", key=f"low_{item['id']}"):
                    st.success(f"Order placed for {item['name']}")

def display_inventory_table(inventory_items):
    """Display detailed inventory table"""
    st.subheader("📋 Detailed Inventory")

    # Create DataFrame
    df = pd.DataFrame(inventory_items)

    # Add stock status column
    df['stock_status'] = df.apply(lambda row: get_stock_status(row['current_stock'], row['min_stock']), axis=1)
    df['stock_percentage'] = (df['current_stock'] / df['max_stock'] * 100).round(1)
    df['total_value'] = (df['current_stock'] * df['cost_per_unit']).round(2)

    # Format columns
    df['last_updated'] = df['last_updated'].dt.strftime('%Y-%m-%d %H:%M')
    df['cost_per_unit'] = df['cost_per_unit'].apply(lambda x: f"${x:.2f}")
    df['total_value'] = df['total_value'].apply(lambda x: f"${x:.2f}")

    # Display table
    st.dataframe(
        df[['name', 'category', 'current_stock', 'unit', 'min_stock', 'max_stock',
            'stock_status', 'stock_percentage', 'supplier', 'cost_per_unit', 'total_value', 'last_updated']],
        use_container_width=True,
        column_config={
            "name": "Item Name",
            "category": "Category",
            "current_stock": "Current Stock",
            "unit": "Unit",
            "min_stock": "Min Stock",
            "max_stock": "Max Stock",
            "stock_status": "Status",
            "stock_percentage": "Stock %",
            "supplier": "Supplier",
            "cost_per_unit": "Cost/Unit",
            "total_value": "Total Value",
            "last_updated": "Last Updated"
        }
    )

def display_category_analysis(inventory_items):
    """Display category analysis charts"""
    st.subheader("📈 Category Analysis")

    df = pd.DataFrame(inventory_items)

    col1, col2 = st.columns(2)

    with col1:
        # Stock by category
        category_stock = df.groupby('category')['current_stock'].sum().reset_index()
        fig = px.pie(category_stock, values='current_stock', names='category',
                    title="Stock Distribution by Category")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Value by category
        df['total_value'] = df['current_stock'] * df['cost_per_unit']
        category_value = df.groupby('category')['total_value'].sum().reset_index()
        fig = px.bar(category_value, x='category', y='total_value',
                    title="Inventory Value by Category")
        fig.update_layout(yaxis_title="Value ($)")
        st.plotly_chart(fig, use_container_width=True)

def display_reorder_suggestions(inventory_items):
    """Display reorder suggestions"""
    st.subheader("🛒 Reorder Suggestions")

    suggestions = []
    for item in inventory_items:
        if item['current_stock'] <= item['min_stock'] * 1.2:  # 20% above minimum
            reorder_qty = item['max_stock'] - item['current_stock']
            total_cost = reorder_qty * item['cost_per_unit']
            suggestions.append({
                'item': item['name'],
                'current_stock': item['current_stock'],
                'reorder_qty': reorder_qty,
                'unit': item['unit'],
                'supplier': item['supplier'],
                'total_cost': total_cost,
                'urgency': 'Critical' if item['current_stock'] <= item['min_stock'] else 'Low Stock'
            })

    if suggestions:
        suggestions_df = pd.DataFrame(suggestions)
        suggestions_df['total_cost'] = suggestions_df['total_cost'].apply(lambda x: f"${x:.2f}")

        st.dataframe(
            suggestions_df,
            use_container_width=True,
            column_config={
                "item": "Item",
                "current_stock": "Current Stock",
                "reorder_qty": "Reorder Qty",
                "unit": "Unit",
                "supplier": "Supplier",
                "total_cost": "Total Cost",
                "urgency": "Urgency"
            }
        )

        total_reorder_cost = sum(s['total_cost'] for s in suggestions)
        st.info(f"**Total Reorder Cost: ${total_reorder_cost:,.2f}**")
    else:
        st.success("All items are well stocked! No reorder suggestions at this time.")

def main():
    """Main inventory dashboard function"""

    st.title("📦 Inventory Dashboard")
    st.markdown("Real-time inventory tracking and management")

    # Load data
    inventory_items = get_inventory_data()

    # Display overview
    display_inventory_overview(inventory_items)

    st.markdown("---")

    # Display alerts
    display_stock_alerts(inventory_items)

    st.markdown("---")

    # Display detailed table
    display_inventory_table(inventory_items)

    st.markdown("---")

    # Display analysis
    display_category_analysis(inventory_items)

    st.markdown("---")

    # Display reorder suggestions
    display_reorder_suggestions(inventory_items)

    # Footer
    st.markdown("---")
    st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

if __name__ == "__main__":
    main()
