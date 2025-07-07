import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="⚡ Energy Consumption Calculator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
    }
    .energy-card {
        background: linear-gradient(135deg, #ff6b6b, #ffa500);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .day-selector {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .stSelectbox label {
        font-weight: bold;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'weekly_data' not in st.session_state:
    st.session_state.weekly_data = {
        'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0,
        'Friday': 0, 'Saturday': 0, 'Sunday': 0
    }

if 'user_info' not in st.session_state:
    st.session_state.user_info = {}

# Header
st.markdown("""
<div class="main-header">
    <h1>⚡ Smart Energy Consumption Calculator</h1>
    <p style="color: #f0f0f0; font-size: 1.2rem;">Track your daily energy usage and go green! 🌱</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for user information
st.sidebar.header("👤 User Information")
st.sidebar.markdown("---")

name = st.sidebar.text_input("📛 Enter Your Name:", placeholder="John Doe")
age = st.sidebar.number_input("🎂 Enter Your Age:", min_value=1, max_value=120, value=25)
city = st.sidebar.text_input("🏙️ Enter Your City:", placeholder="Mumbai")
area = st.sidebar.text_input("📍 Enter Your Area:", placeholder="Bandra")

st.sidebar.markdown("---")
st.sidebar.header("🏠 House Details")

house_type = st.sidebar.selectbox(
    "🏘️ House Type:",
    ["Flat", "Independent"],
    index=0
)

bhk = st.sidebar.selectbox(
    "🏠 How many BHK:",
    [1, 2, 3, 4],
    index=1
)

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🗓️ Daily Energy Calculator")
    
    # Day selector
    selected_day = st.selectbox(
        "📅 Select Day:",
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        index=0
    )
    
    st.markdown("---")
    st.subheader("🔌 Appliances")
    
    # Appliances input
    has_ac = st.checkbox("❄️ Air Conditioner", key=f"ac_{selected_day}")
    has_fridge = st.checkbox("🧊 Refrigerator", key=f"fridge_{selected_day}")
    has_washing_machine = st.checkbox("👕 Washing Machine", key=f"wm_{selected_day}")
    
    # Additional appliances for more fun
    has_tv = st.checkbox("📺 Television", key=f"tv_{selected_day}")
    has_microwave = st.checkbox("🍽️ Microwave", key=f"microwave_{selected_day}")
    has_dishwasher = st.checkbox("🍽️ Dishwasher", key=f"dishwasher_{selected_day}")
    
    # Calculate energy consumption
    def calculate_energy(bhk, has_ac, has_fridge, has_wm, has_tv, has_microwave, has_dishwasher):
        # Base energy calculation (fixed the bug in original code)
        if bhk == 1:
            energy = 2 * 0.4 + 2 * 0.8
        elif bhk == 2:
            energy = 3 * 0.4 + 3 * 0.8
        elif bhk == 3:  # Fixed: was bhk==2 again
            energy = 4 * 0.4 + 4 * 0.8
        else:  # 4 BHK
            energy = 5 * 0.4 + 5 * 0.8
        
        # Add appliances
        if has_ac:
            energy += 3
        if has_fridge:
            energy += 4
        if has_wm:
            energy += 2
        if has_tv:
            energy += 1.5
        if has_microwave:
            energy += 1
        if has_dishwasher:
            energy += 2.5
        
        return round(energy, 2)
    
    # Calculate and store daily energy
    daily_energy = calculate_energy(bhk, has_ac, has_fridge, has_washing_machine, 
                                   has_tv, has_microwave, has_dishwasher)
    
    if st.button(f"💾 Save {selected_day}'s Data", type="primary"):
        st.session_state.weekly_data[selected_day] = daily_energy
        st.success(f"✅ {selected_day}'s energy consumption saved: {daily_energy} kWh")
    
    # Display current day's energy
    st.markdown(f"""
    <div class="energy-card">
        <h2>⚡ {selected_day}'s Energy</h2>
        <h1>{daily_energy} kWh</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.header("📊 Weekly Energy Dashboard")
    
    # Weekly summary
    weekly_total = sum(st.session_state.weekly_data.values())
    weekly_avg = weekly_total / 7 if weekly_total > 0 else 0
    
    # Metrics
    col_metric1, col_metric2, col_metric3 = st.columns(3)
    
    with col_metric1:
        st.metric("📈 Weekly Total", f"{weekly_total:.2f} kWh")
    
    with col_metric2:
        st.metric("📊 Daily Average", f"{weekly_avg:.2f} kWh")
    
    with col_metric3:
        cost_estimate = weekly_total * 8  # Assuming ₹8 per kWh
        st.metric("💰 Weekly Cost", f"₹{cost_estimate:.2f}")
    
    # Weekly bar chart
    days = list(st.session_state.weekly_data.keys())
    values = list(st.session_state.weekly_data.values())
    
    fig_bar = go.Figure(data=[
        go.Bar(
            x=days,
            y=values,
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3', '#54A0FF'],
            text=values,
            textposition='auto',
        )
    ])
    
    fig_bar.update_layout(
        title="📊 Weekly Energy Consumption",
        xaxis_title="Days",
        yaxis_title="Energy (kWh)",
        showlegend=False,
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Weekly pie chart
    if weekly_total > 0:
        fig_pie = px.pie(
            values=values,
            names=days,
            title="🥧 Weekly Energy Distribution",
            color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3', '#54A0FF']
        )
        
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)

# Bottom section with additional insights
st.markdown("---")
st.header("🌱 Energy Insights & Tips")

col_tip1, col_tip2, col_tip3 = st.columns(3)

with col_tip1:
    st.info("""
    💡 **Energy Saving Tips**
    - Use LED bulbs
    - Unplug devices when not in use
    - Set AC to 24°C or higher
    - Use natural light during day
    """)

with col_tip2:
    st.warning("""
    ⚠️ **High Consumption Alert**
    - AC uses most energy (3 kWh/day)
    - Fridge runs 24/7 (4 kWh/day)
    - Consider energy-efficient appliances
    """)

with col_tip3:
    # Environmental impact
    carbon_footprint = weekly_total * 0.82  # kg CO2 per kWh in India
    st.success(f"""
    🌍 **Environmental Impact**
    - Weekly CO2: {carbon_footprint:.2f} kg
    - Monthly CO2: {carbon_footprint * 4:.2f} kg
    - Plant {int(carbon_footprint/22)} trees to offset!
    """)

# Reset button
if st.button("🔄 Reset All Data", type="secondary"):
    st.session_state.weekly_data = {
        'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0,
        'Friday': 0, 'Saturday': 0, 'Sunday': 0
    }
    st.success("✅ All data has been reset!")
    st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-top: 2rem;">
    <p style="color: white; margin: 0;">⚡ Made with ❤️ for a greener tomorrow 🌱</p>
    <p style="color: #f0f0f0; margin: 0; font-size: 0.9rem;">Track • Save • Sustain</p>
</div>
""", unsafe_allow_html=True)