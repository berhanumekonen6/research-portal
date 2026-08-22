# ===================================================================
# ETHIOPIAN ACADEMIC PORTAL - RESEARCH COLLABORATION SYSTEM
# WITH ADMIN-APPROVED REGISTRATION & USER MANAGEMENT
# Berhanu Mekonen, PhD, Arba Minch University, June 25, 2026
# ===================================================================

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import re
import hashlib
import os
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import random
import time  # for celebration delays

st.set_page_config(
    page_title="Ethiopian Research Collaboration Portal",
    page_icon="🌿🇪🇹🎉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================================================================
# USER DATABASE - WITH ADMIN AND APPROVAL SYSTEM
# ===================================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

# ---- List of countries with flag emojis (simplified) ----
COUNTRIES_WITH_FLAGS = [
    "🇪🇹 Ethiopia", "🇰🇪 Kenya", "🇺🇬 Uganda", "🇹🇿 Tanzania", "🇷🇼 Rwanda",
    "🇸🇩 Sudan", "🇸🇸 South Sudan", "🇸🇴 Somalia", "🇩🇯 Djibouti", "🇪🇷 Eritrea",
    "🇺🇸 United States", "🇬🇧 United Kingdom", "🇨🇦 Canada", "🇦🇺 Australia",
    "🇩🇪 Germany", "🇫🇷 France", "🇮🇹 Italy", "🇪🇸 Spain", "🇵🇹 Portugal",
    "🇳🇱 Netherlands", "🇧🇪 Belgium", "🇨🇭 Switzerland", "🇸🇪 Sweden", "🇳🇴 Norway",
    "🇩🇰 Denmark", "🇫🇮 Finland", "🇮🇪 Ireland", "🇦🇹 Austria", "🇬🇷 Greece",
    "🇹🇷 Turkey", "🇮🇳 India", "🇨🇳 China", "🇯🇵 Japan", "🇰🇷 South Korea",
    "🇧🇷 Brazil", "🇿🇦 South Africa", "🇳🇬 Nigeria", "🇬🇭 Ghana", "🇰🇪 Kenya",
    "🇹🇿 Tanzania", "🇺🇬 Uganda", "🇷🇼 Rwanda", "🇸🇩 Sudan", "🇸🇸 South Sudan",
    "🇸🇴 Somalia", "🇩🇯 Djibouti", "🇪🇷 Eritrea", "🇲🇦 Morocco", "🇩🇿 Algeria",
    "🇹🇳 Tunisia", "🇱🇾 Libya", "🇪🇬 Egypt", "🇸🇦 Saudi Arabia", "🇦🇪 UAE",
    "🇶🇦 Qatar", "🇰🇼 Kuwait", "🇴🇲 Oman", "🇾🇪 Yemen", "🇯🇴 Jordan",
    "🇱🇧 Lebanon", "🇮🇱 Israel", "🇵🇸 Palestine", "🇮🇷 Iran", "🇮🇶 Iraq",
    "🇦🇫 Afghanistan", "🇵🇰 Pakistan", "🇧🇩 Bangladesh", "🇱🇰 Sri Lanka",
    "🇳🇵 Nepal", "🇧🇹 Bhutan", "🇲🇲 Myanmar", "🇹🇭 Thailand", "🇻🇳 Vietnam",
    "🇰🇭 Cambodia", "🇱🇦 Laos", "🇲🇾 Malaysia", "🇸🇬 Singapore", "🇵🇭 Philippines",
    "🇮🇩 Indonesia", "🇦🇺 Australia", "🇳🇿 New Zealand", "🇵🇬 Papua New Guinea",
    "🇫🇯 Fiji", "🇸🇧 Solomon Islands", "🇻🇺 Vanuatu", "🇼🇸 Samoa", "🇹🇴 Tonga"
]

# ---- Status options ----
STATUS_OPTIONS = [
    "PhD Student", "MSc Student", "BSc Student",
    "Assistant Professor", "Associate Professor", "Professor",
    "Lecturer", "Senior Lecturer", "Researcher", "Postdoctoral Researcher",
    "Other"
]

# ---- Department options (common Ethiopian universities) ----
DEPARTMENT_OPTIONS = [
    "Mathematics", "Applied Mathematics", "Statistics", "Computer Science",
    "Physics", "Chemistry", "Biology", "Biotechnology",
    "Civil Engineering", "Electrical Engineering", "Mechanical Engineering",
    "Chemical Engineering", "Industrial Engineering",
    "Economics", "Management", "Accounting", "Marketing",
    "Agriculture", "Animal Science", "Plant Science",
    "Public Health", "Medicine", "Pharmacy", "Nursing",
    "Law", "Political Science", "History", "Geography",
    "English", "Amharic", "Linguistics", "Journalism",
    "Education", "Psychology", "Sociology", "Anthropology",
    "Environmental Science", "Geology", "Meteorology",
    "Other"
]

# ---- Student level options ----
STUDENT_LEVEL_OPTIONS = ["Degree", "MSc", "PhD"]

def init_user_db():
    if 'user_db' not in st.session_state:
        # Default admin account
        st.session_state.user_db = {
            "admin": hash_password("admin")
        }
    if 'user_profiles' not in st.session_state:
        st.session_state.user_profiles = {
            "admin": {"name": "Administrator", "role": "admin"}
        }
    if 'pending_users' not in st.session_state:
        st.session_state.pending_users = []   # list of dicts with registration details
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    if 'notifications' not in st.session_state:
        st.session_state.notifications = []
    if 'forum_posts' not in st.session_state:
        st.session_state.forum_posts = []
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    if 'feedback' not in st.session_state:
        st.session_state.feedback = []
    if 'user_points' not in st.session_state:
        st.session_state.user_points = {}
    if 'user_badges' not in st.session_state:
        st.session_state.user_badges = {}
    if 'events' not in st.session_state:
        st.session_state.events = []
    if 'mentorships' not in st.session_state:
        st.session_state.mentorships = []
    if 'grants' not in st.session_state:
        st.session_state.grants = []
    if 'papers' not in st.session_state:
        st.session_state.papers = []
    if 'onboarding_complete' not in st.session_state:
        st.session_state.onboarding_complete = False
    if 'onboarding_step' not in st.session_state:
        st.session_state.onboarding_step = 1
    if 'show_about' not in st.session_state:
        st.session_state.show_about = False
    if 'requests' not in st.session_state:
        st.session_state.requests = []
    if 'selected_professor' not in st.session_state:
        st.session_state.selected_professor = None
    if 'show_letter' not in st.session_state:
        st.session_state.show_letter = False
    if 'last_request' not in st.session_state:
        st.session_state.last_request = None

def add_notification(message, notification_type="info", link=None):
    st.session_state.notifications.append({
        "id": len(st.session_state.notifications),
        "message": message,
        "type": notification_type,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "read": False,
        "link": link
    })

def add_points(username, points, action):
    if username not in st.session_state.user_points:
        st.session_state.user_points[username] = 0
    st.session_state.user_points[username] += points
    st.session_state.user_points[f"{username}_last_action"] = action
    add_notification(f"⭐ +{points} points for {action}!", "success")

def add_badge(username, badge_name):
    if username not in st.session_state.user_badges:
        st.session_state.user_badges[username] = []
    if badge_name not in st.session_state.user_badges[username]:
        st.session_state.user_badges[username].append(badge_name)
        add_notification(f"🏅 New badge earned: {badge_name}!", "success")

def login_user(username, password):
    init_user_db()
    if username not in st.session_state.user_db:
        return False, "❌ Username not found. Please register first."
    stored_hash = st.session_state.user_db[username]
    if verify_password(password, stored_hash):
        st.session_state.logged_in = True
        st.session_state.current_user = username
        profile = st.session_state.user_profiles.get(username, {})
        display_name = profile.get('name', username.split('@')[0].replace('.', ' ').title())
        add_notification(f"Welcome back, {display_name}!", "success")
        add_points(username, 5, "Daily login")
        # Celebration balloons for both admin and users
        st.balloons()
        time.sleep(0.5)  # give time for balloons to render
        return True, "✅ Login successful!"
    else:
        return False, "❌ Incorrect password. Please try again."

def logout_user():
    st.session_state.logged_in = False
    st.session_state.current_user = None

def is_admin():
    return st.session_state.get('current_user') == 'admin'

def request_registration(full_name, username, password, confirm_password, affiliation, status,
                         position, department, student_level, nationality, other_fields=""):
    """Submit a registration request for admin approval."""
    init_user_db()
    # Validate
    if not full_name.strip():
        return False, "❌ Full name is required."
    if not username.endswith("@amu.edu.et"):
        return False, "❌ Username must end with @amu.edu.et"
    if username in st.session_state.user_db:
        return False, "❌ Username already exists. Please choose a different one."
    if password != confirm_password:
        return False, "❌ Passwords do not match."
    if len(password) < 6:
        return False, "❌ Password must be at least 6 characters long."
    if not affiliation.strip():
        return False, "❌ Affiliation is required."
    if not status:
        return False, "❌ Please select a status."
    if not department:
        return False, "❌ Please select a department."
    if not nationality:
        return False, "❌ Please select a nationality."

    # Check if already pending
    for p in st.session_state.pending_users:
        if p['username'] == username:
            return False, "❌ Registration already pending. Please wait for admin approval."

    # Create pending request
    request = {
        "full_name": full_name.strip(),
        "username": username,
        "password_hash": hash_password(password),  # store hashed
        "affiliation": affiliation.strip(),
        "status": status,
        "position": position.strip() if position else "",
        "department": department,
        "student_level": student_level if student_level else "",
        "nationality": nationality,
        "other_fields": other_fields,
        "request_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "approved": False,
        "rejected": False
    }
    st.session_state.pending_users.append(request)
    add_notification(f"📝 New registration request from {full_name} ({username})", "info")
    return True, "✅ Registration request submitted! Please wait for admin approval."

def approve_user(request_index):
    """Admin approves a pending user and adds them to the user database."""
    if request_index >= len(st.session_state.pending_users):
        return False, "❌ Request not found."
    req = st.session_state.pending_users[request_index]
    if req['approved'] or req['rejected']:
        return False, "❌ Request already processed."

    username = req['username']
    # Add to user_db
    st.session_state.user_db[username] = req['password_hash']
    # Store profile
    st.session_state.user_profiles[username] = {
        "name": req['full_name'],
        "affiliation": req['affiliation'],
        "status": req['status'],
        "position": req['position'],
        "department": req['department'],
        "student_level": req['student_level'],
        "nationality": req['nationality'],
        "other_fields": req['other_fields'],
        "role": "user"   # regular user
    }
    # Mark as approved
    req['approved'] = True
    add_notification(f"✅ User {username} approved!", "success")
    return True, f"✅ User {username} approved successfully!"

def reject_user(request_index):
    if request_index >= len(st.session_state.pending_users):
        return False, "❌ Request not found."
    req = st.session_state.pending_users[request_index]
    if req['approved'] or req['rejected']:
        return False, "❌ Request already processed."
    req['rejected'] = True
    add_notification(f"❌ User {req['username']} registration rejected.", "warning")
    return True, f"❌ User {req['username']} rejected."

# ===================================================================
# CSS STYLES - (kept from original, with minor additions)
# ===================================================================

st.markdown("""
<style>
    :root {
        --primary: #1B5E20;
        --primary-light: #2E7D32;
        --primary-dark: #0D3B0D;
        --accent: #1A73E8;
        --accent-hover: #1557B0;
        --gold: #FFD700;
        --dark: #0a1a0a;
        --dark-card: #0f2a0f;
    }

    /* Global Styles - White Background */
    html, body, .stApp {
        font-size: 18px !important;
        line-height: 1.8 !important;
        background: #FFFFFF !important;
    }

    .stApp, .main, .block-container {
        background: #FFFFFF !important;
        color: #202124 !important;
    }

    /* All text - dark for readability on white */
    h1, h2, h3, h4, h5, h6, p, li, span, div, .stMarkdown, .stTextInput, .stSelectbox, .stButton {
        color: #202124 !important;
        font-weight: 500 !important;
    }

    /* Headings - Google Blue/Gradient */
    h1 {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #1A73E8, #4285F4, #34A853);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    h2 {
        font-size: 2.8rem !important;
        font-weight: 700 !important;
        color: #1A73E8 !important;
        border-bottom: 3px solid #E8F0FE;
        padding-bottom: 0.5rem;
    }
    h3 {
        font-size: 2.2rem !important;
        font-weight: 600 !important;
        color: #1A73E8 !important;
    }
    h4 {
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        color: #202124 !important;
    }

    p, li, .stMarkdown {
        font-size: 1.2rem !important;
        font-weight: 400 !important;
        line-height: 2 !important;
        color: #202124 !important;
    }

    /* LOGIN PAGE STYLES */
    .login-container {
        max-width: 600px;
        margin: 2rem auto;
        padding: 2.5rem;
        background: #FFFFFF !important;
        border: 1px solid #E8EAED;
        border-radius: 16px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.08);
    }

    .login-container h1 {
        text-align: center;
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem;
    }

    .login-container .login-subtitle {
        text-align: center;
        color: #5F6368 !important;
        font-size: 1.1rem !important;
        margin-bottom: 2rem;
    }

    .login-container .input-label {
        font-weight: 600 !important;
        color: #202124 !important;
        font-size: 1rem !important;
        display: block;
        margin-bottom: 0.3rem;
    }

    .login-container .input-hint {
        color: #5F6368 !important;
        font-size: 0.85rem !important;
        font-weight: 400 !important;
        display: block;
        margin-top: 0.2rem;
    }

    .login-btn {
        background: linear-gradient(135deg, #1A73E8, #4285F4) !important;
        color: #FFFFFF !important;
        border: none !important;
        padding: 0.9rem 2rem !important;
        border-radius: 30px !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        width: 100%;
        cursor: pointer !important;
        transition: all 0.3s !important;
        box-shadow: 0 2px 8px rgba(26,115,232,0.25) !important;
    }
    .login-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 16px rgba(26,115,232,0.35) !important;
    }

    .register-btn {
        background: linear-gradient(135deg, #34A853, #2D9249) !important;
        color: #FFFFFF !important;
        border: none !important;
        padding: 0.9rem 2rem !important;
        border-radius: 30px !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        width: 100%;
        cursor: pointer !important;
        transition: all 0.3s !important;
        box-shadow: 0 2px 8px rgba(52,168,83,0.25) !important;
    }
    .register-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 16px rgba(52,168,83,0.35) !important;
    }

    /* User info */
    .user-info {
        display: flex;
        align-items: center;
        gap: 15px;
        background: rgba(255, 255, 255, 0.9) !important;
        padding: 8px 20px;
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(10px);
    }

    .user-info .user-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: linear-gradient(135deg, #1A73E8, #4285F4);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #FFFFFF;
        font-weight: 700;
        font-size: 1.2rem;
    }

    .user-info .user-name {
        color: #202124 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }

    /* Main header */
    .main-header {
        background: linear-gradient(rgba(27, 94, 32, 0.65), rgba(13, 59, 13, 0.75)),
                    url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1200&h=400&fit=crop') !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        padding: 2rem 3rem 1.8rem 3rem !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 215, 0, 0.3) !important;
        margin-bottom: 1.5rem !important;
        box-shadow: 0 4px 30px rgba(0,0,0,0.1) !important;
        position: relative !important;
        overflow: hidden !important;
    }

    .main-header::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        background: linear-gradient(135deg, rgba(27, 94, 32, 0.3), rgba(13, 59, 13, 0.4)) !important;
        z-index: 0 !important;
    }

    .main-header .header-content {
        position: relative !important;
        z-index: 1 !important;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 20px;
    }

    .main-header .logo-section {
        display: flex;
        align-items: center;
        gap: 25px;
        flex: 1;
    }

    .main-header .logo-icon {
        width: 75px;
        height: 75px;
        background: rgba(255, 215, 0, 0.2) !important;
        border: 2px solid #FFD700 !important;
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.8rem;
        color: #FFFFFF;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        animation: pulse 3s infinite;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    .main-header .logo-text h1 {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
        background: none !important;
        -webkit-text-fill-color: #FFFFFF !important;
        margin: 0;
        text-shadow: 0 2px 30px rgba(0,0,0,0.3);
    }

    .main-header .logo-text .subtitle {
        color: rgba(255, 255, 255, 0.95) !important;
        font-size: 1.4rem !important;
        font-weight: 400 !important;
        margin: 5px 0 0 0;
        text-shadow: 0 1px 15px rgba(0,0,0,0.2);
    }

    .main-header .logo-text .subtitle .highlight {
        color: #FFD700 !important;
        font-weight: 600 !important;
    }

    .main-header .logo-text .developer-credit {
        color: rgba(255, 255, 255, 0.7) !important;
        font-size: 1rem !important;
        font-weight: 400 !important;
        margin: 8px 0 0 0;
        font-style: italic;
        letter-spacing: 0.5px;
        text-shadow: 0 1px 10px rgba(0,0,0,0.2);
    }

    .main-header .logo-text .developer-credit .highlight-name {
        color: #FFD700 !important;
        font-weight: 600 !important;
    }

    .main-header .logo-text .developer-credit .highlight-institution {
        color: #90EE90 !important;
        font-weight: 600 !important;
    }

    .main-header .header-right {
        display: flex;
        align-items: center;
        gap: 30px;
        flex-wrap: wrap;
    }

    .main-header .header-stats {
        display: flex;
        gap: 25px;
        flex-wrap: wrap;
        align-items: center;
    }

    .main-header .stat-item {
        background: rgba(255, 255, 255, 0.12) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 12px 22px;
        border-radius: 14px;
        text-align: center;
        min-width: 100px;
        transition: all 0.3s;
    }

    .main-header .stat-item:hover {
        border-color: #FFD700;
        transform: translateY(-2px);
        background: rgba(255, 255, 255, 0.2) !important;
    }

    .main-header .stat-item .number {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        color: #FFD700 !important;
        display: block;
    }

    .main-header .stat-item .label {
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        color: rgba(255, 255, 255, 0.8) !important;
        display: block;
        margin-top: 4px;
    }

    /* Research dropdown */
    .research-dropdown {
        position: relative;
        display: inline-block;
        margin-left: 5px;
        z-index: 9999;
    }

    .research-btn {
        background: rgba(255, 215, 0, 0.2) !important;
        backdrop-filter: blur(10px);
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 215, 0, 0.3) !important;
        padding: 12px 24px;
        border-radius: 30px;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.3s ease;
        display: inline-flex;
        align-items: center;
        gap: 10px;
        white-space: nowrap;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        letter-spacing: 0.3px;
        user-select: none;
    }

    .research-btn:hover {
        background: rgba(255, 215, 0, 0.35) !important;
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 4px 20px rgba(255, 215, 0, 0.2);
        color: #FFFFFF !important;
        border-color: #FFD700 !important;
    }

    .research-btn .arrow-down {
        display: inline-block;
        transition: transform 0.3s ease;
        font-size: 0.8rem;
        color: rgba(255,255,255,0.8);
    }

    .research-dropdown:hover .arrow-down {
        transform: rotate(180deg);
    }

    .research-dropdown-content {
        display: none;
        position: absolute;
        left: 0;
        bottom: 100%;
        background: #FFFFFF !important;
        min-width: 400px;
        max-width: 90vw;
        max-height: 350px;
        overflow-y: auto;
        border: 1px solid #E8EAED;
        border-radius: 16px;
        padding: 1.2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.12);
        z-index: 1000;
        margin-bottom: 10px;
    }

    .research-dropdown:hover .research-dropdown-content {
        display: block;
    }

    @media (max-width: 768px) {
        .research-dropdown-content {
            left: auto;
            right: 0;
            min-width: 280px;
            max-width: 85vw;
        }
    }

    .research-dropdown-content .dropdown-title {
        color: #1A73E8 !important;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 12px;
        border-bottom: 1px solid #E8EAED;
        padding-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
        position: sticky;
        top: 0;
        background: #FFFFFF;
        z-index: 2;
    }

    .research-dropdown-content .link-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 14px;
        border-radius: 10px;
        transition: all 0.3s ease;
        text-decoration: none;
        color: #202124 !important;
        font-size: 1rem;
        font-weight: 500 !important;
        cursor: pointer;
    }

    .research-dropdown-content .link-item:hover {
        background: #E8F0FE !important;
        transform: translateX(5px);
    }

    .research-dropdown-content .link-item .link-icon {
        font-size: 1.2rem;
        flex-shrink: 0;
    }

    .research-dropdown-content .link-item .link-text {
        flex: 1;
        color: #202124 !important;
    }

    .research-dropdown-content .link-item .link-url {
        color: #5F6368 !important;
        font-size: 0.7rem;
        font-family: monospace;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 100px;
    }

    .research-dropdown-content .link-item .link-arrow {
        color: #1A73E8 !important;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }

    .research-dropdown-content .link-item:hover .link-arrow {
        transform: translateX(4px);
    }

    .research-dropdown-content .divider {
        border: none;
        border-top: 1px solid #E8EAED;
        margin: 4px 0;
    }

    .ethiopian-stripe {
        height: 5px;
        background: linear-gradient(to right, #078930, #FCDD09, #DA121A);
        border-radius: 3px;
        margin: 12px 0 0 0;
    }

    /* Status bar */
    .status-bar {
        background: #F8F9FA !important;
        border: 1px solid #E8EAED;
        border-radius: 16px;
        padding: 1.2rem 2.5rem;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 15px;
    }

    .status-bar .status-dot {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        display: inline-block;
        animation: blink 2s infinite;
    }

    .status-bar .status-dot.online {
        background: #34A853;
        box-shadow: 0 0 20px rgba(52,168,83,0.3);
    }

    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    .status-bar .status-text {
        color: #202124 !important;
        font-size: 1.2rem !important;
        font-weight: 500 !important;
    }

    .status-bar .status-text .highlight-green {
        color: #34A853 !important;
        font-weight: 700 !important;
    }

    .status-bar .live-badge {
        background: linear-gradient(135deg, #1A73E8, #4285F4);
        color: #FFFFFF !important;
        padding: 6px 18px;
        border-radius: 25px;
        font-size: 1rem !important;
        font-weight: 600 !important;
        border: none;
    }

    /* Professor card */
    .professor-card {
        background: #FFFFFF !important;
        border: 1px solid #E8EAED !important;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }

    .professor-card:hover {
        transform: translateY(-4px);
        border-color: #1A73E8 !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
    }

    .badge-available {
        background: #E6F4EA !important;
        color: #34A853 !important;
        border: 1px solid #34A853;
        padding: 6px 18px;
        border-radius: 25px;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }

    .badge-full {
        background: #FCE8E6 !important;
        color: #EA4335 !important;
        border: 1px solid #EA4335;
        padding: 6px 18px;
        border-radius: 25px;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }

    .badge-verified {
        display: inline-block;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        margin: 2px 4px 2px 0;
        background: #E8F0FE !important;
        color: #1A73E8 !important;
        border: 1px solid #1A73E8;
    }

    .badge-collab {
        background: #E8F0FE !important;
        color: #1A73E8 !important;
        border: 1px solid #1A73E8;
        padding: 4px 14px;
        border-radius: 25px;
        display: inline-block;
        margin: 2px 4px 2px 0;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }

    .social-links {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin: 10px 0;
    }

    .social-link {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 16px;
        border-radius: 25px;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        text-decoration: none !important;
        transition: all 0.3s ease;
        border: 1px solid #E8EAED;
        color: #202124 !important;
    }

    .social-link-orcid {
        background: #E8F0FE !important;
        color: #1A73E8 !important;
        border-color: #1A73E8;
    }

    .social-link-researchgate {
        background: #E6F4EA !important;
        color: #34A853 !important;
        border-color: #34A853;
    }

    .social-link-scholar {
        background: #FCE8E6 !important;
        color: #EA4335 !important;
        border-color: #EA4335;
    }

    .social-link-scopus {
        background: #FFF3E0 !important;
        color: #FB8C00 !important;
        border-color: #FB8C00;
    }

    /* Notification & chat styles (kept from original) */
    .notification-item {
        padding: 0.75rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        border-left: 4px solid #1A73E8;
        background: #F8F9FA;
    }

    .notification-item.unread {
        background: #E8F0FE;
        border-left-color: #EA4335;
    }

    .notification-item .notification-time {
        color: #5F6368 !important;
        font-size: 0.8rem !important;
    }

    .chat-message {
        padding: 0.75rem 1rem;
        border-radius: 12px;
        margin-bottom: 0.5rem;
        max-width: 80%;
    }

    .chat-message.user {
        background: #E8F0FE !important;
        border: 1px solid #1A73E8;
        margin-left: auto;
    }

    .chat-message.other {
        background: #F8F9FA !important;
        border: 1px solid #E8EAED;
    }

    .chat-message .chat-author {
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        color: #1A73E8 !important;
    }

    .chat-message .chat-time {
        color: #5F6368 !important;
        font-size: 0.7rem !important;
    }

    .badge-display {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin: 10px 0;
    }

    .badge-item {
        background: #E8F0FE !important;
        border: 1px solid #1A73E8;
        border-radius: 30px;
        padding: 4px 16px;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        color: #1A73E8 !important;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    .badge-item.gold {
        background: #FFF8E1 !important;
        border-color: #FFD700;
        color: #F9A825 !important;
    }

    .feedback-item {
        background: #FFFFFF !important;
        border: 1px solid #E8EAED;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    .feedback-item .feedback-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }

    .feedback-item .feedback-rating {
        color: #FFD700;
        font-size: 1.2rem;
    }

    .dashboard-card {
        background: #FFFFFF !important;
        border: 1px solid #E8EAED;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s;
    }

    .dashboard-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.06);
        border-color: #1A73E8;
    }

    .dashboard-card .card-value {
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        color: #1A73E8 !important;
    }

    .dashboard-card .card-label {
        color: #5F6368 !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
    }

    .stButton > button {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        padding: 0.9rem 2.2rem !important;
        background: linear-gradient(135deg, #1A73E8, #4285F4) !important;
        color: white !important;
        border-radius: 30px !important;
        border: none !important;
        width: 100%;
        transition: all 0.3s !important;
        box-shadow: 0 2px 8px rgba(26,115,232,0.25) !important;
        min-height: 55px !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 4px 16px rgba(26,115,232,0.35) !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: #F8F9FA !important;
        border-radius: 16px;
        padding: 8px;
        border: 1px solid #E8EAED;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 14px 30px;
        color: #5F6368 !important;
        font-weight: 500 !important;
        font-size: 1.1rem !important;
    }

    .stTabs [aria-selected="true"] {
        background: #FFFFFF !important;
        color: #1A73E8 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
        border: 1px solid #E8EAED;
    }

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > input {
        background: #FFFFFF !important;
        border: 1px solid #DADCE0 !important;
        border-radius: 12px !important;
        color: #202124 !important;
        padding: 14px 20px !important;
        font-size: 1.15rem !important;
        font-weight: 400 !important;
        min-height: 55px !important;
        transition: all 0.3s !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #1A73E8 !important;
        box-shadow: 0 0 0 3px rgba(26,115,232,0.15) !important;
    }

    .search-section {
        background: #F8F9FA !important;
        border: 1px solid #E8EAED;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
    }

    .about-section {
        background: #FFFFFF !important;
        border: 1px solid #E8EAED;
        border-radius: 16px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 24px rgba(0,0,0,0.04);
    }

    .about-section h2 {
        font-size: 2.5rem !important;
        color: #1A73E8 !important;
        margin-top: 2rem;
        border-bottom: 3px solid #E8F0FE;
        padding-bottom: 0.5rem;
        font-weight: 700 !important;
    }

    .about-section h3 {
        font-size: 1.8rem !important;
        color: #1A73E8 !important;
        margin-top: 1.5rem;
        font-weight: 600 !important;
    }

    .about-section .stat-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin: 1.5rem 0;
    }

    .about-section .stat-card {
        background: #F8F9FA !important;
        border: 1px solid #E8EAED;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s;
    }

    .about-section .stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-color: #1A73E8;
    }

    .about-section .stat-card .number {
        font-size: 3rem !important;
        font-weight: 800 !important;
        color: #1A73E8 !important;
        display: block;
    }

    .about-section .stat-card .label {
        font-size: 1.1rem !important;
        color: #5F6368 !important;
        font-weight: 500 !important;
    }

    .about-section .quote {
        font-style: italic;
        font-size: 1.4rem !important;
        font-weight: 500 !important;
        color: #1A73E8 !important;
        text-align: center;
        padding: 1.5rem;
        margin: 2rem 0;
        border-top: 1px solid #E8EAED;
        border-bottom: 1px solid #E8EAED;
    }

    .about-section .footer-credit {
        text-align: center;
        margin-top: 2.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid #E8EAED;
        color: #5F6368 !important;
        font-size: 1rem !important;
        font-weight: 400 !important;
    }

    .letter-box {
        background: #FFFFFF !important;
        border: 2px solid #E8EAED;
        border-radius: 16px;
        padding: 3rem;
        font-family: 'Times New Roman', serif;
        line-height: 2;
        margin: 1.5rem 0;
        color: #202124 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        font-size: 1.2rem !important;
    }

    .letter-box h2 {
        text-align: center;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #1A73E8 !important;
        -webkit-text-fill-color: #1A73E8 !important;
    }

    .letter-box .date {
        text-align: right;
        font-size: 1.1rem !important;
        color: #5F6368 !important;
    }

    .letter-box .signature {
        margin-top: 3rem;
        border-top: 1px solid #E8EAED;
        padding-top: 2rem;
    }

    .css-1d391kg, .css-12w0qpk, [data-testid="stSidebar"] {
        background: #F8F9FA !important;
        border-right: 1px solid #E8EAED !important;
    }
</style>
""", unsafe_allow_html=True)

# ===================================================================
# RESEARCHER PROFILES - ALL 8 RESEARCHERS (unchanged, omitted for brevity)
# ===================================================================

# (All 8 researcher profiles are kept exactly as in the original code.
# To save space, they are omitted here but must be included in the final file.)

# ===================================================================
# HELPER FUNCTIONS (original, unchanged)
# ===================================================================

def create_forum_post(title, content, author, tags=[]):
    # ... (same as before)
    pass

def add_comment_to_post(post_id, author, content):
    # ... (same as before)
    pass

def like_post(post_id):
    # ... (same as before)
    pass

def show_notification_center():
    # ... (same as before)
    pass

def show_onboarding():
    # ... (same as before)
    pass

def show_event_calendar():
    # ... (same as before)
    pass

def show_grants():
    # ... (same as before)
    pass

def show_researcher_of_month():
    # ... (same as before)
    pass

def show_chat():
    # ... (same as before)
    pass

def show_about_page():
    # ... (same as before)
    pass

# ===================================================================
# LOAD DATA, SEARCH, LETTER GENERATION
# ===================================================================

@st.cache_data
def load_data():
    # ... (same as before)
    pass

def search_academicians(academicians_df, search_query, search_type):
    # ... (same as before)
    pass

def generate_request_letter(student_name, student_institution, professor_name, professor_title,
                           professor_institution, research_topic, request_type,
                           student_email, student_phone):
    # ... (same as before)
    pass

# ===================================================================
# LOGIN PAGE (Modified with Registration Request)
# ===================================================================

def show_login_page():
    init_user_db()
    st.markdown("""
    <div style="text-align:center; padding:1rem 0;">
        <div style="font-size:4rem; margin-bottom:0.5rem;">🌿🇪🇹🎉</div>
        <h1 style="font-size:3rem; margin:0;">Research Collaboration Portal</h1>
        <p style="color:#5F6368; font-size:1.2rem; margin-top:0.5rem;">Sign in to access the Ethiopian Research Network</p>
        <p style="color:#5F6368; font-size:1rem; margin-top:0.3rem;">Please register first if you don't have an account</p>
    </div>
    """, unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Request Registration"])
    with tab1:
        with st.container():
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            with st.form("login_form"):
                username = st.text_input("📧 Email Address", placeholder="your.name@amu.edu.et", help="Use your AMU email address")
                password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    submitted = st.form_submit_button("Sign In", use_container_width=True)
                if submitted:
                    if not username or not password:
                        st.error("❌ Please enter both username and password.")
                    else:
                        # Check if user exists and is approved
                        if username in st.session_state.user_db:
                            success, message = login_user(username, password)
                            if success:
                                st.success(message)
                                # Balloons already triggered in login_user; wait a moment then rerun
                                time.sleep(1)  # allow balloons to show
                                st.rerun()
                            else:
                                st.error(message)
                        else:
                            # Check if pending
                            pending = [p for p in st.session_state.pending_users if p['username'] == username]
                            if pending:
                                if pending[0]['rejected']:
                                    st.error("❌ Your registration request was rejected by the admin.")
                                elif pending[0]['approved']:
                                    st.success("✅ Your request was approved! Please login.")
                                else:
                                    st.warning("⏳ Your registration request is pending admin approval. Please wait.")
                            else:
                                st.error("❌ Username not found. Please register first.")
            st.markdown("""
            <div style="text-align:center; margin-top:1.5rem; padding-top:1rem; border-top:1px solid #E8EAED;">
                <p style="color:#5F6368; font-size:0.9rem; margin:0;">
                    📧 For support, contact: <b style="color:#1A73E8;">berhanu.mekonen@amu.edu.et</b>
                </p>
                <p style="color:#5F6368; font-size:0.9rem; margin:0;">
                    📞 Phone: <b style="color:#1A73E8;">+251 905 527 481</b>
                </p>
                <p style="color:#5F6368; font-size:0.85rem; margin-top:0.5rem;">
                    ⚠️ Admin: username <b>admin</b> password <b>admin</b>
                </p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    with tab2:
        with st.container():
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            st.markdown("""
            <div style="text-align:center; margin-bottom:1.5rem;">
                <h3 style="margin:0; color:#1A73E8;">Request Account</h3>
                <p style="color:#5F6368; font-size:0.95rem;">Fill in the details below. Admin will review and approve.</p>
            </div>
            """, unsafe_allow_html=True)
            with st.form("registration_request_form"):
                full_name = st.text_input("👤 Full Name *", placeholder="e.g., Berhanu Mekonen")
                username = st.text_input("📧 Email Address (username) *", placeholder="your.name@amu.edu.et", help="Must end with @amu.edu.et")
                password = st.text_input("🔒 Create Password *", type="password", placeholder="Minimum 6 characters", help="Password must be at least 6 characters long")
                confirm_password = st.text_input("✅ Confirm Password *", type="password", placeholder="Re-enter your password")
                affiliation = st.text_input("🏛️ Affiliation / Institution *", placeholder="e.g., Arba Minch University")
                status = st.selectbox("📌 Current Status *", STATUS_OPTIONS)
                position = st.text_input("💼 Position (if any)", placeholder="e.g., Head of Department, Dean")
                department = st.selectbox("📚 Department *", DEPARTMENT_OPTIONS)
                student_level = st.selectbox("🎓 Student Level (if student)", [""] + STUDENT_LEVEL_OPTIONS)
                nationality = st.selectbox("🌍 Nationality *", COUNTRIES_WITH_FLAGS)
                other_fields = st.text_area("📝 Additional Information (optional)", placeholder="Any other details you'd like to share...")

                if st.form_submit_button("Submit Request", use_container_width=True):
                    success, message = request_registration(
                        full_name, username, password, confirm_password,
                        affiliation, status, position, department, student_level, nationality, other_fields
                    )
                    if success:
                        st.success(message)
                        st.balloons()
                        time.sleep(0.5)
                    else:
                        st.error(message)
            st.markdown('</div>', unsafe_allow_html=True)

# ===================================================================
# ADMIN PANEL (New)
# ===================================================================

def show_admin_panel():
    st.markdown("### 👨‍💼 Admin Dashboard")
    st.markdown("Welcome, Administrator! Here you can manage user registrations and view system stats.")

    # Pending registrations
    pending = [p for p in st.session_state.pending_users if not p['approved'] and not p['rejected']]
    if pending:
        st.markdown(f"#### 📌 Pending Registration Requests ({len(pending)})")
        for i, req in enumerate(pending):
            with st.expander(f"Request from {req['full_name']} ({req['username']}) - {req['request_date']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                    **Full Name:** {req['full_name']}  
                    **Username:** {req['username']}  
                    **Affiliation:** {req['affiliation']}  
                    **Status:** {req['status']}  
                    **Position:** {req.get('position', 'N/A')}  
                    **Department:** {req['department']}  
                    """)
                with col2:
                    st.markdown(f"""
                    **Student Level:** {req.get('student_level', 'N/A')}  
                    **Nationality:** {req['nationality']}  
                    **Request Date:** {req['request_date']}  
                    **Additional Info:** {req.get('other_fields', 'None')}  
                    """)
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button(f"✅ Approve", key=f"approve_{i}"):
                        success, msg = approve_user(i)
                        if success:
                            st.success(msg)
                            st.balloons()
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error(msg)
                with col_b:
                    if st.button(f"❌ Reject", key=f"reject_{i}"):
                        success, msg = reject_user(i)
                        if success:
                            st.warning(msg)
                            st.rerun()
                        else:
                            st.error(msg)
    else:
        st.info("No pending registration requests.")

    # Approved and rejected users stats
    approved = [p for p in st.session_state.pending_users if p.get('approved')]
    rejected = [p for p in st.session_state.pending_users if p.get('rejected')]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Registered Users", len(st.session_state.user_db) - 1)  # exclude admin
    col2.metric("Pending Requests", len(pending))
    col3.metric("Approved", len(approved))
    col4.metric("Rejected", len(rejected))

    # List of all users
    st.markdown("#### 👥 All Approved Users")
    users = [u for u in st.session_state.user_db.keys() if u != 'admin']
    if users:
        df_users = pd.DataFrame({
            "Username": users,
            "Name": [st.session_state.user_profiles.get(u, {}).get('name', 'N/A') for u in users],
            "Affiliation": [st.session_state.user_profiles.get(u, {}).get('affiliation', 'N/A') for u in users],
            "Status": [st.session_state.user_profiles.get(u, {}).get('status', 'N/A') for u in users]
        })
        st.dataframe(df_users, use_container_width=True)
    else:
        st.info("No approved users yet.")

# ===================================================================
# MAIN APPLICATION (Modified with Admin routing and balloon fix)
# ===================================================================

def main():
    init_user_db()
    if not st.session_state.logged_in:
        show_login_page()
        return

    academicians_df, students_df = load_data()
    if 'requests' not in st.session_state:
        st.session_state.requests = []
    if 'selected_professor' not in st.session_state:
        st.session_state.selected_professor = None
    if 'show_letter' not in st.session_state:
        st.session_state.show_letter = False
    if 'last_request' not in st.session_state:
        st.session_state.last_request = None
    if 'show_about' not in st.session_state:
        st.session_state.show_about = False

    current_user = st.session_state.current_user
    profile = st.session_state.user_profiles.get(current_user, {})
    user_display_name = profile.get('name', current_user.split('@')[0].replace('.', ' ').title())
    is_admin = (current_user == 'admin')

    # SIDEBAR
    with st.sidebar:
        st.markdown("### Research Portal")
        st.markdown("---")
        st.markdown(f"""
        <div style="background:#E8F0FE;padding:1rem;border-radius:12px;margin-bottom:1rem;">
            <p style="margin:0;font-weight:600;color:#1A73E8;">👤 {user_display_name}</p>
            <p style="margin:0;font-size:0.85rem;color:#5F6368;">{current_user}</p>
            <p style="margin:0;font-size:0.85rem;color:#5F6368;">⭐ Points: {st.session_state.user_points.get(current_user, 0)}</p>
            <div class="badge-display">
                {''.join(f'<span class="badge-item">🏅 {b}</span>' for b in st.session_state.user_badges.get(current_user, []))}
            </div>
        </div>
        """, unsafe_allow_html=True)

        unread = len([n for n in st.session_state.notifications if not n.get('read', False)])

        # Navigation options (admin gets extra)
        if is_admin:
            nav_options = [
                "👑 Admin Dashboard",
                "🏠 Home",
                "🔍 Find Researchers",
                "💬 Forum",
                "📊 Analytics",
                "📋 My Requests",
                "💬 Chat",
                "📅 Events",
                "💰 Grants",
                "👥 Mentorship",
                "📄 Papers",
                "📝 Feedback",
                "👤 Profile"
            ]
        else:
            nav_options = [
                "🏠 Home",
                "🔍 Find Researchers",
                "💬 Forum",
                "📊 Analytics",
                "📋 My Requests",
                "💬 Chat",
                "📅 Events",
                "💰 Grants",
                "👥 Mentorship",
                "📄 Papers",
                "📝 Feedback",
                "👤 Profile"
            ]
        if unread > 0:
            nav_options.append(f"📨 Notifications <span class='notification-badge'>{unread}</span>")
        else:
            nav_options.append("📨 Notifications")
        selected_page = st.radio("Navigation", nav_options, index=0)
        st.session_state.current_page = selected_page

        if st.button("🚪 Logout", use_container_width=True):
            logout_user()
            st.rerun()
        st.markdown("---")
        if st.button("About This Portal", use_container_width=True):
            st.session_state.show_about = True
            st.rerun()
        st.markdown("---")
        st.markdown("Connecting Ethiopian Researchers")
        st.markdown("*Berhanu Mekonen, PhD, Arba Minch University, June 25, 2026*")

    if st.session_state.show_about:
        show_about_page()
        return

    current_page = getattr(st.session_state, 'current_page', "🏠 Home")

    # HEADER WITH STATS
    available_profs = len(academicians_df[academicians_df['available_for_collaboration'] == True])
    total_publications = sum([len(p.get('publications', [])) for _, p in academicians_df.iterrows()])
    total_completed_phds = sum([p.get('completed_phds', 0) for _, p in academicians_df.iterrows()])

    st.markdown(f"""
    <div class="main-header">
        <div class="header-content">
            <div class="logo-section">
                <div class="logo-icon">🌿🇪🇹🎉</div>
                <div class="logo-text">
                    <h1>Ethiopian Research Collaboration Portal</h1>
                    <div class="subtitle">
                        Connecting <span class="highlight">Ethiopian</span> Researchers & Academic Professionals
                    </div>
                    <div class="developer-credit">
                        🌿🇪🇹🎉 <span class="highlight-name">Berhanu Mekonen, PhD</span> ·
                        <span class="highlight-institution">Arba Minch University</span> ·
                        June 25, 2026
                    </div>
                </div>
            </div>
            <div class="header-right">
                <div class="user-info">
                    <div class="user-avatar">{user_display_name[0]}</div>
                    <span class="user-name">{user_display_name}</span>
                </div>
                <div class="header-stats">
                    <div class="stat-item">
                        <span class="number">{len(academicians_df)}</span>
                        <span class="label">Verified Professionals</span>
                    </div>
                    <div class="stat-item">
                        <span class="number">{available_profs}</span>
                        <span class="label">Available</span>
                    </div>
                    <div class="stat-item">
                        <span class="number">{len(students_df)}</span>
                        <span class="label">Student Researchers</span>
                    </div>
                    <div class="stat-item">
                        <span class="number">{total_publications}</span>
                        <span class="label">Publications</span>
                    </div>
                    <div class="stat-item">
                        <span class="number">{total_completed_phds}</span>
                        <span class="label">PhDs Completed</span>
                    </div>
                </div>
                <div class="research-dropdown">
                    <button class="research-btn">
                        🌍 Researches in the world 🎉<span class="arrow-down">▼</span>
                    </button>
                    <div class="research-dropdown-content">
                        <div class="dropdown-title">📚 Research Resources</div>
                        <a href="https://scholar.google.com/" target="_blank" class="link-item">
                            <span class="link-icon">🔬</span>
                            <span class="link-text">Google Scholar</span>
                            <span class="link-url">scholar.google.com</span>
                            <span class="link-arrow">→</span>
                        </a>
                        <hr class="divider">
                        <a href="https://www.scimagojr.com/" target="_blank" class="link-item">
                            <span class="link-icon">📊</span>
                            <span class="link-text">Check Scopus Indexed or not</span>
                            <span class="link-url">scimagojr.com</span>
                            <span class="link-arrow">→</span>
                        </a>
                        <hr class="divider">
                        <a href="https://mjl.clarivate.com/home" target="_blank" class="link-item">
                            <span class="link-icon">📋</span>
                            <span class="link-text">Check Web of Science Indexed or not</span>
                            <span class="link-url">mjl.clarivate.com</span>
                            <span class="link-arrow">→</span>
                        </a>
                    </div>
                </div>
            </div>
        </div>
        <div class="ethiopian-stripe"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="status-bar">
        <div>
            <span class="status-dot online"></span>
            <span class="status-text">System Online · <span class="highlight-green">{len(academicians_df)}</span> verified professionals ready for collaboration</span>
        </div>
        <div>
            <span class="live-badge">LIVE · {datetime.now().strftime('%H:%M:%S')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ===================================================================
    # PAGE ROUTING
    # ===================================================================

    if current_page == "👑 Admin Dashboard" and is_admin:
        show_admin_panel()
        return

    if current_page == "🏠 Home" or current_page == "🔍 Find Researchers":
        if current_page == "🏠 Home":
            show_researcher_of_month()
            st.markdown("---")
        st.markdown("### Find Academic Professionals")
        with st.container():
            st.markdown('<div class="search-section">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 1.5, 0.8])
            with col1:
                prof_search_type = st.selectbox("Search by:", ["All Fields", "Name", "Research Area", "Institution", "Keyword"])
            with col2:
                prof_search_query = st.text_input("Enter search term:", placeholder="e.g., mathematics, queuing...")
            with col3:
                show_available_only = st.checkbox("Available Only", value=True)
            st.markdown('</div>', unsafe_allow_html=True)

        filtered_profs = search_academicians(academicians_df, prof_search_query, prof_search_type)
        if show_available_only:
            filtered_profs = filtered_profs[filtered_profs['available_for_collaboration'] == True]
        st.caption(f"Found {len(filtered_profs)} verified professional(s)")

        for _, prof in filtered_profs.iterrows():
            slots = prof['supervisory_capacity'] - prof['current_students']
            status_class = "badge-available" if slots > 0 else "badge-full"
            status_text = f"{slots} slots available" if slots > 0 else "Fully booked"
            with st.expander(f"{prof['profile_image']} {prof['name']} - {prof['title']}", expanded=False):
                col1, col2 = st.columns([2, 1])
                with col1:
                    verification_html = ""
                    for badge in prof.get('verification_badges', []):
                        verification_html += f'<span class="badge-verified">{badge}</span>'
                    social_links_html = ""
                    if prof.get('orcid_url'):
                        social_links_html += f'<a href="{prof["orcid_url"]}" target="_blank" class="social-link social-link-orcid">ORCID</a>'
                    if prof.get('researchgate_url'):
                        social_links_html += f'<a href="{prof["researchgate_url"]}" target="_blank" class="social-link social-link-researchgate">ResearchGate</a>'
                    if prof.get('google_scholar_url'):
                        social_links_html += f'<a href="{prof["google_scholar_url"]}" target="_blank" class="social-link social-link-scholar">Google Scholar</a>'
                    if prof.get('scopus_url'):
                        social_links_html += f'<a href="{prof["scopus_url"]}" target="_blank" class="social-link social-link-scopus">Scopus</a>'
                    if social_links_html:
                        social_links_html = f'<div class="social-links">{social_links_html}</div>'
                    st.markdown(f"""
                    <div class="professor-card">
                        <div class="card-header">
                            <div>
                                <h3>{prof['profile_image']} {prof['name']}</h3>
                                <span class="title-badge">{prof['title']}</span>
                                <div style="margin-top:8px;">{verification_html}</div>
                                {social_links_html}
                            </div>
                            <div>
                                <span class="{status_class}">{status_text}</span>
                                <br>
                                <span style="color:#FBBC04;">⭐ Trust Score: {prof['trust_score']}%</span>
                            </div>
                        </div>
                        <div>
                            <p><b>🏛️ Institution:</b> {prof['institution']}</p>
                            <p><b>📚 Department:</b> {prof['department']}</p>
                            <p><b>🎓 Education:</b> {prof['education']}</p>
                            <p><b>🔬 Research Interests:</b> {prof['research_interests']}</p>
                            <div>
                                {''.join(f'<span class="badge-collab">{t}</span>' for t in prof.get('collaboration_types', []))}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if prof.get('publications'):
                        with st.expander("📄 Publications"):
                            for pub in prof['publications']:
                                st.write(f"• {pub}")
                with col2:
                    st.markdown(f"""
                    <div style="background:#F8F9FA;border:1px solid #E8EAED;border-radius:12px;padding:1.5rem;">
                        <h4 style="color:#202124;">📬 Contact</h4>
                        <p style="color:#202124;">✉️ {prof['email']}</p>
                        <p style="color:#202124;">📞 {prof['phone']}</p>
                        <p style="color:#202124;">📊 Completed PhDs: <span style="color:#1A73E8;font-weight:700;">{prof['completed_phds']}</span></p>
                        <p style="color:#202124;">📋 Available Slots: <span style="color:#1A73E8;font-weight:700;">{slots}</span></p>
                        <p style="color:#202124;">📈 h-index: <span style="color:#1A73E8;font-weight:700;">{prof['h_index']}</span> | 📑 Citations: <span style="color:#1A73E8;font-weight:700;">{prof['total_citations']}</span></p>
                    </div>
                    """, unsafe_allow_html=True)
                    if slots > 0:
                        if st.button(f"Request Collaboration with {prof['name'].split()[0]}", key=f"req_{prof['id']}"):
                            st.session_state.selected_professor = prof.to_dict()
                            st.success(f"Ready to request collaboration with {prof['name']}")
                            st.rerun()
                    else:
                        st.warning("No available slots")

    elif current_page == "📋 My Requests" or st.session_state.selected_professor:
        st.markdown("### Request Collaboration")
        if st.session_state.selected_professor:
            prof = st.session_state.selected_professor
            st.markdown(f"""
            <div style="background:#E8F0FE;border:1px solid #1A73E8;border-radius:12px;padding:1.5rem;margin-bottom:1.5rem;border-left:5px solid #1A73E8;">
                <h4 style="color:#202124;">Requesting: {prof['name']} - {prof['title']}</h4>
                <p style="color:#5F6368;">🏛️ {prof['institution']} • 📚 {prof['department']}</p>
            </div>
            """, unsafe_allow_html=True)
            with st.form("collaboration_request"):
                request_type = st.selectbox("Type of Collaboration", prof.get('collaboration_types', ['Research Supervision', 'Joint Research', 'Consultancy']))
                col1, col2 = st.columns(2)
                with col1:
                    requester_name = st.text_input("Full Name *", value=user_display_name)
                    requester_email = st.text_input("Email Address *", value=current_user)
                with col2:
                    requester_institution = st.text_input("Institution *", value=profile.get('institution', 'Arba Minch University'))
                    requester_phone = st.text_input("Phone Number", value="")
                research_topic = st.text_area("Research Topic/Proposal *", height=150)
                submitted = st.form_submit_button("Submit Request", use_container_width=True)
                if submitted:
                    if not requester_name or not requester_email or not requester_institution or not research_topic:
                        st.error("Please fill in all required fields")
                    else:
                        letter_data = generate_request_letter(
                            requester_name, requester_institution,
                            prof['name'], prof['title'], prof['institution'],
                            research_topic, request_type,
                            requester_email, requester_phone
                        )
                        request = {
                            'id': f"REQ{len(st.session_state.requests)+1:04d}",
                            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                            'requester': requester_name,
                            'requester_institution': requester_institution,
                            'professor': prof['name'],
                            'professor_institution': prof['institution'],
                            'request_type': request_type,
                            'research_topic': research_topic,
                            'status': 'Pending',
                            'letter': letter_data
                        }
                        st.session_state.requests.append(request)
                        st.session_state.last_request = request
                        st.session_state.show_letter = True
                        add_notification(f"📩 Collaboration request submitted to {prof['name']}", "success")
                        st.success(f"✅ Request submitted successfully to {prof['name']}!")
                        st.balloons()
                        st.markdown(f"""
                        <div class="letter-box">
                            <h2>REQUEST FOR {request_type.upper()}</h2>
                            <p class="date"><b>Date:</b> {letter_data['date']}</p>
                            <p><b>From:</b><br>{letter_data['from_address']}</p>
                            <p><b>To:</b><br>{letter_data['to_address']}</p>
                            <p><b>Subject:</b> {letter_data['subject']}</p>
                            <p>Dear {prof['name'].split()[0]},</p>
                            <p>{letter_data['body']}</p>
                            <div class="signature">
                                <p>Yours sincerely,</p>
                                <p><b>{requester_name}</b><br>{requester_institution}</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("👈 Please go to 'Find Professionals' and click 'Request Collaboration'")
        st.markdown("### My Collaboration Requests")
        if not st.session_state.requests:
            st.info("You haven't submitted any collaboration requests yet.")
        else:
            for req in reversed(st.session_state.requests):
                with st.expander(f"📩 {req['request_type']} - {req['professor']} ({req['status']})"):
                    st.markdown(f"""
                    <div style="background:#F8F9FA;padding:1.5rem;border-radius:12px;border:1px solid #E8EAED;">
                        <p><b>Institution:</b> {req['professor_institution']}</p>
                        <p><b>Topic:</b> {req['research_topic'][:150]}...</p>
                        <p><b>Submitted:</b> {req['date']}</p>
                        <p><b>Status:</b> <span style="color:#1A73E8;font-weight:600;">{req['status']}</span></p>
                    </div>
                    """, unsafe_allow_html=True)

    elif current_page == "💬 Forum":
        st.markdown("### 💬 Research Discussion Forum")
        st.caption("Share ideas, discuss research, and connect with fellow researchers.")
        with st.expander("➕ Create New Post", expanded=False):
            with st.form("new_post"):
                title = st.text_input("Title", placeholder="Enter your post title...")
                content = st.text_area("Content", height=150, placeholder="Share your research ideas, questions, or insights...")
                tags = st.text_input("Tags (comma separated)", placeholder="e.g., optimization, machine learning, epidemiology")
                submitted = st.form_submit_button("📝 Publish Post", use_container_width=True)
                if submitted and title and content:
                    create_forum_post(title, content, user_display_name, tags)
                    if len(st.session_state.forum_posts) == 1:
                        add_badge(st.session_state.current_user, "💬 First Post")
                    st.success("✅ Post published successfully!")
                    st.rerun()
                elif submitted:
                    st.error("❌ Please enter both title and content.")
        if st.session_state.forum_posts:
            st.markdown(f"### 📝 Recent Posts ({len(st.session_state.forum_posts)} total)")
            for post in reversed(st.session_state.forum_posts):
                with st.expander(f"📌 {post['title']} - by {post['author']}", expanded=False):
                    st.markdown(f"""
                    <div class="forum-post">
                        <div class="post-header">
                            <span class="post-title">{post['title']}</span>
                            <span class="post-meta">🕐 {post['date']} · ❤️ {post['likes']} likes</span>
                        </div>
                        <div style="padding:0.5rem 0;border-top:1px solid #E8EAED;border-bottom:1px solid #E8EAED;">
                            {post['content']}
                        </div>
                        <div class="post-tags">
                            {''.join(f'<span class="tag">#{tag}</span>' for tag in post['tags'])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    col1, col2 = st.columns([1, 5])
                    with col1:
                        if st.button(f"❤️ {post['likes']}", key=f"like_{post['id']}"):
                            like_post(post['id'])
                            st.rerun()
                    st.markdown("---")
                    st.markdown("#### 💬 Comments")
                    if post['comments']:
                        for comment in post['comments']:
                            st.markdown(f"""
                            <div style="background:#F8F9FA;padding:0.75rem;border-radius:8px;margin-bottom:0.5rem;border-left:3px solid #1A73E8;">
                                <strong>{comment['author']}</strong> <span style="color:#5F6368;font-size:0.8rem;">({comment['date']})</span>
                                <p style="margin:0.2rem 0 0 0;">{comment['content']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.caption("No comments yet. Be the first to comment!")
                    with st.form(f"comment_form_{post['id']}"):
                        comment_content = st.text_area("Add a comment", key=f"comment_{post['id']}", placeholder="Share your thoughts...")
                        submitted = st.form_submit_button("💬 Submit Comment", use_container_width=True)
                        if submitted and comment_content:
                            add_comment_to_post(post['id'], user_display_name, comment_content)
                            st.success("Comment added!")
                            st.rerun()
                        elif submitted:
                            st.error("❌ Please enter a comment.")
        else:
            st.info("No posts yet. Start a discussion! 🚀")

    elif current_page == "📊 Analytics":
        st.markdown("### 📊 Research Impact Dashboard")
        pub_data = []
        for _, prof in academicians_df.iterrows():
            pub_data.append({
                'name': prof['name'].split()[1] if len(prof['name'].split()) > 1 else prof['name'],
                'publications': len(prof.get('publications', [])),
                'citations': prof.get('total_citations', 0),
                'h_index': prof.get('h_index', 0),
                'trust_score': prof.get('trust_score', 0)
            })
        df_pub = pd.DataFrame(pub_data)
        if not df_pub.empty:
            col1, col2 = st.columns(2)
            with col1:
                fig = px.bar(df_pub, x='name', y='publications', title='Publications by Researcher', color='publications', color_continuous_scale='Greens', text='publications')
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                fig2 = px.scatter(df_pub, x='publications', y='citations', size='h_index', text='name', title='Publications vs Citations', color='trust_score', color_continuous_scale='Viridis')
                fig2.update_layout(height=400)
                st.plotly_chart(fig2, use_container_width=True)
            col3, col4 = st.columns(2)
            with col3:
                fig3 = px.bar(df_pub, x='name', y='h_index', title='h-index by Researcher', color='h_index', color_continuous_scale='Blues', text='h_index')
                fig3.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig3, use_container_width=True)
            with col4:
                fig4 = px.bar(df_pub, x='name', y='trust_score', title='Trust Score by Researcher', color='trust_score', color_continuous_scale='Oranges', text='trust_score')
                fig4.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig4, use_container_width=True)
            st.markdown("#### 📊 Summary Statistics")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Publications", df_pub['publications'].sum())
            c2.metric("Total Citations", df_pub['citations'].sum())
            c3.metric("Average h-index", f"{df_pub['h_index'].mean():.1f}")
            c4.metric("Average Trust Score", f"{df_pub['trust_score'].mean():.1f}%")

    elif current_page == "💬 Chat":
        show_chat()
    elif current_page == "📅 Events":
        show_event_calendar()
    elif current_page == "💰 Grants":
        show_grants()
    elif current_page == "👥 Mentorship":
        st.markdown("### 👥 Mentorship Program")
        with st.expander("➕ Become a Mentor", expanded=False):
            with st.form("mentor_form"):
                expertise = st.text_input("Your Expertise / Research Areas")
                availability = st.selectbox("Availability", ["Available", "Limited", "Not Available"])
                if st.form_submit_button("Register as Mentor"):
                    st.session_state.mentorships.append({
                        "mentor": st.session_state.current_user,
                        "expertise": expertise,
                        "availability": availability,
                        "mentees": []
                    })
                    add_notification(f"👨‍🏫 {user_display_name} registered as a mentor!", "success")
                    add_points(st.session_state.current_user, 10, "Mentor registration")
                    st.success("You are now a mentor!")
                    st.rerun()
        if st.session_state.mentorships:
            for m in st.session_state.mentorships:
                st.markdown(f"<div style='background:#F8F9FA;padding:1rem;border-radius:12px;margin-bottom:0.5rem;'><strong>{m['mentor']}</strong> · Expertise: {m['expertise']} · {m['availability']}</div>", unsafe_allow_html=True)
    elif current_page == "📄 Papers":
        st.markdown("### 📄 Research Paper Sharing")
        with st.expander("📤 Upload a Paper", expanded=False):
            with st.form("paper_form"):
                title = st.text_input("Paper Title")
                authors = st.text_input("Authors (comma separated)")
                abstract = st.text_area("Abstract / Description")
                if st.form_submit_button("Upload Paper"):
                    st.session_state.papers.append({
                        "title": title,
                        "authors": authors,
                        "abstract": abstract,
                        "uploaded_by": st.session_state.current_user,
                        "date": datetime.now().strftime("%Y-%m-%d")
                    })
                    add_points(st.session_state.current_user, 10, "Paper upload")
                    st.success("Paper uploaded!")
                    st.rerun()
        for p in reversed(st.session_state.papers):
            st.markdown(f"<div style='background:#FFFFFF;border:1px solid #E8EAED;border-radius:12px;padding:1rem;margin-bottom:0.5rem;'><strong>{p['title']}</strong><br>Authors: {p['authors']}<br>{p['abstract'][:200]}...<br><span style='color:#5F6368;'>Uploaded by {p['uploaded_by']} on {p['date']}</span></div>", unsafe_allow_html=True)
    elif current_page == "📝 Feedback":
        st.markdown("### 📝 Feedback & Suggestions")
        with st.form("feedback_form"):
            rating = st.slider("How would you rate the platform?", 1, 5, 5)
            comment = st.text_area("Your feedback (optional)", placeholder="Tell us what you think...")
            if st.form_submit_button("Submit Feedback"):
                st.session_state.feedback.append({
                    "user": st.session_state.current_user,
                    "rating": rating,
                    "comment": comment,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                add_points(st.session_state.current_user, 5, "Feedback submitted")
                st.success("Thank you for your feedback!")
                st.rerun()
        st.markdown("### Recent Feedback")
        for fb in reversed(st.session_state.feedback[-5:]):
            stars = "⭐" * fb['rating']
            st.markdown(f"<div class='feedback-item'><div class='feedback-header'><strong>{fb['user']}</strong><span class='feedback-rating'>{stars}</span></div><p>{fb['comment']}</p><span style='color:#5F6368;font-size:0.8rem;'>{fb['date']}</span></div>", unsafe_allow_html=True)
    elif current_page == "👤 Profile":
        st.markdown("### 👤 My Profile")
        profile = st.session_state.user_profiles.get(st.session_state.current_user, {})
        st.markdown(f"""
        <div style="background:#F8F9FA;padding:2rem;border-radius:16px;border:1px solid #E8EAED;">
            <div style="font-size:4rem;text-align:center;">👤</div>
            <h3 style="text-align:center;">{profile.get('name', user_display_name)}</h3>
            <p style="text-align:center;color:#5F6368;">{st.session_state.current_user}</p>
            <p><strong>Institution:</strong> {profile.get('institution', 'Not set')}</p>
            <p><strong>Department:</strong> {profile.get('department', 'Not set')}</p>
            <p><strong>Research Interests:</strong> {', '.join(profile.get('interests', [])) or 'Not set'}</p>
            <p><strong>Looking for:</strong> {profile.get('collab_type', 'Not set')}</p>
            <p><strong>Points:</strong> ⭐ {st.session_state.user_points.get(st.session_state.current_user, 0)}</p>
            <div><strong>Badges:</strong> {', '.join(st.session_state.user_badges.get(st.session_state.current_user, [])) or 'None yet'}</div>
        </div>
        """, unsafe_allow_html=True)
    elif "📨 Notifications" in current_page:
        show_notification_center()

if __name__ == "__main__":
    main()
