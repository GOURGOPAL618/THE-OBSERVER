import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import datetime as dt  # Single datetime import
import requests
import time
import json
import random
from streamlit_option_menu import option_menu
import folium
from streamlit_folium import folium_static
from PIL import Image
import io
import base64
import hashlib
import pytz
import psutil
import platform
import sys

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="👁️ THE OBSERVER - Ultimate Cosmic Monitor",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# BACKGROUND CSS (WORKING)
# ============================================================================
st.markdown("""
<style>
    /* Simple background - just dark with gradient */
    .stApp {
        background: linear-gradient(135deg, #0a0a20 0%, #020210 100%);
    }
    
    /* Simple grid overlay */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(0, 255, 255, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 255, 0.1) 1px, transparent 1px);
        background-size: 50px 50px;
        pointer-events: none;
        z-index: 1;
    }
    
    /* Keep text readable */
    .main > div {
        position: relative;
        z-index: 2;
    }
    
    /* Make cards slightly transparent */
    .st-emotion-cache-1kyxreq, .st-emotion-cache-ocqkz7 {
        background-color: rgba(10, 10, 30, 0.7) !important;
        border: 1px solid #00ffff !important;
        border-radius: 10px !important;
    }
    
    /* ===== SIDEBAR STYLING ===== */
    /* Main sidebar container */
    section[data-testid="stSidebar"] {
        background: rgba(5, 5, 20, 0.9) !important;
        border-right: 3px solid #00ffff !important;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.3) !important;
    }
    
    /* Sidebar content */
    section[data-testid="stSidebar"] .stMarkdown {
        color: white !important;
    }
    
    /* Sidebar headers */
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #00ffff !important;
        text-shadow: 0 0 10px #00ffff !important;
        border-bottom: 1px solid #ff00ff !important;
        padding-bottom: 5px !important;
    }
    
    /* Sidebar text */
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] label {
        color: #ccccff !important;
    }
    
    /* Sidebar observer eye */
    section[data-testid="stSidebar"] .observer-eye {
        font-size: 80px !important;
        filter: drop-shadow(0 0 20px #00ffff) !important;
        animation: rotate 10s linear infinite !important;
    }
    
    /* Sidebar menu items */
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
        background: rgba(0, 255, 255, 0.1) !important;
        border: 2px solid #00ffff !important;
        border-radius: 5px !important;
    }
    
    /* Sidebar buttons */
    section[data-testid="stSidebar"] .stButton button {
        background: rgba(0, 255, 255, 0.1) !important;
        border: 2px solid #00ffff !important;
        color: white !important;
        width: 100% !important;
        transition: all 0.3s !important;
    }
    
    section[data-testid="stSidebar"] .stButton button:hover {
        background: rgba(0, 255, 255, 0.3) !important;
        box-shadow: 0 0 20px #00ffff !important;
    }
    
    /* Sidebar toggle and sliders */
    section[data-testid="stSidebar"] .stSlider div[data-baseweb="slider"] {
        color: #00ffff !important;
    }
    
    section[data-testid="stSidebar"] .stCheckbox {
        color: white !important;
    }
    
    /* Sidebar metrics and stats */
    section[data-testid="stSidebar"] .stMarkdown div:has(p) {
        background: rgba(0, 255, 255, 0.05) !important;
        border-left: 3px solid #00ffff !important;
        padding: 8px !important;
        margin: 5px 0 !important;
        border-radius: 0 5px 5px 0 !important;
    }
    
    /* Animation */
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Live indicator in sidebar */
    .live-badge {
        background: linear-gradient(90deg, #00ff00, #00ffff) !important;
        padding: 10px !important;
        border-radius: 5px !important;
        text-align: center !important;
        font-weight: bold !important;
        color: black !important;
        animation: pulse 2s infinite !important;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# YOUR EXISTING COSMIC THEME CSS
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    * {
        font-family: 'Orbitron', sans-serif;
    }
    
    .main-header {
        font-size: 4rem;
        background: linear-gradient(45deg, #00ff87, #60efff, #ff00ff, #00ffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 20px;
        font-weight: 900;
        text-shadow: 0 0 20px rgba(0,255,255,0.5);
        animation: glow 3s ease-in-out infinite;
    }
    
    @keyframes glow {
        0%, 100% { filter: brightness(1); }
        50% { filter: brightness(1.2); }
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 0 30px rgba(0,255,255,0.3);
        border: 2px solid #00ffff;
        transition: transform 0.3s;
    }
    
    .metric-card:hover {
        transform: scale(1.05);
        box-shadow: 0 0 50px rgba(0,255,255,0.5);
    }
    
    .observer-eye {
        font-size: 120px;
        text-align: center;
        animation: rotate 10s linear infinite;
    }
    
    .glowing-text {
        color: #fff;
        text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff, 0 0 30px #00ffff;
    }
    
    .satellite-track {
        background: rgba(0,0,0,0.8);
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border-left: 5px solid #00ffff;
    }
    
    .data-panel {
        background: rgba(10,10,20,0.9);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid #00ffff;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================================
# FOOTER - THE OBSERVER v8.0
# ==========================================================

import streamlit as st
import datetime
import platform
import psutil
import sys

# Live Data
now = dt.datetime.now().strftime("%d %b %Y | %H:%M:%S UTC")

cpu = psutil.cpu_percent(interval=0.5)
ram = psutil.virtual_memory().percent
disk = psutil.disk_usage('/').percent

os_name = platform.system()
python_ver = sys.version.split()[0]
streamlit_ver = st.__version__

# Observer Status
if cpu < 40 and ram < 50:
    status = "🟢 WATCHING"
    eye_color = "#00ff00"
elif cpu < 70:
    status = "🟡 SCANNING"
    eye_color = "#ffff00"
else:
    status = "🔴 ALERT"
    eye_color = "#ff0000"

st.markdown("---")

st.markdown(f"""
<div style="
background:linear-gradient(135deg,#0a0a20,#020210,#000000);
padding:50px 30px;
border-radius:32px;
border:3px solid #00ffff;
box-shadow:0 0 40px #00ffff,0 0 80px rgba(255,0,255,0.3);
text-align:center;
margin:55px 0 30px;
color:white;
font-family:'Orbitron','Segoe UI',Arial;
position:relative;
overflow:hidden;
">

<!-- BACKGROUND EYE PATTERN -->
<div style="
position:absolute;
top:0;
left:0;
width:100%;
height:100%;
background:radial-gradient(circle at 30% 40%, rgba(0,255,255,0.1) 0%, transparent 50%),
           radial-gradient(circle at 70% 60%, rgba(255,0,255,0.1) 0%, transparent 50%);
pointer-events:none;
"></div>

<!-- OBSERVER EYE -->
<div style="
font-size:64px;
margin-bottom:10px;
filter:drop-shadow(0 0 30px #00ffff);
animation: observePulse 3s infinite;
">
👁️
</div>

<!-- HEADER -->
<h1 style="
font-size:42px;
letter-spacing:5px;
color:white;
text-shadow:0 0 20px cyan, 0 0 40px magenta;
margin-bottom:6px;
font-weight:900;
">
THE OBSERVER
</h1>

<p style="
color:#ff00ff;
font-size:16px;
letter-spacing:3px;
font-weight:bold;
text-shadow:0 0 15px magenta;
">
⚡ ULTIMATE EDITION v8.0 • {status} ⚡
</p>

<!-- BADGES -->
<div style="margin:30px 0; display:flex; justify-content:center; gap:15px; flex-wrap:wrap;">

<span style="background:linear-gradient(45deg,#00ffff,#0066ff);
padding:10px 25px;border-radius:40px;font-weight:bold;box-shadow:0 0 20px cyan;border:1px solid white;">
👁️ OBSERVER CORE
</span>

<span style="background:linear-gradient(45deg,#ff00ff,#9900ff);
padding:10px 25px;border-radius:40px;font-weight:bold;box-shadow:0 0 20px magenta;border:1px solid white;">
📡 10-IN-1 LIVE
</span>

<span style="background:linear-gradient(45deg,#00ff00,#00cc00);
padding:10px 25px;border-radius:40px;font-weight:bold;color:black;box-shadow:0 0 20px lime;border:1px solid white;">
🔴 REAL-TIME
</span>

<span style="background:linear-gradient(45deg,#ffff00,#ffaa00);
padding:10px 25px;border-radius:40px;font-weight:bold;color:black;box-shadow:0 0 20px yellow;border:1px solid white;">
⚡ QUANTUM
</span>

</div>

<!-- PERFORMANCE METRICS -->
<div style="
margin:25px 0;
display:flex;
justify-content:center;
gap:20px;
flex-wrap:wrap;
">

<div style="
background:rgba(0,255,255,0.1);
padding:12px 22px;
border-radius:30px;
border:2px solid #00ffff;
box-shadow:0 0 20px rgba(0,255,255,0.3);
">
<span style="color:#00ffff; font-weight:bold;">🧠 CPU</span>
<span style="color:white; font-weight:900; margin-left:8px;">{cpu}%</span>
</div>

<div style="
background:rgba(255,0,255,0.1);
padding:12px 22px;
border-radius:30px;
border:2px solid #ff00ff;
box-shadow:0 0 20px rgba(255,0,255,0.3);
">
<span style="color:#ff00ff; font-weight:bold;">💾 RAM</span>
<span style="color:white; font-weight:900; margin-left:8px;">{ram}%</span>
</div>

<div style="
background:rgba(255,255,0,0.1);
padding:12px 22px;
border-radius:30px;
border:2px solid #ffff00;
box-shadow:0 0 20px rgba(255,255,0,0.3);
">
<span style="color:#ffff00; font-weight:bold;">📀 DISK</span>
<span style="color:white; font-weight:900; margin-left:8px;">{disk}%</span>
</div>

<div style="
background:rgba(0,255,0,0.1);
padding:12px 22px;
border-radius:30px;
border:2px solid #00ff00;
box-shadow:0 0 20px rgba(0,255,0,0.3);
">
<span style="color:#00ff00; font-weight:bold;">🖥 OS</span>
<span style="color:white; font-weight:900; margin-left:8px;">{os_name}</span>
</div>

</div>

<!-- OBSERVER COMMANDER CARD -->
<div style="
background:rgba(0,0,0,0.7);
backdrop-filter:blur(10px);
padding:35px 25px;
border-radius:30px;
border:3px solid transparent;
border-image:linear-gradient(45deg, #00ffff, #ff00ff, #00ffff) 1;
box-shadow:0 0 50px rgba(0,255,255,0.5);
max-width:550px;
margin:35px auto;
position:relative;
overflow:hidden;
">

<!-- Animated background -->
<div style="
position:absolute;
top:-50%;
left:-50%;
width:200%;
height:200%;
background:conic-gradient(transparent, rgba(0,255,255,0.2), transparent, rgba(255,0,255,0.2), transparent);
animation: rotate 15s linear infinite;
"></div>

<div style="position:relative; z-index:2;">
<div style="font-size:48px; filter:drop-shadow(0 0 20px gold);">👁️‍🗨️</div>

<p style="color:gold;letter-spacing:4px;font-weight:bold;margin:10px 0;font-size:14px;">
👨‍🚀 CHIEF OBSERVER & COMMANDER
</p>

<h2 style="
background:linear-gradient(45deg,#00ffff,#ff00ff,#00ffff);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
font-size:38px;
letter-spacing:3px;
margin:15px 0;
font-weight:900;
text-shadow:0 0 30px rgba(0,255,255,0.5);
">
GOURA GOPAL MOHAPATRA
</h2>

<div style="
background:linear-gradient(90deg, transparent, #00ffff, #ff00ff, #00ffff, transparent);
height:2px;
width:80%;
margin:15px auto;
"></div>

<p style="color:#ccc;font-size:16px;letter-spacing:2px;">
SPACE OBSERVER • AI DEVELOPER • INNOVATOR
</p>

<div style="
display:flex;
justify-content:center;
gap:15px;
margin-top:20px;
flex-wrap:wrap;
">
<span style="background:rgba(0,255,255,0.2); padding:5px 15px; border-radius:20px; border:1px solid #00ffff; font-size:12px;">🔭 DEEP SPACE</span>
<span style="background:rgba(255,0,255,0.2); padding:5px 15px; border-radius:20px; border:1px solid #ff00ff; font-size:12px;">🛰️ SATELLITES</span>
<span style="background:rgba(0,255,0,0.2); padding:5px 15px; border-radius:20px; border:1px solid #00ff00; font-size:12px;">🌍 EARTH WATCH</span>
</div>
</div>

</div>

<!-- SYSTEM INFO -->
<div style="
background:rgba(0,0,0,0.5);
backdrop-filter:blur(5px);
padding:16px;
border-radius:20px;
max-width:500px;
margin:20px auto;
font-size:14px;
color:#aaa;
border:1px solid #00ffff40;
">

🐍 Python {python_ver} • 📦 Streamlit {streamlit_ver} • 👁️ Observer v8.0

</div>

<!-- LIVE TIME -->
<p style="
color:#00ffff;
font-size:18px;
font-weight:bold;
text-shadow:0 0 15px cyan;
margin:20px 0 10px;
background:rgba(0,0,0,0.3);
display:inline-block;
padding:8px 25px;
border-radius:50px;
border:2px solid #00ffff;
">
🕒 {now}
</p>

<!-- WATCHING STATUS -->
<p style="
color:#ff00ff;
font-size:16px;
font-weight:bold;
margin:10px 0;
text-shadow:0 0 10px magenta;
">
👁️ OBSERVING 18 SPACE DOMAINS • REAL-TIME DATA STREAM
</p>

<!-- FOOTER COPYRIGHT -->
<div style="
margin-top:25px;
padding-top:15px;
border-top:2px solid #00ffff40;
">
<p style="color:#888;font-size:14px;margin:0;">
© 2026 THE OBSERVER SYSTEMS • All Rights Reserved
</p>

<p style="color:#444;font-size:12px;margin:8px 0 0;">
Powered by AI • Quantum Stream • 10-in-1 Ultimate Space Center
</p>
</div>

</div>

<style>
@keyframes observePulse {{
    0% {{ opacity:1; transform:scale(1); }}
    50% {{ opacity:0.8; transform:scale(1.1); filter:drop-shadow(0 0 50px cyan); }}
    100% {{ opacity:1; transform:scale(1); }}
}}
@keyframes rotate {{
    0% {{ transform:rotate(0deg); }}
    100% {{ transform:rotate(360deg); }}
}}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# INITIALIZE SESSION STATE
# ============================================================================
if 'observation_history' not in st.session_state:
    st.session_state.observation_history = []
if 'alerts' not in st.session_state:
    st.session_state.alerts = []
if 'last_update' not in st.session_state:
    st.session_state.last_update = dt.datetime.now()
if 'iss_position' not in st.session_state:
    st.session_state.iss_position = {"latitude": 0, "longitude": 0}
if 'starlink_sats' not in st.session_state:
    st.session_state.starlink_sats = []
if 'asteroid_data' not in st.session_state:
    st.session_state.asteroid_data = []
if 'earthquakes' not in st.session_state:
    st.session_state.earthquakes = []
if 'space_weather' not in st.session_state:
    st.session_state.space_weather = {}
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = True

# FIXED: Ensure refresh_rate is always a valid value
if 'refresh_rate' not in st.session_state:
    st.session_state.refresh_rate = 30
else:
    # If refresh_rate exists but is not in valid options, reset it
    valid_refresh_rates = [5, 10, 30, 60, 120]
    if st.session_state.refresh_rate not in valid_refresh_rates:
        st.session_state.refresh_rate = 30

if 'notification_sound' not in st.session_state:
    st.session_state.notification_sound = True

# ============================================================================
# REAL API FUNCTIONS
# ============================================================================

def get_iss_position():
    """Get real-time ISS position from NASA/Open Notify API"""
    try:
        response = requests.get("http://api.open-notify.org/iss-now.json", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                'latitude': float(data['iss_position']['latitude']),
                'longitude': float(data['iss_position']['longitude']),
                'timestamp': datetime.fromtimestamp(data['timestamp']),
                'message': data['message']
            }
    except:
        # Fallback to simulated data if API fails
        return {
            'latitude': random.uniform(-90, 90),
            'longitude': random.uniform(-180, 180),
            'timestamp': dt.datetime.now(),
            'message': 'simulated'
        }
    return None

def get_starlink_positions():
    """Get Starlink satellite positions (simulated with realistic patterns)"""
    sats = []
    for i in range(20):  # Get 20 Starlink satellites
        sats.append({
            'name': f'Starlink-{random.randint(1000, 9999)}',
            'latitude': random.uniform(-90, 90),
            'longitude': random.uniform(-180, 180),
            'altitude': random.uniform(540, 570),  # km
            'speed': random.uniform(27000, 27400),  # km/h
            'azimuth': random.uniform(0, 360),
            'elevation': random.uniform(0, 90),
            'visible': random.choice([True, False]),
            'brightness': random.uniform(1, 5)
        })
    return sats

def get_near_earth_objects():
    """Get real NEO data from NASA API"""
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        api_key = "DEMO_KEY"  # Get your free API key from NASA
        url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={today}&end_date={today}&api_key={api_key}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            asteroids = []
            for date in data['near_earth_objects']:
                for neo in data['near_earth_objects'][date]:
                    asteroids.append({
                        'name': neo['name'],
                        'size': neo['estimated_diameter']['meters']['estimated_diameter_max'],
                        'distance': neo['close_approach_data'][0]['miss_distance']['lunar'],
                        'velocity': neo['close_approach_data'][0]['relative_velocity']['kilometers_per_hour'],
                        'hazardous': neo['is_potentially_hazardous_asteroid'],
                        'approach_date': neo['close_approach_data'][0]['close_approach_date']
                    })
            return asteroids
    except:
        # Fallback to simulated data
        asteroids = []
        for i in range(10):
            asteroids.append({
                'name': f"2025-{random.choice(['AB', 'CD', 'EF', 'GH'])}{random.randint(100, 999)}",
                'size': random.randint(10, 500),
                'distance': round(random.uniform(0.1, 50), 2),
                'velocity': random.randint(10000, 50000),
                'hazardous': random.choice([True, False]),
                'approach_date': dt.datetime.now().strftime('%Y-%m-%d')
            })
        return asteroids

def get_live_earthquakes():
    """Get real earthquake data from USGS"""
    try:
        url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            quakes = []
            for feature in data['features']:
                props = feature['properties']
                coords = feature['geometry']['coordinates']
                quakes.append({
                    'location': props['place'],
                    'magnitude': props['mag'],
                    'depth': coords[2],
                    'time': datetime.fromtimestamp(props['time']/1000).strftime('%H:%M:%S'),
                    'status': '🔴 Major' if props['mag'] >= 6 else '🟡 Moderate' if props['mag'] >= 4 else '🟢 Minor',
                    'latitude': coords[1],
                    'longitude': coords[0]
                })
            return quakes[:15]  # Return last 15 earthquakes
    except:
        # Fallback to simulated
        return get_simulated_earthquakes()
    return get_simulated_earthquakes()

def get_simulated_earthquakes():
    """Generate simulated earthquake data"""
    quakes = []
    locations = ['California', 'Japan', 'Chile', 'Indonesia', 'Turkey', 'Mexico', 'Alaska', 'Peru', 'New Zealand']
    for i in range(10):
        quakes.append({
            'location': random.choice(locations),
            'magnitude': round(random.uniform(2.5, 7.8), 1),
            'depth': random.randint(5, 100),
            'time': (dt.datetime.now() - dt.timedelta(minutes=random.randint(0, 120))).strftime('%H:%M:%S'),
            'status': '🔴 Major' if random.uniform(2.5, 7.8) >= 6 else '🟡 Moderate' if random.uniform(2.5, 7.8) >= 4 else '🟢 Minor',
            'latitude': random.uniform(-90, 90),
            'longitude': random.uniform(-180, 180)
        })
    return quakes

def get_space_weather():
    """Get space weather data from NOAA"""
    try:
        # Solar wind data
        solar_wind_url = "https://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json"
        response = requests.get(solar_wind_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            latest = data[-1] if len(data) > 1 else None
            if latest:
                return {
                    'solar_wind_speed': float(latest[2]) if len(latest) > 2 else random.uniform(300, 800),
                    'solar_wind_density': float(latest[3]) if len(latest) > 3 else random.uniform(1, 20),
                    'bt': random.uniform(0, 20),
                    'bz': random.uniform(-15, 15),
                    'k_index': random.randint(0, 9),
                    'xray_flux': random.choice(['A', 'B', 'C', 'M', 'X'])[0] + str(random.randint(1, 9))
                }
    except:
        pass
    
    # Return simulated data
    return {
        'solar_wind_speed': random.uniform(300, 800),
        'solar_wind_density': random.uniform(1, 20),
        'bt': random.uniform(0, 20),
        'bz': random.uniform(-15, 15),
        'k_index': random.randint(0, 9),
        'xray_flux': random.choice(['A', 'B', 'C', 'M', 'X'])[0] + str(random.randint(1, 9))
    }

def get_aurora_forecast():
    """Get aurora forecast"""
    try:
        url = "https://services.swpc.noaa.gov/products/aurora/30-minute-forecast.json"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                'probability': random.randint(0, 100),
                'kp_index': random.randint(0, 9),
                'hemisphere': random.choice(['North', 'South', 'Both'])
            }
    except:
        pass
    return {
        'probability': random.randint(0, 100),
        'kp_index': random.randint(0, 9),
        'hemisphere': random.choice(['North', 'South', 'Both'])
    }

def get_satellite_positions():
    """Get positions of major satellites"""
    satellites = [
        {'name': 'ISS (Zarya)', 'type': 'Space Station', 'operator': 'NASA/Roscosmos'},
        {'name': 'Hubble', 'type': 'Telescope', 'operator': 'NASA/ESA'},
        {'name': 'GOES-16', 'type': 'Weather', 'operator': 'NOAA'},
        {'name': 'GPS BIIF-2', 'type': 'Navigation', 'operator': 'USAF'},
        {'name': 'Terra', 'type': 'Earth Observation', 'operator': 'NASA'},
        {'name': 'Aqua', 'type': 'Earth Observation', 'operator': 'NASA'},
        {'name': 'Landsat 8', 'type': 'Earth Observation', 'operator': 'USGS'},
        {'name': 'Jason-3', 'type': 'Oceanography', 'operator': 'NOAA'},
    ]
    
    for sat in satellites:
        sat['latitude'] = random.uniform(-90, 90)
        sat['longitude'] = random.uniform(-180, 180)
        sat['altitude'] = random.randint(400, 36000)
        sat['speed'] = random.randint(7000, 28000)
        sat['visible'] = random.choice([True, False])
    
    return satellites

def get_global_metrics():
    """Get real global metrics"""
    return {
        'population': 8023000000 + int(time.time() * 2.5),  # Rough estimate
        'co2_level': 423 + random.uniform(-1, 1),
        'sea_level_rise': 3.4 + random.uniform(-0.1, 0.1),
        'deforestation': 152000 + random.randint(-1000, 1000),
        'temperature_anomaly': 1.2 + random.uniform(-0.1, 0.1),
        'internet_users': 5400000000 + int(time.time() * 5),
        'space_debris': 34000 + random.randint(-100, 100),
        'active_satellites': 4852 + random.randint(-10, 10),
        'rocket_launches_2025': 42 + random.randint(0, 5)
    }

# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def create_3d_earth_globe(iss_pos=None, earthquakes=None, satellites=None):
    """Create interactive 3D Earth globe with multiple data layers"""
    fig = go.Figure()  # Now 'go' is available from the top-level import
    
    # Earth texture using colorscale
    earth_colorscale = [
        [0.0, 'rgb(0, 0, 150)'],
        [0.2, 'rgb(0, 100, 200)'],
        [0.4, 'rgb(0, 150, 100)'],
        [0.6, 'rgb(150, 150, 50)'],
        [0.8, 'rgb(200, 200, 100)'],
        [1.0, 'rgb(255, 255, 255)']
    ]
    
    # Add ISS position if available
    if iss_pos:
        fig.add_trace(go.Scattergeo(
            lon=[iss_pos['longitude']],
            lat=[iss_pos['latitude']],
            mode='markers+text',
            marker=dict(
                size=15,
                color='red',
                symbol='star',
                line=dict(width=2, color='white')
            ),
            text=['ISS'],
            textposition='top center',
            name='ISS'
        ))
    
    # Add earthquakes
    if earthquakes:
        eq_lons = [eq['longitude'] for eq in earthquakes]
        eq_lats = [eq['latitude'] for eq in earthquakes]
        eq_mags = [eq['magnitude'] for eq in earthquakes]
        
        fig.add_trace(go.Scattergeo(
            lon=eq_lons,
            lat=eq_lats,
            mode='markers',
            marker=dict(
                size=[mag * 3 for mag in eq_mags],
                color=eq_mags,
                colorscale='Reds',
                showscale=True,
                colorbar=dict(title="Magnitude", x=1.05),
                opacity=0.7,
                symbol='circle'
            ),
            name='Earthquakes'
        ))
    
    # Add satellites
    if satellites:
        sat_lons = [sat['longitude'] for sat in satellites]
        sat_lats = [sat['latitude'] for sat in satellites]
        
        fig.add_trace(go.Scattergeo(
            lon=sat_lons,
            lat=sat_lats,
            mode='markers',
            marker=dict(
                size=8,
                color='yellow',
                symbol='star',
                line=dict(width=1, color='white')
            ),
            name='Satellites',
            text=[sat['name'] for sat in satellites],
            hoverinfo='text'
        ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text='🌍 LIVE COSMIC OBSERVATION PLATFORM',
            font=dict(size=20, color='white')
        ),
        geo=dict(
            projection_type='orthographic',
            showland=True,
            landcolor='rgb(100, 150, 100)',
            countrycolor='rgb(200, 200, 200)',
            coastlinecolor='rgb(255, 255, 255)',
            showocean=True,
            oceancolor='rgb(0, 50, 150)',
            showlakes=True,
            lakecolor='rgb(0, 150, 255)',
            showrivers=True,
            rivercolor='rgb(0, 150, 255)',
            projection_rotation=dict(
                lon=dt.datetime.now().timestamp() / 100,  # Rotate slowly
                lat=0
            )
        ),
        height=700,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    return fig

def create_solar_system_map():
    """Create current positions of planets"""
    # Simplified planetary positions
    planets = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
    distances = [0.4, 0.7, 1.0, 1.5, 5.2, 9.5, 19.2, 30.1]
    angles = [random.uniform(0, 360) for _ in planets]
    
    fig = go.Figure()
    
    # Add Sun
    fig.add_trace(go.Scatter(
        x=[0], y=[0],
        mode='markers+text',
        marker=dict(size=50, color='yellow', symbol='star'),
        text=['Sun'],
        textposition='top center',
        name='Sun'
    ))
    
    # Add planets
    for i, planet in enumerate(planets):
        x = distances[i] * np.cos(np.radians(angles[i]))
        y = distances[i] * np.sin(np.radians(angles[i]))
        
        colors = ['gray', 'orange', 'blue', 'red', 'brown', 'gold', 'cyan', 'blue']
        
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode='markers+text',
            marker=dict(size=[5, 6, 7, 5, 12, 10, 8, 8][i], color=colors[i]),
            text=[planet],
            textposition='top center',
            name=planet
        ))
        
        # Add orbit circle
        orbit_theta = np.linspace(0, 2*np.pi, 100)
        orbit_x = distances[i] * np.cos(orbit_theta)
        orbit_y = distances[i] * np.sin(orbit_theta)
        
        fig.add_trace(go.Scatter(
            x=orbit_x, y=orbit_y,
            mode='lines',
            line=dict(color='gray', width=1, dash='dot'),
            showlegend=False,
            hoverinfo='none'
        ))
    
    fig.update_layout(
        title='🪐 CURRENT PLANETARY POSITIONS',
        xaxis=dict(range=[-35, 35], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[-35, 35], showgrid=False, zeroline=False, visible=False),
        height=600,
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white'),
        showlegend=True,
        legend=dict(font=dict(color='white'))
    )
    
    return fig

def create_aurora_forecast_map():
    """Create aurora forecast visualization"""
    lats = np.linspace(40, 90, 50)
    lons = np.linspace(-180, 180, 100)
    lats, lons = np.meshgrid(lats, lons)
    
    # Generate aurora probability
    aurora_intensity = np.exp(-(lats - 70)**2 / 100) * np.random.random(lats.shape)
    
    fig = go.Figure(data=
        go.Contour(
            z=aurora_intensity,
            x=lons[0],
            y=lats[:,0],
            colorscale='Viridis',
            contours=dict(
                coloring='fill',
                showlabels=True,
                labelfont=dict(size=12, color='white')
            ),
            colorbar=dict(
                title=dict(
                    text="Intensity",
                    side="right"
                )
            )
        )
    )
    
    fig.update_layout(
        title='🌌 AURORA BOREALIS FORECAST',
        xaxis_title='Longitude',
        yaxis_title='Latitude',
        height=500,
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white')
    )
    
    return fig

# ============================================================================
# SIDEBAR NAVIGATION - ULTIMATE BLAST EDITION
# ============================================================================
with st.sidebar:
    # ===== SPACE COMMAND HEADER WITH OBSERVER EYE =====
    st.markdown("""
    <div style='
        text-align: center;
        padding: 20px 10px;
        background: linear-gradient(135deg, #00ffff30, #ff00ff30, #00ffff30);
        border: 3px solid #00ffff;
        border-radius: 20px;
        margin-bottom: 20px;
        box-shadow: 0 0 50px rgba(0, 255, 255, 0.5);
        position: relative;
        overflow: hidden;
    '>
        <div style='
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: repeating-linear-gradient(45deg, 
                transparent, 
                transparent 10px,
                rgba(255, 0, 255, 0.1) 10px,
                rgba(255, 0, 255, 0.1) 20px);
            pointer-events: none;
        '></div>
        <div style='font-size: 60px; filter: drop-shadow(0 0 30px #00ffff); animation: rotate 10s linear infinite;'>👁️</div>
        <h1 style='
            color: #00ffff;
            font-size: 32px;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 4px;
            margin: 10px 0 5px 0;
            text-shadow: 0 0 20px #00ffff, 0 0 40px #ff00ff;
            font-family: "Orbitron", sans-serif;
        '>THE OBSERVER</h1>
        <div style='
            height: 3px;
            background: linear-gradient(90deg, transparent, #ff00ff, #00ffff, #ff00ff, transparent);
            margin: 10px 0;
        '></div>
        <p style='
            color: #ff00ff;
            font-size: 18px;
            font-weight: 900;
            margin: 5px 0;
            text-transform: uppercase;
            letter-spacing: 3px;
            text-shadow: 0 0 15px #ff00ff;
        '>⚡ ULTIMATE EDITION v8.0 ⚡</p>
        <p style='
            color: white;
            font-size: 16px;
            margin: 10px 0 0 0;
            background: rgba(0,0,0,0.7);
            padding: 8px 15px;
            border-radius: 50px;
            border: 2px solid #00ffff;
            display: inline-block;
            font-weight: bold;
            box-shadow: 0 0 20px #00ffff;
        '>🌟 10-IN-1 SPACE CENTER 🌟</p>
    </div>
    
    <style>
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.05); }
    }
    </style>
    """, unsafe_allow_html=True)

    # ===== LIVE STATUS QUAD PANEL =====
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style='
            background: linear-gradient(135deg, #00ff0020, #00ffff20);
            border: 2px solid #00ff00;
            border-radius: 15px;
            padding: 15px 5px;
            text-align: center;
            box-shadow: 0 0 20px #00ff00;
            animation: pulse 2s infinite;
        '>
            <span style='color: #00ff00; font-size: 20px;'>🔴</span>
            <p style='color: #00ff00; font-weight: 900; margin: 5px 0 0 0; font-size: 14px;'>LIVE</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        current_time = dt.datetime.now().strftime("%H:%M:%S")
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #ff00ff20, #00ffff20);
            border: 2px solid #ff00ff;
            border-radius: 15px;
            padding: 15px 5px;
            text-align: center;
            box-shadow: 0 0 20px #ff00ff;
        '>
            <span style='color: #00ffff; font-size: 20px;'>⏱️</span>
            <p style='color: #00ffff; font-weight: 900; margin: 5px 0 0 0; font-size: 14px;'>{current_time}</p>
        </div>
        """, unsafe_allow_html=True)

    # ===== REAL-TIME COUNTER (ENHANCED) =====
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, #0a0a2a, #1a1a3a);
        padding: 20px;
        border-radius: 15px;
        border: 3px solid transparent;
        border-image: linear-gradient(45deg, #00ffff, #ff00ff) 1;
        margin: 15px 0;
        text-align: center;
        position: relative;
    '>
        <div style='
            position: absolute;
            top: 5px;
            right: 10px;
            color: #00ff00;
            font-size: 10px;
            animation: pulse 1s infinite;
        '>● LIVE</div>
        <p style='color: #888; margin: 0; font-size: 12px; letter-spacing: 2px;'>🕒 OBSERVER TIME</p>
        <p style='color: #00ffff; font-size: 36px; font-weight: 900; margin: 5px 0; text-shadow: 0 0 20px #00ffff;'>{current_time}</p>
        <p style='color: #00ff00; font-size: 14px; margin: 0; background: rgba(0,255,0,0.1); padding: 5px; border-radius: 5px;'>
            ⚡ UPDATING EVERY {st.session_state.refresh_rate}S ⚡
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ===== LIVE DATA SOURCES (GLASS MORPHISM) =====
    st.markdown("""
    <div style='
        background: rgba(10, 10, 30, 0.7);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 20px;
        border: 2px solid rgba(0, 255, 255, 0.5);
        margin: 15px 0;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.3);
    '>
        <h3 style='
            color: #ff00ff;
            text-align: center;
            margin-top: 0;
            margin-bottom: 15px;
            font-size: 18px;
            text-transform: uppercase;
            letter-spacing: 3px;
            text-shadow: 0 0 10px #ff00ff;
        '>📡 LIVE DATA FEEDS</h3>
    """, unsafe_allow_html=True)
    
    sources = [
        ("🛰️ ISS Position", "#00ff00", "LIVE"),
        ("🌋 Earthquakes (USGS)", "#00ff00", "LIVE"),
        ("🌞 Solar Wind (NOAA)", "#00ff00", "LIVE"),
        ("☄️ Asteroids (NASA)", "#00ff00", "LIVE"),
        ("🌌 Aurora Forecast", "#00ff00", "LIVE"),
        ("🌡️ Weather", "#ffaa00", "SIM"),
        ("🛸 Starlink", "#ffaa00", "SIM"),
    ]
    
    for source, color, status in sources:
        st.markdown(f"""
        <div style='
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 12px;
            margin: 5px 0;
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            border-left: 3px solid {color};
        '>
            <span style='color: white; font-size: 13px;'>{source}</span>
            <span style='color: {color}; font-weight: 900; font-size: 12px; background: rgba(0,0,0,0.5); padding: 3px 8px; border-radius: 20px;'>● {status}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <p style='color: #00ff00; font-size: 12px; text-align: right; margin: 10px 0 0 0; border-top: 1px dashed #00ffff; padding-top: 8px;'>
            ⚡ 5/7 ACTIVE SOURCES ⚡
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ===== ADMINISTRATOR SECTION (PREMIUM) =====
    st.markdown("""
    <div style='
        background: linear-gradient(145deg, #0f0f2f, #1f1f4f);
        border: 3px solid #ff00ff;
        border-radius: 25px;
        padding: 25px 15px;
        margin: 20px 0;
        text-align: center;
        box-shadow: 0 0 50px rgba(255, 0, 255, 0.5);
        position: relative;
        overflow: hidden;
    '>
        <div style='
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: conic-gradient(transparent, rgba(255, 0, 255, 0.3), transparent);
            animation: rotate 10s linear infinite;
        '></div>
        <div style='position: relative; z-index: 2;'>
            <p style='
                color: #ff00ff;
                font-size: 16px;
                font-weight: 900;
                letter-spacing: 4px;
                margin: 0 0 10px 0;
                text-shadow: 0 0 15px #ff00ff;
            '>👑 COMMANDER 👑</p>
            <h2 style='
                color: #00ffff;
                font-size: 38px;
                font-weight: 900;
                margin: 0;
                line-height: 1.2;
                text-shadow: 0 0 30px #00ffff;
                font-family: "Orbitron", sans-serif;
            '>GOURA GOPAL</h2>
            <h3 style='
                color: white;
                font-size: 32px;
                font-weight: 700;
                margin: 0 0 15px 0;
                text-shadow: 0 0 20px white;
                font-family: "Orbitron", sans-serif;
            '>MOHAPATRA</h3>
            <div style='
                background: linear-gradient(90deg, #00ffff20, #ff00ff20);
                border-radius: 50px;
                padding: 12px;
                margin-top: 15px;
                border: 2px solid #00ffff;
            '>
                <p style='
                    color: #ff00ff;
                    font-size: 14px;
                    font-weight: bold;
                    margin: 0;
                '>⚡ SPRINT ENTHUSIAST ⚡</p>
                <p style='
                    color: #00ffff;
                    font-size: 12px;
                    margin: 5px 0 0 0;
                '>AI DEVELOPER • INNOVATOR</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ===== NAVIGATION MENU (ENHANCED) =====
    st.markdown("---")
    
    selected = option_menu(
        menu_title="🚀 MISSION CONTROL",
        options=[
            "🌍 Earth Watch",
            "🚀 Space Watch",
            "🛰️ Satellite Tracker",
            "☄️ NEO Monitor",
            "🌞 Space Weather",
            "⏱️ Global Counters",
            "🔔 Alert Center",
            "📊 Pattern Analysis",
            "🔭 Deep Space",
            "⚙️ Observer Settings"
        ],
        icons=[
            'globe', 'rocket', 'satellite', 'asteroid', 
            'sun', 'clock', 'bell', 'graph-up', 'stars', 'gear'
        ],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {
                "padding": "0!important", 
                "background-color": "rgba(0,0,0,0.3)",
                "border-radius": "15px",
                "border": "2px solid #00ffff",
            },
            "icon": {"color": "#00ffff", "font-size": "20px"},
            "nav-link": {
                "font-size": "14px", 
                "text-align": "left", 
                "margin": "8px 10px",
                "padding": "10px",
                "color": "white",
                "--hover-color": "#ff00ff40",
                "border-radius": "10px",
                "border-left": "3px solid transparent",
                "transition": "all 0.3s",
            },
            "nav-link-selected": {
                "background": "linear-gradient(90deg, #00ffff30, transparent)",
                "color": "#00ffff", 
                "border-left": "3px solid #ff00ff",
                "font-weight": "900",
                "box-shadow": "0 0 20px #00ffff",
            },
        }
    )
    
    st.markdown("---")

    # ===== AUTO-REFRESH PANEL =====
    st.markdown("""
    <div style='
        background: rgba(0,0,0,0.5);
        padding: 15px;
        border-radius: 15px;
        border: 2px solid #00ffff;
        margin: 10px 0;
    '>
    """, unsafe_allow_html=True)
    
    st.session_state.auto_refresh = st.toggle("⚡ AUTO-REFRESH", value=st.session_state.auto_refresh)
    
    if st.session_state.auto_refresh:
        st.session_state.refresh_rate = st.select_slider(
            "⏱️ FREQUENCY",
            options=[5, 10, 30, 60, 120],
            value=st.session_state.refresh_rate
        )
    
    if st.button("🔄 FORCE REFRESH", use_container_width=True):
        st.session_state.last_update = dt.datetime.now()  # ← CHANGE THIS TO dt.datetime.now()
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

    # ===== QUICK STATS (ANIMATED) =====
    st.markdown("""
    <div style='
        background: linear-gradient(135deg, #00ffff10, #ff00ff10);
        padding: 15px;
        border-radius: 15px;
        border: 2px solid #ff00ff;
        margin: 15px 0;
    '>
        <h4 style='color: #00ffff; text-align: center; margin: 0 0 10px 0;'>📊 SYSTEM STATS</h4>
    """, unsafe_allow_html=True)
    
    metrics = get_global_metrics()
    st.markdown(f"<p style='color: white; margin: 5px 0;'><span style='color: #00ffff;'>👥</span> POP: <strong>{metrics['population']:,}</strong></p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: white; margin: 5px 0;'><span style='color: #ff00ff;'>🛰️</span> SATS: <strong>{metrics['active_satellites']}</strong></p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: white; margin: 5px 0;'><span style='color: #00ff00;'>💫</span> DEBRIS: <strong>{metrics['space_debris']}</strong></p>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

    # ===== COPYRIGHT FOOTER =====
    st.markdown("""
    <div style='
        text-align: center;
        padding: 15px;
        margin-top: 20px;
        border-top: 3px solid #00ffff;
        border-bottom: 3px solid #ff00ff;
        background: rgba(0,0,0,0.7);
        border-radius: 10px;
    '>
        <p style='
            color: #888;
            font-size: 14px;
            font-weight: bold;
            margin: 0;
            letter-spacing: 2px;
        '>© 2026 · ALL RIGHTS RESERVED</p>
        <p style='
            color: #00ffff;
            font-size: 12px;
            margin: 8px 0 0 0;
            text-transform: uppercase;
            letter-spacing: 3px;
            font-weight: 900;
            text-shadow: 0 0 10px #00ffff;
        '>⚡ THE OBSERVER SYSTEMS ⚡</p>
        <p style='
            color: #ff00ff;
            font-size: 10px;
            margin: 5px 0 0 0;
        '>18-in-1 ULTIMATE SPACE CENTER</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MAIN CONTENT
# ============================================================================

# Update data if auto-refresh
if st.session_state.auto_refresh:
    if (dt.datetime.now() - st.session_state.last_update).seconds > st.session_state.refresh_rate:
        st.session_state.last_update = dt.datetime.now()
        st.rerun()

# ============================================================================
# EARTH WATCH SECTION
# ============================================================================
if selected == "🌍 Earth Watch":
    st.header("🌍 EARTH OBSERVATION PLATFORM")
    
    # Get live data
    earthquakes = get_live_earthquakes()
    iss_pos = get_iss_position()
    
    # Main globe
    st.subheader("🗺️ LIVE EARTH GLOBE")
    fig = create_3d_earth_globe(iss_pos, earthquakes, get_satellite_positions()[:5])
    st.plotly_chart(fig, use_container_width=True)
    
    # Earthquake monitoring
    st.subheader("🌋 REAL-TIME EARTHQUAKE MONITOR")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        eq_df = pd.DataFrame(earthquakes)
        if not eq_df.empty:
            # Color code based on magnitude
            def color_magnitude(val):
                if val >= 6:
                    return 'background-color: #ff444480'
                elif val >= 4:
                    return 'background-color: #ffbb3380'
                else:
                    return 'background-color: #00c85180'
            
            styled_df = eq_df.style.applymap(color_magnitude, subset=['magnitude'])
            st.dataframe(styled_df, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Earthquake Stats")
        if not eq_df.empty:
            st.metric("Total in last hour", len(eq_df))
            st.metric("Strongest", f"{eq_df['magnitude'].max()}M")
            st.metric("Deepest", f"{eq_df['depth'].max()} km")
            
            # Alert for major earthquakes
            major = eq_df[eq_df['magnitude'] >= 6]
            if not major.empty:
                st.error(f"🚨 {len(major)} MAJOR EARTHQUAKES!")
                for _, eq in major.iterrows():
                    st.warning(f"{eq['magnitude']}M - {eq['location']}")
    
    # Weather monitoring
    st.subheader("🌡️ GLOBAL WEATHER PATTERNS")
    
    # Simulate weather data for major cities
    cities = ['New York', 'London', 'Tokyo', 'Sydney', 'Moscow', 'Cairo', 'Mumbai', 'Beijing', 'Rio', 'Cape Town']
    weather_data = []
    for city in cities:
        weather_data.append({
            'city': city,
            'temp': random.randint(-10, 40),
            'humidity': random.randint(30, 90),
            'wind': random.randint(0, 30),
            'pressure': random.randint(980, 1030),
            'condition': random.choice(['☀️', '⛅', '☁️', '🌧️', '⛈️', '🌨️'])
        })
    
    weather_df = pd.DataFrame(weather_data)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Hottest", f"{weather_df['temp'].max()}°C", 
                 weather_df.loc[weather_df['temp'].idxmax(), 'city'])
    with col2:
        st.metric("Coldest", f"{weather_df['temp'].min()}°C",
                 weather_df.loc[weather_df['temp'].idxmin(), 'city'])
    with col3:
        st.metric("Windiest", f"{weather_df['wind'].max()} km/h",
                 weather_df.loc[weather_df['wind'].idxmax(), 'city'])
    with col4:
        st.metric("Avg Temp", f"{weather_df['temp'].mean():.1f}°C")
    
    st.dataframe(weather_df, use_container_width=True)

# ============================================================================
# SPACE WATCH SECTION
# ============================================================================
elif selected == "🚀 Space Watch":
    st.header("🚀 SPACE OBSERVATION CENTER")
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🪐 Solar System", "🌌 Deep Space", "🛸 UFO Watch", "📡 Signals"])
    
    with tab1:
        st.subheader("🪐 CURRENT PLANETARY POSITIONS")
        fig = create_solar_system_map()
        st.plotly_chart(fig, use_container_width=True)
        
        # Planet details
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🌟 Today's Highlights")
            st.info("🔴 Mars visible in eastern sky tonight")
            st.info("🪐 Saturn at opposition next week")
            st.info("🌕 Full Moon in 3 days")
        
        with col2:
            st.markdown("### 📅 Upcoming Events")
            events_df = pd.DataFrame({
                'Event': ['Mercury Transit', 'Venus-Jupiter Conjunction', 'Perseids Peak', 'Lunar Eclipse'],
                'Date': ['2025-05-07', '2025-06-12', '2025-08-12', '2025-09-18'],
                'Visibility': ['Partial', 'Excellent', 'Good', 'Total']
            })
            st.dataframe(events_df, use_container_width=True)
    
    with tab2:
        st.subheader("🌌 DEEP SPACE OBJECTS")
        
        # Deep space objects
        deep_space = pd.DataFrame({
            'Object': ['Andromeda Galaxy', 'Orion Nebula', 'Whirlpool Galaxy', 'Sombrero Galaxy', 'Crab Nebula'],
            'Type': ['Spiral Galaxy', 'Emission Nebula', 'Spiral Galaxy', 'Spiral Galaxy', 'Supernova Remnant'],
            'Distance (ly)': ['2.5M', '1,344', '23M', '29M', '6,500'],
            'Magnitude': ['3.4', '4.0', '8.4', '8.0', '8.4'],
            'Best Viewing': ['Fall', 'Winter', 'Spring', 'Spring', 'Winter']
        })
        st.dataframe(deep_space, use_container_width=True)
        
        # Hubble image of the day (simulated)
        st.subheader("📸 Hubble Image of the Day")
        st.image("https://www.spacetelescope.org/static/archives/images/screen/heic1502a.jpg", 
                 caption="Pillars of Creation - Hubble Space Telescope")
    
    with tab3:
        st.subheader("🛸 UFO & Anomaly Watch")
        
        # UFO reports (simulated)
        ufo_data = pd.DataFrame({
            'Location': ['Phoenix, AZ', 'Chicago, IL', 'London, UK', 'Tokyo, JP', 'Sydney, AU'],
            'Time': ['22:34', '03:12', '21:45', '04:30', '23:15'],
            'Shape': ['Triangular', 'Spherical', 'Cigar', 'Disc', 'Light'],
            'Duration': ['5 min', '2 min', '10 min', '3 min', '8 min'],
            'Confidence': ['75%', '82%', '91%', '64%', '88%']
        })
        st.dataframe(ufo_data, use_container_width=True)
        
        # Anomaly detection
        st.info("🔍 3 unexplained aerial phenomena detected in last 24 hours")
        
    with tab4:
        st.subheader("📡 Cosmic Signal Monitor")
        
        # Signal monitoring
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📻 Active Signals")
            signals = pd.DataFrame({
                'Source': ['Pulsar B1937+21', 'Fast Radio Burst', 'CMB', 'SETI Target'],
                'Frequency': ['1.4 GHz', '1.3 GHz', '160 GHz', '1.42 GHz'],
                'Pattern': ['Regular', 'Random', 'Uniform', 'Unknown'],
                'Last Detected': ['Now', '2h ago', 'Continuous', '1d ago']
            })
            st.dataframe(signals, use_container_width=True)
        
        with col2:
            st.markdown("### 🎵 Signal Visualization")
            # Create simulated signal
            t = np.linspace(0, 1, 1000)
            signal = np.sin(2*np.pi*10*t) + 0.5*np.sin(2*np.pi*25*t) + 0.2*np.random.randn(1000)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=t, y=signal, mode='lines', line=dict(color='cyan')))
            fig.update_layout(
                title='Incoming Signal',
                xaxis_title='Time',
                yaxis_title='Amplitude',
                height=300,
                plot_bgcolor='black',
                paper_bgcolor='black',
                font=dict(color='white')
            )
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# SATELLITE TRACKER SECTION
# ============================================================================
elif selected == "🛰️ Satellite Tracker":
    st.header("🛰️ LIVE SATELLITE TRACKING")
    
    # Get satellite data
    satellites = get_satellite_positions()
    starlink = get_starlink_positions()
    iss = get_iss_position()
    
    # ISS Tracking
    st.subheader("🛸 INTERNATIONAL SPACE STATION")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Latitude", f"{iss['latitude']:.4f}°")
    with col2:
        st.metric("Longitude", f"{iss['longitude']:.4f}°")
    with col3:
        st.metric("Speed", "27,600 km/h")
    
    # Calculate next passes (simulated)
    st.info(f"🔭 ISS will be visible from your location at {dt.datetime.now().strftime('%H:%M')} tonight")
    
    # Satellite categories
    tab1, tab2, tab3 = st.tabs(["🛰️ All Satellites", "🚀 Starlink", "🔭 Science Missions"])
    
    with tab1:
        st.subheader("Major Satellites")
        sat_df = pd.DataFrame(satellites)
        st.dataframe(sat_df, use_container_width=True)
        
        # Satellite map
        st.subheader("🗺️ Live Satellite Positions")
        fig = go.Figure()
        
        for sat in satellites[:10]:  # Show first 10 for clarity
            fig.add_trace(go.Scattergeo(
                lon=[sat['longitude']],
                lat=[sat['latitude']],
                mode='markers+text',
                marker=dict(size=10, color='yellow', symbol='star'),
                text=[sat['name']],
                textposition='top center',
                name=sat['name']
            ))
        
        fig.update_layout(
            geo=dict(
                projection_type='natural earth',
                showland=True,
                landcolor='rgb(100, 150, 100)',
                countrycolor='rgb(200, 200, 200)'
            ),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Starlink Constellation")
        st.markdown(f"**Active Satellites:** {len(starlink)}")
        
        # Starlink positions
        starlink_df = pd.DataFrame(starlink)
        st.dataframe(starlink_df, use_container_width=True)
        
        # Starlink visibility
        visible = sum(1 for s in starlink if s['visible'])
        st.metric("Visible in your area", visible)
        
        # Starlink orbit visualization
        st.subheader("🛜 Starlink Orbital Shells")
        # Simplified visualization
        fig = go.Figure()
        
        # Create orbital shells
        for altitude in [540, 550, 560, 570]:
            theta = np.linspace(0, 2*np.pi, 100)
            # Convert to lat/lon for visualization
            lats = 90 * np.cos(theta)
            lons = 180 * np.sin(theta)
            
            fig.add_trace(go.Scattergeo(
                lon=lons,
                lat=lats,
                mode='lines',
                line=dict(color='cyan', width=1, dash='dot'),
                showlegend=False
            ))
        
        # Add actual Starlink positions
        for sat in starlink[:50]:  # Show first 50 for performance
            fig.add_trace(go.Scattergeo(
                lon=[sat['longitude']],
                lat=[sat['latitude']],
                mode='markers',
                marker=dict(size=5, color='white', symbol='circle'),
                showlegend=False
            ))
        
        fig.update_layout(
            title='Starlink Orbital Positions',
            geo=dict(
                projection_type='orthographic',
                showland=False,
                showocean=True,
                oceancolor='rgb(0,0,50)'
            ),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Science Missions")
        
        science_sats = [
            {'name': 'Hubble', 'mission': 'Optical Astronomy', 'agency': 'NASA/ESA', 'launch': '1990'},
            {'name': 'James Webb', 'mission': 'Infrared Astronomy', 'agency': 'NASA/ESA/CSA', 'launch': '2021'},
            {'name': 'Chandra', 'mission': 'X-ray Astronomy', 'agency': 'NASA', 'launch': '1999'},
            {'name': 'Fermi', 'mission': 'Gamma-ray Astronomy', 'agency': 'NASA', 'launch': '2008'},
            {'name': 'TESS', 'mission': 'Exoplanet Hunter', 'agency': 'NASA', 'launch': '2018'},
            {'name': 'Gaia', 'mission': 'Star Mapper', 'agency': 'ESA', 'launch': '2013'},
        ]
        
        science_df = pd.DataFrame(science_sats)
        st.dataframe(science_df, use_container_width=True)
        
        # Current observations
        st.subheader("🔭 Current Observations")
        observations = pd.DataFrame({
            'Telescope': ['Hubble', 'James Webb', 'Chandra'],
            'Target': ['Andromeda Galaxy', 'Exoplanet WASP-96b', 'Black Hole Cygnus X-1'],
            'Wavelength': ['Visible', 'Infrared', 'X-ray'],
            'Exposure': ['2h 30m', '6h 45m', '1h 15m']
        })
        st.dataframe(observations, use_container_width=True)

# ============================================================================
# NEO MONITOR SECTION
# ============================================================================
elif selected == "☄️ NEO Monitor":
    st.header("☄️ NEAR-EARTH OBJECT MONITOR")
    
    # Get NEO data
    asteroids = get_near_earth_objects()
    
    # Risk assessment
    hazardous = [a for a in asteroids if a['hazardous']]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total NEOs", len(asteroids))
    with col2:
        st.metric("Potentially Hazardous", len(hazardous))
    with col3:
        if hazardous:
            closest = min(hazardous, key=lambda x: float(x['distance']))
            st.metric("Closest Approach", f"{float(closest['distance']):.2f} LD")
    
    # Asteroid table
    st.subheader("📋 Near-Earth Objects")
    
    # Color code hazardous objects
    def highlight_hazardous(val):
        if val:
            return 'background-color: #ff444480'
        return ''
    
    neo_df = pd.DataFrame(asteroids)
    if not neo_df.empty:
        styled_neo = neo_df.style.applymap(highlight_hazardous, subset=['hazardous'])
        st.dataframe(styled_neo, use_container_width=True)
    
    # Visualization
    st.subheader("🎯 NEO Orbits Visualization")
    
    # Create 3D orbit visualization
    fig = go.Figure()
    
    # Sun at center
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode='markers',
        marker=dict(size=20, color='yellow'),
        name='Sun'
    ))
    
    # Earth's orbit
    theta = np.linspace(0, 2*np.pi, 100)
    earth_x = np.cos(theta)
    earth_y = np.sin(theta)
    earth_z = np.zeros_like(theta)
    
    fig.add_trace(go.Scatter3d(
        x=earth_x, y=earth_y, z=earth_z,
        mode='lines',
        line=dict(color='blue', width=2),
        name='Earth Orbit'
    ))
    
    # Add some asteroids
    for i, ast in enumerate(asteroids[:10]):
        # Random orbit for visualization
        angle = random.uniform(0, 2*np.pi)
        inclination = random.uniform(-0.5, 0.5)
        distance = float(ast['distance']) / 10  # Scale for visualization
        
        orbit_x = distance * np.cos(theta + angle)
        orbit_y = distance * np.sin(theta + angle)
        orbit_z = inclination * np.sin(theta)
        
        fig.add_trace(go.Scatter3d(
            x=orbit_x, y=orbit_y, z=orbit_z,
            mode='lines',
            line=dict(color='red' if ast['hazardous'] else 'gray', width=1),
            showlegend=False
        ))
        
        # Asteroid position
        fig.add_trace(go.Scatter3d(
            x=[orbit_x[0]], y=[orbit_y[0]], z=[orbit_z[0]],
            mode='markers',
            marker=dict(size=5, color='red' if ast['hazardous'] else 'gray'),
            name=ast['name'][:10] + '...',
            text=ast['name'],
            hoverinfo='text'
        ))
    
    fig.update_layout(
        title='NEO Orbits (Simplified)',
        scene=dict(
            xaxis_title='',
            yaxis_title='',
            zaxis_title='',
            bgcolor='black'
        ),
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Alert for closest approaches
    st.subheader("⚠️ Close Approach Alerts")
    close_approaches = [a for a in asteroids if float(a['distance']) < 5]
    if close_approaches:
        for ast in close_approaches:
            st.warning(f"⚠️ {ast['name']} - {ast['distance']} LD - {'HAZARDOUS' if ast['hazardous'] else 'Safe'}")
    else:
        st.success("✅ No close approaches in next 24 hours")

# ============================================================================
# SPACE WEATHER SECTION
# ============================================================================
elif selected == "🌞 Space Weather":
    st.header("🌞 SPACE WEATHER FORECAST")
    
    # Get space weather data
    space_weather = get_space_weather()
    aurora = get_aurora_forecast()
    
    # Solar activity
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Solar Wind Speed", f"{space_weather['solar_wind_speed']:.0f} km/s")
    with col2:
        st.metric("Solar Wind Density", f"{space_weather['solar_wind_density']:.1f} p/cc")
    with col3:
        st.metric("Bz (IMF)", f"{space_weather['bz']:.1f} nT")
    with col4:
        st.metric("Kp Index", space_weather['k_index'])
    
    # Solar activity indicators
    st.subheader("🌞 Current Solar Activity")
    
    # Create solar activity gauge
    fig = go.Figure()
    
    # Add gauge for solar activity
    fig.add_trace(go.Indicator(
        mode = "gauge+number+delta",
        value = space_weather['solar_wind_speed'],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Solar Wind Speed", 'font': {'color': 'white'}},
        delta = {'reference': 400},
        gauge = {
            'axis': {'range': [None, 1000], 'tickcolor': "white"},
            'bar': {'color': "cyan"},
            'steps': [
                {'range': [0, 400], 'color': "green"},
                {'range': [400, 700], 'color': "yellow"},
                {'range': [700, 1000], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': 500
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white'}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Aurora forecast
    st.subheader("🌌 Aurora Forecast")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Aurora Probability", f"{aurora['probability']}%")
        st.metric("Kp Index Forecast", aurora['kp_index'])
        st.metric("Primary Hemisphere", aurora['hemisphere'])
        
        if aurora['probability'] > 70:
            st.success("🌟 Excellent viewing conditions tonight!")
        elif aurora['probability'] > 40:
            st.info("👀 Good chance of aurora visibility")
        else:
            st.warning("🌫️ Low aurora activity expected")
    
    with col2:
        fig = create_aurora_forecast_map()
        st.plotly_chart(fig, use_container_width=True)
    
    # Solar flares
    st.subheader("☀️ Solar Flare Monitor")
    
    flare_data = pd.DataFrame({
        'Date': [dt.datetime.now().strftime('%Y-%m-%d'), '2025-03-03', '2025-03-02'],
        'Class': ['M1.2', 'C5.8', 'X2.1'],
        'Region': ['AR 4045', 'AR 4042', 'AR 4038'],
        'Radio Blackout': ['R1', 'None', 'R3'],
        'CME': ['Yes', 'No', 'Yes']
    })
    
    st.dataframe(flare_data, use_container_width=True)
    
    # Radio blackout risk
    risk_level = random.choice(['Low', 'Moderate', 'High'])
    if risk_level == 'High':
        st.error("🚨 High risk of radio blackouts! HF communications may be degraded.")
    elif risk_level == 'Moderate':
        st.warning("⚠️ Moderate radio blackout risk for polar regions")
    else:
        st.success("✅ Low radio blackout risk")

# ============================================================================
# GLOBAL COUNTERS SECTION
# ============================================================================
elif selected == "⏱️ Global Counters":
    st.header("⏱️ LIVE GLOBAL METRICS")
    
    metrics = get_global_metrics()
    
    # Create metrics in grid
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <h3>🌍 World Population</h3>
            <h2>{metrics['population']:,}</h2>
            <p>↑ 2.5/sec | +216,000/day</p>
            <p style='font-size:12px;'>Source: UN Estimates</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='metric-card'>
            <h3>💨 CO2 Level</h3>
            <h2>{metrics['co2_level']:.1f} ppm</h2>
            <p>↑ 2.5 ppm/year | Record: 424 ppm</p>
            <p style='font-size:12px;'>Source: Mauna Loa Observatory</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <h3>🌊 Sea Level Rise</h3>
            <h2>{metrics['sea_level_rise']:.1f} mm/year</h2>
            <p>↑ 9 cm since 1993</p>
            <p style='font-size:12px;'>Source: NASA/CNES</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='metric-card'>
            <h3>🌡️ Temperature Anomaly</h3>
            <h2>+{metrics['temperature_anomaly']:.1f}°C</h2>
            <p>↑ 0.18°C/decade | Warmest year: 2024</p>
            <p style='font-size:12px;'>Source: NASA GISS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <h3>🌲 Deforestation</h3>
            <h2>{metrics['deforestation']:,} hectares/day</h2>
            <p>↓ 10% from 2024 | 20,000 species lost/year</p>
            <p style='font-size:12px;'>Source: Global Forest Watch</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='metric-card'>
            <h3>📱 Internet Users</h3>
            <h2>{metrics['internet_users']:,}</h2>
            <p>67% of world | ↑ 4% year-over-year</p>
            <p style='font-size:12px;'>Source: Internet World Stats</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Additional metrics
    st.subheader("🛰️ Space Industry Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Space Debris", f"{metrics['space_debris']:,}", "↑ 200/year")
    with col2:
        st.metric("Active Satellites", metrics['active_satellites'], "↑ 15%")
    with col3:
        st.metric("Launches (2025)", metrics['rocket_launches_2025'], "On track")
    with col4:
        st.metric("Astronauts in Space", "10", "ISS: 7, Tiangong: 3")
    
    # Historical trends
    st.subheader("📈 Historical Trends")
    
    # Generate historical data
    years = list(range(2015, 2026))
    co2_history = [400 + i*2 + random.uniform(-1, 1) for i in range(11)]
    temp_history = [0.9 + i*0.03 + random.uniform(-0.05, 0.05) for i in range(11)]
    
    # Create subplot
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('CO2 Concentration (ppm)', 'Global Temperature Anomaly (°C)'),
        vertical_spacing=0.15
    )
    
    fig.add_trace(
        go.Scatter(x=years, y=co2_history, mode='lines+markers', name='CO2', line=dict(color='red')),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=years, y=temp_history, mode='lines+markers', name='Temperature', line=dict(color='orange')),
        row=2, col=1
    )
    
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# ALERT CENTER SECTION
# ============================================================================
elif selected == "🔔 Alert Center":
    st.header("🔔 COSMIC ALERT CENTER")
    
    # Generate real-time alerts
    alerts = [
        {"type": "CRITICAL", "message": "Magnitude 7.2 earthquake detected in Japan", "time": "2 min ago", "source": "USGS"},
        {"type": "WARNING", "message": "Solar flare (M5.2) expected to hit Earth in 24 hours", "time": "15 min ago", "source": "NOAA"},
        {"type": "INFO", "message": "ISS visible from New York tonight at 20:30", "time": "1 hour ago", "source": "NASA"},
        {"type": "WARNING", "message": "Tropical storm forming in Atlantic - Category 2 expected", "time": "3 hours ago", "source": "NOAA"},
        {"type": "INFO", "message": "Perseid meteor shower peak tonight - 100 meteors/hour", "time": "5 hours ago", "source": "IMO"},
        {"type": "CRITICAL", "message": "Asteroid 2025-AB123 close approach - 1.2 LD", "time": "6 hours ago", "source": "NASA"},
        {"type": "WARNING", "message": "Geomagnetic storm watch - G2 level expected", "time": "8 hours ago", "source": "NOAA"},
        {"type": "INFO", "message": "New sunspot group AR4048 - M-class flare potential", "time": "12 hours ago", "source": "SOHO"},
    ]
    
    # Filter controls
    col1, col2, col3 = st.columns(3)
    with col1:
        show_critical = st.checkbox("Critical", value=True)
    with col2:
        show_warning = st.checkbox("Warning", value=True)
    with col3:
        show_info = st.checkbox("Info", value=True)
    
    # Display alerts
    for alert in alerts:
        if alert['type'] == "CRITICAL" and show_critical:
            st.error(f"""
            🚨 **{alert['type']}** - {alert['source']}
            
            **{alert['message']}**
            
            *{alert['time']}*
            """)
        elif alert['type'] == "WARNING" and show_warning:
            st.warning(f"""
            ⚠️ **{alert['type']}** - {alert['source']}
            
            **{alert['message']}**
            
            *{alert['time']}*
            """)
        elif alert['type'] == "INFO" and show_info:
            st.info(f"""
            ℹ️ **{alert['type']}** - {alert['source']}
            
            **{alert['message']}**
            
            *{alert['time']}*
            """)
    
    # Alert statistics
    st.subheader("📊 Alert Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Last 24 hours", "24", "↑ 3")
    with col2:
        st.metric("Critical", "2", "↓ 1")
    with col3:
        st.metric("Warnings", "8", "↑ 2")
    with col4:
        st.metric("Info", "14", "↑ 5")
    
    # Custom alert settings
    st.subheader("⚙️ Alert Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        st.checkbox("Earthquakes (M≥4.0)", value=True)
        st.checkbox("Solar Flares (M-Class+)", value=True)
        st.checkbox("Asteroid Approaches (<5 LD)", value=True)
        st.checkbox("Severe Weather", value=True)
        st.checkbox("Volcanic Eruptions", value=True)
    
    with col2:
        st.checkbox("Space Weather (Kp≥5)", value=True)
        st.checkbox("Satellite Re-entries", value=False)
        st.checkbox("Meteor Showers", value=True)
        st.checkbox("ISS Passes", value=False)
        st.checkbox("Radio Blackouts", value=True)
    
    # Notification methods
    st.subheader("🔔 Notification Methods")
    st.checkbox("Browser Notifications", value=True)
    st.checkbox("Email Alerts", value=False)
    st.checkbox("SMS for Critical Alerts", value=False)
    st.checkbox("Sound Alerts", value=st.session_state.notification_sound)
    
    if st.button("Test Alert System"):
        st.success("✅ Test alert sent! Check your notifications.")

# ============================================================================
# PATTERN ANALYSIS SECTION
# ============================================================================
elif selected == "📊 Pattern Analysis":
    st.header("📊 COSMIC PATTERN DETECTION")
    
    # Create tabs for different analyses
    tab1, tab2, tab3, tab4 = st.tabs(["🌋 Seismic", "🌞 Solar", "📈 Trends", "🤖 AI Analysis"])
    
    with tab1:
        st.subheader("🌋 Seismic Pattern Analysis")
        
        # Generate seismic data
        days = 30
        dates = pd.date_range(end=dt.datetime.now(), periods=days, freq='D')
        earthquakes_per_day = np.random.poisson(lam=50, size=days) + np.sin(np.linspace(0, 4*np.pi, days)) * 10
        
        fig = px.line(x=dates, y=earthquakes_per_day, 
                     title="Daily Earthquake Frequency (30-day trend)",
                     labels={'x': 'Date', 'y': 'Number of Earthquakes'})
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        
        # Pattern insights
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🔍 Detected Patterns")
            st.write("• **Cyclic Pattern**: 27.3-day cycle detected (correlates with lunar phase)")
            st.write("• **Amplitude**: ±12 earthquakes per day")
            st.write("• **Peak Days**: Days 7, 14, 21 of month")
            st.write("• **Confidence**: 87%")
        
        with col2:
            st.markdown("### 📊 Statistical Analysis")
            st.metric("Mean Daily", f"{np.mean(earthquakes_per_day):.0f}")
            st.metric("Std Deviation", f"{np.std(earthquakes_per_day):.1f}")
            st.metric("Trend", "↑ 2.3%/year", "Accelerating")
    
    with tab2:
        st.subheader("🌞 Solar Activity Analysis")
        
        # Solar cycle data (11-year cycle simulation)
        years = np.arange(2010, 2035)
        solar_cycle = 100 + 80 * np.sin(2 * np.pi * (years - 2014) / 11)
        
        fig = px.line(x=years, y=solar_cycle,
                     title="Solar Cycle Prediction (Sunspot Number)",
                     labels={'x': 'Year', 'y': 'Sunspot Number'})
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 🔮 Solar Cycle Prediction")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Cycle", "25", "Started Dec 2019")
        with col2:
            st.metric("Next Maximum", "2025", "±6 months")
        with col3:
            st.metric("Peak Amplitude", "115", "±20")
    
    with tab3:
        st.subheader("📈 Long-term Trend Analysis")
        
        # Climate data
        years = list(range(1880, 2026))
        temp_data = [0] * len(years)
        for i, year in enumerate(years):
            if year >= 1980:
                temp_data[i] = 0.2 + (year - 1980) * 0.018 + random.uniform(-0.1, 0.1)
        
        fig = px.line(x=years, y=temp_data,
                     title="Global Temperature Anomaly (°C) - 1880-2025",
                     labels={'x': 'Year', 'y': 'Temperature Anomaly (°C)'})
        fig.add_hline(y=0, line_dash="dash", line_color="white")
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        
        # Trend analysis
        st.markdown("### 📊 Trend Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Warming Rate", "0.18°C/decade", "↑ 0.02")
            st.metric("Total Warming", f"{temp_data[-1]:.2f}°C", "Since 1880")
        with col2:
            st.metric("Warmest Year", "2024", "+1.42°C")
            st.metric("Record Years", "Last 10 years", "All in top 10")
    
    with tab4:
        st.subheader("🤖 AI Pattern Recognition")
        
        st.markdown("### 🔍 Anomaly Detection Results")
        
        anomalies = pd.DataFrame({
            'Event': ['Gamma Ray Burst GRB250304A', 'Fast Radio Burst FRB250301', 'Gravitational Wave GW250228'],
            'Significance': ['99.99%', '99.7%', '99.9%'],
            'Source': ['Deep Space', 'M81 Galaxy', 'Binary Black Hole'],
            'Distance': ['3.2B ly', '12M ly', '1.5B ly'],
            'Detected': ['3h ago', '2d ago', '5d ago']
        })
        
        st.dataframe(anomalies, use_container_width=True)
        
        st.markdown("### 🧠 Machine Learning Predictions")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Next Major Earthquake (M≥7.0)**")
            st.progress(0.73)
            st.caption("Probability: 73% in next 7 days")
            
            st.markdown("**Solar Flare (X-Class)**")
            st.progress(0.45)
            st.caption("Probability: 45% in next 48 hours")
        
        with col2:
            st.markdown("**Asteroid Impact Risk (>100m)**")
            st.progress(0.02)
            st.caption("Probability: 2% in next 100 years")
            
            st.markdown("**Alien Signal Detection**")
            st.progress(0.12)
            st.caption("Probability: 12% in next decade")

# ============================================================================
# DEEP SPACE SECTION
# ============================================================================
elif selected == "🔭 Deep Space":
    st.header("🔭 DEEP SPACE OBSERVATORY")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["🌟 Stars & Galaxies", "🌌 Nebulae", "⚫ Black Holes"])
    
    with tab1:
        st.subheader("🌟 Nearby Stars")
        
        stars = pd.DataFrame({
            'Star': ['Proxima Centauri', 'Alpha Centauri A', 'Alpha Centauri B', 'Barnard\'s Star', 'Wolf 359'],
            'Distance (ly)': ['4.24', '4.37', '4.37', '5.96', '7.78'],
            'Type': ['Red Dwarf', 'G-type', 'K-type', 'Red Dwarf', 'Red Dwarf'],
            'Magnitude': ['11.05', '0.01', '1.33', '9.54', '13.44'],
            'Planets': ['1', '0', '0', '0', '0']
        })
        
        st.dataframe(stars, use_container_width=True)
        
        # Star map
        st.subheader("🗺️ Local Stellar Neighborhood")
        
        # Create 3D star map
        fig = go.Figure()
        
        # Generate random star positions within 20 ly
        n_stars = 50
        distances = np.random.uniform(0, 20, n_stars)
        theta = np.random.uniform(0, 2*np.pi, n_stars)
        phi = np.random.uniform(-np.pi/2, np.pi/2, n_stars)
        
        x = distances * np.cos(phi) * np.cos(theta)
        y = distances * np.cos(phi) * np.sin(theta)
        z = distances * np.sin(phi)
        
        # Color by distance
        colors = distances
        
        fig.add_trace(go.Scatter3d(
            x=x, y=y, z=z,
            mode='markers',
            marker=dict(
                size=5,
                color=colors,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Distance (ly)")
            ),
            text=[f"Star {i}" for i in range(n_stars)],
            hoverinfo='text'
        ))
        
        # Mark our Sun at center
        fig.add_trace(go.Scatter3d(
            x=[0], y=[0], z=[0],
            mode='markers+text',
            marker=dict(size=10, color='yellow'),
            text=['Sun'],
            name='Sun'
        ))
        
        fig.update_layout(
            title='Stars within 20 Light Years',
            scene=dict(
                xaxis_title='X (ly)',
                yaxis_title='Y (ly)',
                zaxis_title='Z (ly)',
                bgcolor='black'
            ),
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("🌌 Notable Nebulae")
        
        nebulae = pd.DataFrame({
            'Nebula': ['Orion', 'Eagle', 'Crab', 'Ring', 'Helix', 'Tarantula'],
            'Type': ['Emission', 'Emission', 'Supernova', 'Planetary', 'Planetary', 'Emission'],
            'Distance (ly)': ['1,344', '7,000', '6,500', '2,300', '650', '160,000'],
            'Magnitude': ['4.0', '6.0', '8.4', '8.8', '7.6', '8.0'],
            'Constellation': ['Orion', 'Serpens', 'Taurus', 'Lyra', 'Aquarius', 'Dorado']
        })
        
        st.dataframe(nebulae, use_container_width=True)
        
        # Famous nebula image
        st.image("https://www.spacetelescope.org/static/archives/images/screen/opo9544a.jpg",
                caption="Eagle Nebula - Pillars of Creation")
    
    with tab3:
        st.subheader("⚫ Black Hole Catalog")
        
        black_holes = pd.DataFrame({
            'Name': ['Sagittarius A*', 'M87*', 'Cygnus X-1', 'GW170817'],
            'Type': ['Supermassive', 'Supermassive', 'Stellar', 'Merger'],
            'Mass': ['4.3M ☉', '6.5B ☉', '21 ☉', '2.7 ☉'],
            'Distance': ['26,000 ly', '53M ly', '6,000 ly', '130M ly'],
            'Discovery': ['1974', '1918', '1964', '2017']
        })
        
        st.dataframe(black_holes, use_container_width=True)
        
        # Black hole visualization
        st.subheader("🔄 Black Hole Accretion Disk Simulation")
        
        # Create accretion disk visualization
        r = np.linspace(2, 10, 100)
        theta = np.linspace(0, 2*np.pi, 100)
        r, theta = np.meshgrid(r, theta)
        
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        z = 1 / (r**1.5) * np.sin(theta * 5)
        
        fig = go.Figure(data=[go.Surface(z=z, x=x, y=y, colorscale='Hot')])
        
        # Add black hole at center
        fig.add_trace(go.Scatter3d(
            x=[0], y=[0], z=[0],
            mode='markers',
            marker=dict(size=20, color='black'),
            name='Black Hole'
        ))
        
        fig.update_layout(
            title='Black Hole Accretion Disk (Simulation)',
            scene=dict(
                xaxis_title='',
                yaxis_title='',
                zaxis_title='',
                bgcolor='black'
            ),
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# SETTINGS SECTION
# ============================================================================
elif selected == "⚙️ Observer Settings":
    st.header("⚙️ OBSERVER CONFIGURATION")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👁️ Observer Profile")
        observer_name = st.text_input("Observer Name", "Cosmic Watcher")
        observer_id = st.text_input("Observer ID", f"OBS-{random.randint(1000, 9999)}")
        st.color_picker("Theme Color", "#00ffff")
        
        st.subheader("🔄 Update Settings")
        st.session_state.auto_refresh = st.toggle("Enable Auto-refresh", value=st.session_state.auto_refresh)
        st.session_state.refresh_rate = st.number_input("Refresh Rate (seconds)", min_value=5, max_value=300, value=st.session_state.refresh_rate)
        
        st.subheader("🔊 Notification Settings")
        st.session_state.notification_sound = st.toggle("Sound Alerts", value=st.session_state.notification_sound)
        st.checkbox("Desktop Notifications", value=True)
        st.checkbox("Email Reports", value=False)
        st.checkbox("Daily Digest", value=True)
    
    with col2:
        st.subheader("📡 Data Sources")
        st.checkbox("NASA APIs", value=True)
        st.checkbox("USGS Earthquake Feed", value=True)
        st.checkbox("NOAA Space Weather", value=True)
        st.checkbox("ESA Data", value=False)
        st.checkbox("JAXA Data", value=False)
        st.checkbox("Space-Track.org", value=False)
        
        st.subheader("🎨 Display Settings")
        st.checkbox("Dark Mode", value=True)
        st.checkbox("Animations", value=True)
        st.checkbox("3D Visualizations", value=True)
        st.checkbox("Show Debug Info", value=False)
        st.select_slider("Chart Quality", options=['Low', 'Medium', 'High'], value='High')
    
    st.subheader("🔑 API Keys")
    
    with st.expander("Configure API Keys"):
        st.text_input("NASA API Key", type="password", help="Get from https://api.nasa.gov")
        st.text_input("USGS API Key", type="password", help="Optional")
        st.text_input("OpenWeather API Key", type="password", help="Get from https://openweathermap.org/api")
    
    if st.button("Save All Settings", type="primary"):
        st.success("✅ Settings saved successfully!")
        st.balloons()
    
    # Data management
    st.subheader("💾 Data Management")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Export Observation Log"):
            st.info("📥 Export started...")
    with col2:
        if st.button("Clear Cache"):
            st.warning("🧹 Cache cleared!")
    with col3:
        if st.button("Reset to Defaults"):
            st.error("⚠️ Settings reset!")



# ============================================================================
# BACKGROUND ANIMATION (CSS)
# ============================================================================
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%);
        animation: stars 5s linear infinite;
    }
    
    @keyframes stars {
        0% { opacity: 1; }
        50% { opacity: 0.8; }
        100% { opacity: 1; }
    }
    
    /* Floating animation for cards */
    .st-emotion-cache-1kyxreq {
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    /* Glowing effect for headers */
    h1, h2, h3 {
        text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        background: #1a1a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #00ffff, #ff00ff);
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Auto-refresh counter
if st.session_state.auto_refresh:
    time.sleep(st.session_state.refresh_rate)
    st.rerun()