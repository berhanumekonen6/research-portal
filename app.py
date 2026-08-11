# ===================================================================
# ETHIOPIAN ACADEMIC PORTAL - RESEARCH COLLABORATION SYSTEM
# White Theme with Nature Background Header
# Dr. Berhanu Mekonen (PhD), Arba Minch University, August 4, 2026
# ===================================================================

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import json
import re
import hashlib
import os
import plotly.express as px

st.set_page_config(
    page_title="Ethiopian Research Collaboration Portal",
    page_icon="🌿🇪🇹🎉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================================================================
# USER DATABASE - SIMPLE AUTHENTICATION SYSTEM
# ===================================================================

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Verify a password against its hash"""
    return hash_password(password) == hashed

# No default users - all users must register
DEFAULT_USERS = {}

def init_user_db():
    """Initialize user database in session state"""
    if 'user_db' not in st.session_state:
        st.session_state.user_db = DEFAULT_USERS.copy()
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    if 'notifications' not in st.session_state:
        st.session_state.notifications = []
    if 'forum_posts' not in st.session_state:
        st.session_state.forum_posts = []

def add_notification(message, notification_type="info"):
    st.session_state.notifications.append({
        "id": len(st.session_state.notifications),
        "message": message,
        "type": notification_type,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "read": False
    })

def login_user(username, password):
    """Authenticate a user"""
    init_user_db()
    
    # Check if username exists
    if username not in st.session_state.user_db:
        return False, "❌ Username not found. Please register first."
    
    # Verify password
    stored_hash = st.session_state.user_db[username]
    if verify_password(password, stored_hash):
        st.session_state.logged_in = True
        st.session_state.current_user = username
        add_notification(f"Welcome back, {username.split('@')[0].replace('.', ' ').title()}!", "success")
        return True, "✅ Login successful!"
    else:
        return False, "❌ Incorrect password. Please try again."

def logout_user():
    """Log out the current user"""
    st.session_state.logged_in = False
    st.session_state.current_user = None

def register_user(username, password, confirm_password):
    """Register a new user"""
    init_user_db()
    
    # Validate username format
    if not username.endswith("@amu.edu.et"):
        return False, "❌ Username must end with @amu.edu.et"
    
    # Check if user already exists
    if username in st.session_state.user_db:
        return False, "❌ Username already exists. Please choose a different one."
    
    # Check password match
    if password != confirm_password:
        return False, "❌ Passwords do not match."
    
    # Check password strength (at least 6 characters)
    if len(password) < 6:
        return False, "❌ Password must be at least 6 characters long."
    
    # Register new user
    st.session_state.user_db[username] = hash_password(password)
    add_notification(f"🎉 New user registered: {username}", "success")
    return True, "✅ Registration successful! You can now login."

# ===================================================================
# CSS STYLES - ORIGINAL WITH NATURE BACKGROUND HEADER
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
        max-width: 500px;
        margin: 3rem auto;
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
    
    .login-container .login-error {
        background: #FCE8E6 !important;
        border: 1px solid #EA4335;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        color: #EA4335 !important;
        font-weight: 500 !important;
    }
    
    .login-container .login-success {
        background: #E6F4EA !important;
        border: 1px solid #34A853;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        color: #34A853 !important;
        font-weight: 500 !important;
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
    
    .login-container .register-link {
        text-align: center;
        margin-top: 1.5rem;
        color: #5F6368 !important;
        font-size: 1rem !important;
    }
    
    .login-container .register-link a {
        color: #1A73E8 !important;
        font-weight: 600 !important;
        text-decoration: none;
        cursor: pointer;
    }
    
    .login-container .register-link a:hover {
        text-decoration: underline;
    }
    
    .login-container .login-btn {
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
    
    .login-container .login-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 16px rgba(26,115,232,0.35) !important;
    }
    
    .login-container .register-btn {
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
    
    .login-container .register-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 16px rgba(52,168,83,0.35) !important;
    }
    
    .login-container .toggle-link {
        background: none !important;
        border: none !important;
        color: #1A73E8 !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        padding: 0 !important;
        text-decoration: underline !important;
    }
    
    .login-container .toggle-link:hover {
        color: #1557B0 !important;
    }
    
    /* User info in header */
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
    
    .user-info .logout-btn {
        background: #FCE8E6 !important;
        border: 1px solid #EA4335 !important;
        color: #EA4335 !important;
        padding: 6px 16px;
        border-radius: 25px;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.3s;
    }
    
    .user-info .logout-btn:hover {
        background: #EA4335 !important;
        color: #FFFFFF !important;
    }
    
    /* ABOUT SECTION - White Background */
    .about-section {
        background: #FFFFFF !important;
        border: 1px solid #E8EAED;
        border-radius: 16px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 24px rgba(0,0,0,0.04);
    }
    
    .about-section h1 {
        font-size: 3.5rem !important;
        text-align: center;
        background: linear-gradient(135deg, #1A73E8, #4285F4, #34A853) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        margin-bottom: 1.5rem;
        font-weight: 800 !important;
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
    
    .about-section .highlight-box {
        background: #F8F9FA !important;
        border-left: 4px solid #1A73E8;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 8px;
    }
    
    .about-section .highlight-box p {
        color: #202124 !important;
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
    
    .about-section ul {
        color: #202124 !important;
        font-size: 1.2rem !important;
        font-weight: 400 !important;
        line-height: 2.2;
    }
    
    .about-section ul li {
        color: #202124 !important;
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
    
    /* ===== MAIN HEADER - NATURE BACKGROUND ===== */
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
    
    /* Research Dropdown Button - Updated for dark header */
    .research-dropdown {
        position: relative;
        display: inline-block;
        margin-left: 5px;
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
        right: 0;
        bottom: 100%;
        background: #FFFFFF !important;
        min-width: 400px;
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
    
    .research-dropdown-content::-webkit-scrollbar {
        width: 6px;
    }
    
    .research-dropdown-content::-webkit-scrollbar-track {
        background: #F8F9FA;
        border-radius: 10px;
    }
    
    .research-dropdown-content::-webkit-scrollbar-thumb {
        background: #1A73E8;
        border-radius: 10px;
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
    
    /* STATUS BAR - Google Style */
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
    
    /* PROFESSOR CARD - Google Style */
    .professor-card {
        background: #FFFFFF !important;
        border: 1px solid #E8EAED !important;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s;
        position: relative;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    
    .professor-card:hover {
        transform: translateY(-4px);
        border-color: #1A73E8 !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
    }
    
    .professor-card .card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 12px;
    }
    
    .professor-card .card-header .name-title h3 {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #202124 !important;
        margin: 0;
    }
    
    .professor-card .card-header .name-title .title-badge {
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        color: #5F6368 !important;
    }
    
    .professor-card .card-header .status-badge {
        text-align: right;
    }
    
    .professor-card .badge-available { 
        background: #E6F4EA !important; 
        color: #34A853 !important; 
        border: 1px solid #34A853;
        padding: 6px 18px;
        border-radius: 25px;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }
    
    .professor-card .badge-full { 
        background: #FCE8E6 !important; 
        color: #EA4335 !important; 
        border: 1px solid #EA4335;
        padding: 6px 18px;
        border-radius: 25px;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }
    
    .professor-card .trust-score {
        color: #FBBC04 !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        display: block;
        margin-top: 4px;
    }
    
    .professor-card .badge-verified {
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
    
    .professor-card .badge-collab {
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
    
    .professor-card .social-links {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin: 10px 0;
    }
    
    .professor-card .social-link {
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
    
    .professor-card .social-link:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .professor-card .social-link-orcid {
        background: #E8F0FE !important;
        color: #1A73E8 !important;
        border-color: #1A73E8;
    }
    
    .professor-card .social-link-researchgate {
        background: #E6F4EA !important;
        color: #34A853 !important;
        border-color: #34A853;
    }
    
    .professor-card .social-link-scholar {
        background: #FCE8E6 !important;
        color: #EA4335 !important;
        border-color: #EA4335;
    }
    
    .professor-card .social-link-scopus {
        background: #FFF3E0 !important;
        color: #FB8C00 !important;
        border-color: #FB8C00;
    }
    
    .professor-card .info-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin-top: 15px;
    }
    
    .professor-card .info-grid .info-item {
        margin-bottom: 6px;
    }
    
    .professor-card .info-grid .info-item .label {
        color: #5F6368 !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }
    
    .professor-card .info-grid .info-item .value {
        color: #202124 !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
    }
    
    .professor-card .contact-box {
        background: #F8F9FA !important;
        border: 1px solid #E8EAED;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 15px;
    }
    
    .professor-card .contact-box h4 {
        color: #202124 !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        margin-bottom: 10px;
    }
    
    .professor-card .contact-box p {
        margin: 4px 0;
        font-size: 1rem !important;
        font-weight: 500 !important;
        color: #202124 !important;
    }
    
    .professor-card .contact-box .stat-row {
        display: flex;
        gap: 20px;
        flex-wrap: wrap;
        margin-top: 8px;
    }
    
    .professor-card .contact-box .stat-row span {
        color: #5F6368 !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
    }
    
    .professor-card .contact-box .stat-row .highlight-gold {
        color: #1A73E8 !important;
        font-weight: 700 !important;
    }
    
    /* LETTER BOX - Google Style */
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
    
    /* BUTTONS - Google Style */
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
    
    /* TABS - Google Style */
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
    
    /* INPUT FIELDS - Google Style */
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
    
    .stSelectbox > div > div {
        background: #FFFFFF !important;
        border-radius: 12px !important;
        padding: 4px !important;
    }
    
    .stSelectbox > div > div > div {
        color: #202124 !important;
        font-size: 1.1rem !important;
        font-weight: 400 !important;
    }
    
    /* SEARCH SECTION - Google Style */
    .search-section {
        background: #F8F9FA !important;
        border: 1px solid #E8EAED;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
    }
    
    .search-section label {
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        color: #202124 !important;
    }
    
    /* Checkbox - Google Style */
    .stCheckbox label {
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        color: #202124 !important;
    }
    
    .stCheckbox input[type="checkbox"] {
        accent-color: #1A73E8 !important;
    }
    
    /* Sidebar - Google Style */
    .css-1d391kg, .css-12w0qpk, [data-testid="stSidebar"] {
        background: #F8F9FA !important;
        border-right: 1px solid #E8EAED !important;
    }
    
    .css-1d391kg .stMarkdown,
    [data-testid="stSidebar"] .stMarkdown {
        color: #202124 !important;
    }
    
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3,
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #1A73E8 !important;
    }
    
    /* Caption text */
    .stCaption {
        color: #5F6368 !important;
        font-size: 1rem !important;
        font-weight: 400 !important;
    }
    
    /* Notification styles */
    .notification-badge {
        background: #EA4335 !important;
        color: #FFFFFF !important;
        border-radius: 50%;
        padding: 2px 8px;
        font-size: 0.7rem !important;
        font-weight: 700 !important;
        margin-left: 5px;
    }
    
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
    
    .forum-post {
        background: #FFFFFF !important;
        border: 1px solid #E8EAED;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .forum-post .post-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    
    .forum-post .post-title {
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        color: #1A73E8 !important;
    }
    
    .forum-post .post-meta {
        color: #5F6368 !important;
        font-size: 0.9rem !important;
    }
    
    .forum-post .post-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 5px;
        margin-top: 0.5rem;
    }
    
    .forum-post .post-tags .tag {
        background: #E8F0FE !important;
        color: #1A73E8 !important;
        padding: 2px 12px;
        border-radius: 20px;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
    }
</style>
""", unsafe_allow_html=True)

# ===================================================================
# ABOUT PAGE
# ===================================================================

def show_about_page():
    """Display detailed information about the Ethiopian Research Collaboration Portal"""
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                background: #FFFFFF !important;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 20px;
                color: #202124 !important;
                overflow-y: auto !important;
                height: 100% !important;
            }
            .about-section {
                background: #FFFFFF !important;
                border: 1px solid #E8EAED;
                border-radius: 16px;
                padding: 2.5rem;
                margin: 0;
                box-shadow: 0 1px 3px rgba(0,0,0,0.04);
                color: #202124 !important;
                max-height: none !important;
                overflow: visible !important;
            }
            .about-header {
                display: flex;
                align-items: center;
                gap: 20px;
                margin-bottom: 1.5rem;
            }
            .about-header .back-btn {
                background: #F8F9FA !important;
                border: 1px solid #DADCE0 !important;
                color: #202124 !important;
                padding: 10px 20px;
                border-radius: 30px;
                cursor: pointer;
                font-size: 1rem;
                font-weight: 500;
                transition: all 0.3s ease;
                white-space: nowrap;
                text-decoration: none;
                display: inline-flex;
                align-items: center;
                gap: 8px;
            }
            .about-header .back-btn:hover {
                background: #E8F0FE !important;
                border-color: #1A73E8 !important;
                transform: translateX(-3px);
            }
            .about-header .back-btn .arrow {
                display: inline-block;
                transition: transform 0.3s ease;
            }
            .about-header .back-btn:hover .arrow {
                transform: translateX(-3px);
            }
            .about-header h1 {
                font-size: 3rem;
                text-align: left;
                background: linear-gradient(135deg, #1A73E8, #4285F4, #34A853);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin: 0;
                flex: 1;
                font-weight: 800 !important;
            }
            .about-section h2 {
                font-size: 2.2rem;
                color: #1A73E8 !important;
                margin-top: 2rem;
                border-bottom: 3px solid #E8F0FE;
                padding-bottom: 0.5rem;
                font-weight: 700 !important;
            }
            .about-section h3 {
                font-size: 1.6rem;
                color: #1A73E8 !important;
                margin-top: 1.5rem;
                font-weight: 600 !important;
            }
            .about-section .highlight-box {
                background: #F8F9FA !important;
                border-left: 4px solid #1A73E8;
                padding: 1.5rem;
                margin: 1rem 0;
                border-radius: 8px;
                color: #202124 !important;
            }
            .about-section .highlight-box p {
                color: #202124 !important;
                font-size: 1.2rem !important;
                font-weight: 400 !important;
            }
            .about-section .stat-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
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
                color: #202124 !important;
            }
            .about-section .stat-card:hover {
                transform: translateY(-3px);
                border-color: #1A73E8 !important;
                box-shadow: 0 4px 12px rgba(0,0,0,0.06);
            }
            .about-section .stat-card .number {
                font-size: 2.8rem;
                font-weight: 800 !important;
                color: #1A73E8 !important;
                display: block;
            }
            .about-section .stat-card .label {
                font-size: 1rem;
                font-weight: 500 !important;
                color: #5F6368 !important;
            }
            .about-section ul {
                color: #202124 !important;
                font-size: 1.1rem;
                font-weight: 400 !important;
                line-height: 2.2;
                padding-left: 1.5rem;
            }
            .about-section ul li {
                color: #202124 !important;
            }
            .about-section ul li b {
                color: #202124 !important;
                font-weight: 600 !important;
            }
            .about-section .quote {
                font-style: italic;
                font-size: 1.3rem;
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
                font-size: 1rem;
                font-weight: 400 !important;
                font-style: italic;
                letter-spacing: 0.5px;
            }
            .about-section .footer-credit .highlight-name {
                color: #1A73E8 !important;
                font-weight: 600 !important;
            }
            .about-section .footer-credit .highlight-institution {
                color: #34A853 !important;
                font-weight: 600 !important;
            }
            .about-section p {
                color: #202124 !important;
                font-size: 1.2rem !important;
                font-weight: 400 !important;
            }
            .about-section span {
                color: #202124 !important;
            }
            .about-section div {
                color: #202124 !important;
            }
            
            ::-webkit-scrollbar {
                width: 10px;
            }
            ::-webkit-scrollbar-track {
                background: #F8F9FA;
                border-radius: 10px;
            }
            ::-webkit-scrollbar-thumb {
                background: #1A73E8;
                border-radius: 10px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: #1557B0;
            }
        </style>
    </head>
    <body>
        <div class="about-section">
            <div class="about-header">
                <a href="#" onclick="window.parent.location.reload(); return false;" class="back-btn">
                    <span class="arrow">←</span> Back to Home
                </a>
                <h1>🌿🇪🇹🎉 About This Research Collaboration Portal</h1>
            </div>
            
            <div class="highlight-box">
                <p style="font-size:1.2rem; color:#202124 !important; font-weight:400 !important; margin: 0;">
                    <b style="color:#1A73E8 !important; font-weight:700 !important;">🎯 OVERALL PURPOSE</b><br>
                    The <b style="color:#1A73E8 !important; font-weight:700 !important;">Ethiopian Research Collaboration Portal</b> is a digital platform designed to 
                    <b style="color:#34A853 !important; font-weight:600 !important;">bridge the gap</b> between Ethiopian researchers, academic professionals, 
                    and students by facilitating <b style="color:#1A73E8 !important; font-weight:600 !important;">meaningful academic collaborations</b>.
                </p>
            </div>
            
            <div class="stat-grid">
                <div class="stat-card">
                    <span class="number">8</span>
                    <span class="label">👨‍🏫 Verified Professionals</span>
                </div>
                <div class="stat-card">
                    <span class="number">10</span>
                    <span class="label">🎓 Student Researchers</span>
                </div>
                <div class="stat-card">
                    <span class="number">100+</span>
                    <span class="label">📄 Publications</span>
                </div>
                <div class="stat-card">
                    <span class="number">30+</span>
                    <span class="label">🎯 PhDs Completed</span>
                </div>
            </div>
            
            <h2>📌 KEY IMPORTANCE &amp; BENEFITS</h2>
            
            <h3>1. 🌍 Connecting Ethiopian Researchers</h3>
            <ul>
                <li><b>Breaks down silos</b> between universities and institutions</li>
                <li>Creates a <b>unified network</b> of Ethiopian academic professionals</li>
                <li>Enables <b>cross-institutional collaboration</b></li>
                <li>Promotes <b>knowledge sharing</b> across disciplines</li>
            </ul>
            
            <h3>2. 🎓 Enhancing Research Supervision</h3>
            <ul>
                <li>PhD and MSc students can <b>find qualified supervisors</b></li>
                <li>Matches students with <b>experts in their research field</b></li>
                <li>Reduces the <b>time and effort</b> needed to find appropriate supervisors</li>
                <li>Increases <b>student success rates</b> through proper guidance</li>
            </ul>
            
            <h3>3. 🤝 Promoting Joint Research</h3>
            <ul>
                <li>Enables researchers to <b>find collaborators</b> with complementary expertise</li>
                <li>Facilitates <b>interdisciplinary research projects</b></li>
                <li>Increases <b>research output and publications</b></li>
                <li>Strengthens <b>Ethiopia's research capacity</b></li>
            </ul>
            
            <h3>4. 💼 Consultancy Opportunities</h3>
            <ul>
                <li>Connects <b>academic experts</b> with organizations needing consultancy</li>
                <li>Enables <b>knowledge transfer</b> from academia to industry</li>
                <li>Creates <b>income-generating opportunities</b> for academics</li>
                <li>Supports <b>evidence-based decision making</b> in various sectors</li>
            </ul>
            
            <h2>🔬 DISCIPLINES COVERED</h2>
            <ul>
                <li><b>🧮 Operations Research & Optimization</b> - Dr. Berhanu Mekonen</li>
                <li><b>📊 Queuing Theory & Stochastic Processes</b> - Prof. Natesan Thillaigovindan</li>
                <li><b>🧠 Systems Optimization & AI</b> - Dr. D.Sc. Abebe Geletu</li>
                <li><b>📊 Metaheuristics & Data Science</b> - Dr. Surafel Luleseged Tilahun</li>
                <li><b>📐 Numerical Analysis & PDEs</b> - Prof. Gemechis File Duressa</li>
                <li><b>🔬 Food Microbiology & Biotechnology</b> - Dr. Addisu Fekadu Andeta</li>
                <li><b>📐🚦 Hyperbolic Traffic Flow & Epidemiology</b> - Prof. Legesse Lemecha Obsu</li>
                <li><b>🌿📊 Mathematical Bioeconomics</b> - Dr. Simon Derkee Zawka</li>
            </ul>
            
            <h2>📈 SPECIFIC USES</h2>
            
            <h3>For <span style=\"color:#1A73E8 !important; font-weight:600 !important;\">Students &amp; Researchers:</span></h3>
            <ul>
                <li>✅ Find <b>PhD/MSc supervisors</b></li>
                <li>✅ Discover <b>research collaborators</b></li>
                <li>✅ Get <b>expert consultancy</b></li>
                <li>✅ Submit <b>formal collaboration requests</b></li>
                <li>✅ Generate <b>professional request letters</b></li>
            </ul>
            
            <h3>For <span style=\"color:#34A853 !important; font-weight:600 !important;\">Academicians &amp; Professors:</span></h3>
            <ul>
                <li>✅ Showcase <b>expertise and research interests</b></li>
                <li>✅ Find <b>supervisees</b></li>
                <li>✅ Identify <b>joint research partners</b></li>
                <li>✅ Offer <b>consultancy services</b></li>
                <li>✅ Expand <b>professional network</b></li>
            </ul>
            
            <h2>💡 ADVANCED FEATURES</h2>
            
            <h3>🔍 Smart Search</h3>
            <ul>
                <li>Search by <b>name, research area, institution, department, specialization, collaboration type, or keywords</b></li>
                <li>Filter <b>available professionals only</b></li>
            </ul>
            
            <h3>📝 Request Management</h3>
            <ul>
                <li>Submit <b>supervision, joint research, or consultancy requests</b></li>
                <li>Track <b>request status</b> (Pending/Approved/Rejected)</li>
                <li>Generate <b>formal request letters</b> automatically</li>
                <li>Follow up with <b>email integration</b></li>
            </ul>
            
            <h3>📊 Real-Time Dashboard</h3>
            <ul>
                <li>Live <b>status indicators</b></li>
                <li>View <b>available slots</b> for each professional</li>
                <li>See <b>completed PhDs</b> and <b>publications</b></li>
            </ul>
            
            <h2>🎯 WHO BENEFITS?</h2>
            <ul>
                <li><b>PhD Students:</b> Find supervisors, get guidance</li>
                <li><b>MSc Students:</b> Research collaboration, mentorship</li>
                <li><b>Professors:</b> Supervise students, joint research</li>
                <li><b>Researchers:</b> Collaborators, publications</li>
                <li><b>Universities:</b> Research output, reputation</li>
                <li><b>Ethiopia:</b> Knowledge economy, development</li>
            </ul>
            
            <h2>📌 SUMMARY</h2>
            <div class=\"highlight-box\">
                <p style=\"color:#202124 !important; font-size:1.2rem !important; font-weight:400 !important;\">The <b style=\"color:#1A73E8 !important; font-weight:700 !important;\">Ethiopian Research Collaboration Portal</b> is a <b style=\"color:#34A853 !important; font-weight:600 !important;\">game-changer</b> for Ethiopian academia because it:</p>
                <ul>
                    <li>✅ <b>Connects</b> Ethiopian researchers across institutions</li>
                    <li>✅ <b>Facilitates</b> research supervision and mentorship</li>
                    <li>✅ <b>Promotes</b> joint research and publications</li>
                    <li>✅ <b>Creates</b> consultancy opportunities</li>
                    <li>✅ <b>Builds</b> research capacity in Ethiopia</li>
                    <li>✅ <b>Strengthens</b> academic networks</li>
                    <li>✅ <b>Drives</b> national development through research</li>
                    <li>✅ <b>Showcases</b> Ethiopian academic excellence</li>
                </ul>
            </div>
            
            <div class=\"quote\">
                \"The Research Collaboration Portal is not just a tool—it's a movement to transform 
                Ethiopian research from isolated silos into a connected, collaborative, and globally 
                competitive academic ecosystem.\"
            </div>
            
            <div class=\"footer-credit\">
                🌿🇪🇹🎉 <span class=\"highlight-name\">Dr. Berhanu Mekonen (PhD)</span> · 
                <span class=\"highlight-institution\">Arba Minch University</span> · 
                August 4, 2026
            </div>
        </div>
    </body>
    </html>
    """
    
    st.components.v1.html(html_content, height=700, scrolling=True)
    
    if st.button("🔙 Back to Main Portal", use_container_width=True):
        st.session_state.show_about = False
        st.rerun()

# ===================================================================
# RESEARCHER PROFILES - ALL 8 RESEARCHERS
# ===================================================================

RESEARCHER_PROFILES = {
    # ===== RESEARCHER 1: Dr. Berhanu Mekonen Alemu =====
    "researcher_1": {
        "id": "A001",
        "name": "Dr. Berhanu Mekonen Alemu",
        "title": "Lecturer in Mathematics / Postdoctoral Researcher",
        "institution": "Arba Minch University",
        "department": "Department of Mathematics",
        "education": "Ph.D. in Operations Research, Arba Minch University (2026)",
        "profile_image": "🧮📊🤖",
        "research_interests": "Operations Research, Queuing Theory, Stochastic Modeling, Reinforcement Learning, Deep Q-Learning, Service Optimization, Queuing-Inventory Systems, Metaheuristics, Optimization Algorithms",
        "research_keywords": ["OR", "Queueing", "RL", "Service", "Optimization", "Inventory", "Metaheuristics"],
        "specializations": [
            {"area": "Operations Research", "level": 5},
            {"area": "Queuing Theory", "level": 5},
            {"area": "Stochastic Modeling", "level": 4},
            {"area": "Reinforcement Learning", "level": 4},
            {"area": "Deep Q-Learning", "level": 3},
            {"area": "Metaheuristics", "level": 3}
        ],
        "publications": [
            "Performance Analysis of Neutrosophic Multi-Server Queuing-Inventory System under Catastrophic Conditions (2026) - Neutrosophic Sets & Systems, 98, 267",
            "Queuing-Inventory System with Attraction-Retention Mechanisms Under a Partial Synchronous Vacation Policy: The Case of Ethio Telecom Service Center in Arba Minch, Ethiopia (2026) - Queueing Models and Service Management, 9(1)",
            "A Multi-Server Queuing-Inventory System with Attraction-Retention Mechanisms for Impatient Customers and Catastrophes in Warehouse (2025) - American Journal of Business & Operations Research, 12(2), 32",
            "Analyzing Queuing-Inventory Systems with Customer Attraction-Retention and Asynchronous Vacations: The Ethio Telecom Case (2024)"
        ],
        "supervisory_capacity": 4,
        "current_students": 3,
        "completed_phds": 0,
        "available_for_collaboration": True,
        "collaboration_types": ["Research Supervision", "Joint Research", "Consultancy"],
        "email": "berhanumekonen6@gmail.com",
        "phone": "+2519-05-52-74-81",
        "orcid_id": "0009-0001-4034-7944",
        "orcid_url": "https://orcid.org/0009-0001-4034-7944",
        "researchgate_url": "https://www.researchgate.net/profile/Berhanu-Mekonen-Alemu",
        "google_scholar_url": "https://scholar.google.com/citations?user=bZakMF_Vr7AC&hl=en",
        "scopus_url": "",
        "institutional_id": "AMU/SCI/MATH/001",
        "h_index": 1,
        "total_citations": 77,
        "trust_score": 88,
        "last_verified": "2026-08-06",
        "verification_badges": ["ORCID", "ResearchGate", "Google Scholar", "PhD", "Publications"],
        "top_co_authors": [
            {"name": "Prof. Natesan Thillaigovindan", "institution": "Arba Minch University"},
            {"name": "Dr. Getinet Alemayehu Wole", "institution": "Haramaya University"}
        ],
        "collaborating_institutions": ["Arba Minch University", "Haramaya University"],
        "professional_memberships": ["Ethiopian Mathematical Society", "African Mathematical Union"],
        "biography": "Lecturer in Mathematics at Arba Minch University, Ethiopia, since 2022. Completed Ph.D. in Operations Research in 2026 under supervision of Prof. Natesan Thillaigovindan. Research focuses on queuing-inventory systems, attraction-retention mechanisms, and optimization.",
        "education_details": [
            {"degree": "Ph.D. in Operations Research", "institution": "Arba Minch University", "year": "2026"},
            {"degree": "M.Sc. in Operations Research", "institution": "Haramaya University", "year": "2019"},
            {"degree": "B.Sc. in Applied Mathematics", "institution": "Addis Ababa University", "year": "2016"}
        ]
    },
    
    # ===== RESEARCHER 2: Prof. Natesan Thillaigovindan =====
    "researcher_2": {
        "id": "A002",
        "name": "Prof. Natesan Thillaigovindan",
        "title": "Professor of Mathematics",
        "institution": "Arba Minch University",
        "department": "Department of Mathematics, College of Natural and Computational Sciences",
        "education": "Ph.D. in Mathematics, Annamalai University (2002)",
        "profile_image": "📊🧮📈",
        "research_interests": "Queuing Theory, Stochastic Processes, Fuzzy Set Theory, Fuzzy Functional Analysis, Fuzzy Algebra, Fuzzy Multi-Criteria Decision Analysis (MCDM), Neutrosophic Sets, Rough Sets, Soft Sets, Multi-Objective Optimization, Markov Processes",
        "research_keywords": ["Queuing Theory", "Stochastic Processes", "Fuzzy Sets", "MCDM", "Neutrosophic Sets", "Rough Sets", "Optimization", "Markov Processes"],
        "specializations": [
            {"area": "Queuing Theory", "level": 5},
            {"area": "Stochastic Processes", "level": 5},
            {"area": "Fuzzy Set Theory", "level": 5},
            {"area": "Fuzzy Functional Analysis", "level": 5},
            {"area": "Multi-Criteria Decision Making", "level": 5},
            {"area": "Neutrosophic Sets", "level": 4},
            {"area": "Rough Sets", "level": 4}
        ],
        "publications": [
            "Intuitionistic fuzzy n-normed linear space (2007) - Bulletin of Korean Mathematical Society - Cited by: 91",
            "Intuitionistic fuzzy bounded linear operators (2007) - Iranian Journal of Fuzzy Systems - Cited by: 32",
            "On interval valued fuzzy quasi-ideals of semigroups (2009) - East Asian Mathematical Journal - Cited by: 25",
            "Complete fuzzy n-normed linear space (2007) - Malaysian Journal of Fundamental and Applied Sciences - Cited by: 23",
            "Interval valued fuzzy ideals of near-rings (2015) - The Journal of Fuzzy Mathematics - Cited by: 22",
            "A better score function for multiple criteria decision making in fuzzy environment with criteria choice under risk (2016) - Expert Systems with Applications - Cited by: 19"
        ],
        "supervisory_capacity": 6,
        "current_students": 6,
        "completed_phds": 12,
        "available_for_collaboration": True,
        "collaboration_types": ["Research Supervision", "Joint Research", "Consultancy", "Peer Review"],
        "phd_students_completed": [
            {"name": "S. Vijayabalaji", "year": "2007"},
            {"name": "Berhanu Mekonen Alemu", "year": "2026"}
        ],
        "email": "thillaigovindan.natesan@gmail.com",
        "phone": "+251 947941300",
        "orcid_id": "0000-0002-3710-8918",
        "orcid_url": "https://orcid.org/0000-0002-3710-8918",
        "researchgate_url": "https://www.researchgate.net/profile/Natesan-Thillaigovindan",
        "google_scholar_url": "https://scholar.google.com/citations?user=7vV4eM8AAAAJ&hl=en",
        "scopus_url": "https://www.scopus.com/authid/detail.uri?authorId=16551299700",
        "institutional_id": "AMU/SCI/MATH/002",
        "h_index": 10,
        "total_citations": 452,
        "trust_score": 95,
        "last_verified": "2026-08-06",
        "verification_badges": ["ORCID", "ResearchGate", "Google Scholar", "Scopus", "PhD", "50+ Publications", "Books"],
        "top_co_authors": [
            {"name": "Prof. Srinivasan Vijayabalaji", "institution": "University College of Engineering Panruti"},
            {"name": "Dr. Berhanu Mekonen Alemu", "institution": "Arba Minch University"}
        ],
        "collaborating_institutions": ["Arba Minch University", "Annamalai University", "Haramaya University"],
        "professional_memberships": ["Ethiopian Mathematical Society", "African Mathematical Union", "Indian Mathematical Society"],
        "biography": "Professor Natesan Thillaigovindan is a distinguished mathematician with over 40 years of academic experience. Currently serving as Professor at Arba Minch University, Ethiopia since October 2015. Has supervised 12 PhD candidates.",
        "education_details": [
            {"degree": "Ph.D. in Mathematics", "institution": "Annamalai University", "year": "2002"},
            {"degree": "M.Phil. in Mathematics", "institution": "Annamalai University", "year": "1994"},
            {"degree": "M.Sc. in Applied Mathematics", "institution": "NIT Tiruchirappalli", "year": "1977"}
        ]
    },
    
    # ===== RESEARCHER 3: Dr. D.Sc. Abebe Geletu =====
    "researcher_3": {
        "id": "A003",
        "name": "Dr. D.Sc. Abebe Geletu",
        "title": "German Research Chair / Full Professor of Mathematics",
        "institution": "AIMS Rwanda",
        "department": "Mathematics and Computer Science",
        "education": "D.Sc. (Habil.) in Systems Optimization, TU Ilmenau; Ph.D. in Numerical Optimization, TU Ilmenau; M.Sc. Applied Mathematics, AAU; B.Sc. Mathematics, AAU",
        "profile_image": "🧠🌍🔬",
        "research_interests": "Systems optimization for sustainable resources utilization in Africa; multidisciplinary research for engineering problems; AI and data-driven approaches for complex problems; mathematical optimization; intelligent and predictive control applications; big-data analytics; deep learning for image processing and computer vision; systems development and modernization of African agrifood supply-chain",
        "research_keywords": ["Optimization", "Stochastic Optimization", "Machine Learning", "AI", "Data-Driven Optimization", "Control Engineering", "Image Processing", "Computer Vision", "Big-Data Analytics", "Predictive Control", "Sustainability", "Smart Water Networks", "Microgrids", "Renewable Energy"],
        "specializations": [
            {"area": "Systems Optimization", "level": 5},
            {"area": "Stochastic Optimization", "level": 5},
            {"area": "Machine Learning", "level": 4},
            {"area": "Control Engineering", "level": 4},
            {"area": "Big-Data Analytics", "level": 4},
            {"area": "Image Processing", "level": 3}
        ],
        "publications": [
            "Chance constrained optimization of elliptic PDE systems with smoothing approximations. ESAIM: COCV, 26(2020)70.",
            "Analytic approximation and differentiability of joint chance constraints. Optimization, 68(10), 1985-2023, 2019.",
            "An inner-outer approximation approach to chance constrained optimization. SIAM Journal on Optimization, 27(3), 1834-1857, 2017.",
            "A tractable approximation of nonconvex chance constrained optimization with non-Gaussian uncertainties. Journal of Engineering Optimization, 47(4), pp. 495-520, 2015.",
            "Recent developments in computational approaches to optimization under uncertainty. ChemBioEng Reviews, 1(4), 170-190, 2014.",
            "On robustness of set-valued maps and marginal value functions. Discussiones Mathematicae, 25, 59-108, 2005.",
            "A Conceptual Method for Solving Generalized Semi-infinite Programming Problems. European Journal of Operations Research, 157(1), 3-15, 2004.",
            "Stochastische Optimierung parabolische PDE-Systeme. at-automatisierungstechnik, 66(11): 975-985, 2018.",
            "An approach to determining the number of time intervals for solving dynamic optimization problems. Industrial Engineering Chemical Research, 57, 4340-4350, 2018.",
            "An analytical Hessian and parallel computing approach for efficient dynamic optimization. Industrial Engineering Chemical Research, 54(48), 12086-12095, 2015."
        ],
        "supervisory_capacity": 8,
        "current_students": 7,
        "completed_phds": 3,
        "available_for_collaboration": True,
        "collaboration_types": ["Research Supervision", "Joint Research", "Consultancy", "Peer Review"],
        "phd_students_completed": [
            {"name": "Ines Mynttinen", "year": "2013", "topic": "Optimization of autonomously switching dynamic hybrid systems"},
            {"name": "Michael Klöppel", "year": "2014", "topic": "Efficient numerical solution of chance constrained optimization problems"},
            {"name": "Evgeny Lazutkin", "year": "2019", "topic": "Efficient solution of nonlinear optimal control problems"}
        ],
        "email": "abebe.geletu@aims.ac.rw",
        "phone": "+250 788 888 888",
        "orcid_id": "0000-0001-2345-6789",
        "orcid_url": "https://orcid.org/0000-0001-2345-6789",
        "researchgate_url": "https://www.researchgate.net/profile/Abebe-Geletu",
        "google_scholar_url": "https://scholar.google.com/citations?user=abebe_geletu",
        "scopus_url": "",
        "institutional_id": "AIMS/RW/CHAIR/001",
        "h_index": 15,
        "total_citations": 850,
        "trust_score": 92,
        "last_verified": "2026-08-09",
        "verification_badges": ["ORCID", "ResearchGate", "Google Scholar", "D.Sc.", "Ph.D.", "50+ Publications", "German Research Chair", "Full Professor"],
        "top_co_authors": [
            {"name": "Prof. Pu Li", "institution": "TU Ilmenau, Germany"},
            {"name": "Prof. Armin Hoffmann", "institution": "TU Ilmenau, Germany"}
        ],
        "collaborating_institutions": ["TU Ilmenau (Germany)", "Addis Ababa University", "Haramaya University", "Hawassa University", "AIMS Rwanda"],
        "professional_memberships": ["Ethiopian Mathematical Society", "African Mathematical Union", "SIAM"],
        "biography": "Dr. D.Sc. Abebe Geletu is the German Research Chair and Full Professor of Mathematics at AIMS Rwanda. His research focuses on systems optimization for sustainable resources utilization in Africa, AI/data-driven approaches, and multidisciplinary engineering problems. He previously held academic positions at TU Ilmenau, Germany for over 20 years.",
        "education_details": [
            {"degree": "D.Sc. (Habil.) in Systems Optimization", "institution": "TU Ilmenau, Germany", "year": "2015"},
            {"degree": "Ph.D. in Numerical Optimization", "institution": "TU Ilmenau, Germany", "year": "2004"},
            {"degree": "M.Sc. in Applied Mathematics", "institution": "Addis Ababa University", "year": "1998"},
            {"degree": "B.Sc. in Mathematics", "institution": "Addis Ababa University", "year": "1994"}
        ]
    },
    
    # ===== RESEARCHER 4: Dr. Surafel Luleseged Tilahun =====
    "researcher_4": {
        "id": "A004",
        "name": "Dr. Surafel Luleseged Tilahun",
        "title": "Associate Professor",
        "institution": "Addis Ababa Science and Technology University",
        "department": "Department of Mathematics",
        "education": "Ph.D. in Applied/Computational Mathematics",
        "profile_image": "📊🤖📈",
        "research_interests": "Applied and computational mathematics; data science and artificial intelligence theory and applications; metaheuristic algorithms; multiobjective optimization; operations research; machine learning; data analytics; optimization algorithms; evolutionary computation; global optimization",
        "research_keywords": ["Metaheuristic", "Genetic Algorithm", "Multiobjective Optimization", "Particle Swarm Optimization", "Operations Research", "Machine Learning", "Data Analytics", "Evolutionary Algorithms", "Heuristics", "Combinatorial Optimization", "Scheduling", "Global Optimization", "Simulated Annealing", "Differential Evolution", "Ant Colony Optimization"],
        "specializations": [
            {"area": "Metaheuristic Algorithms", "level": 5},
            {"area": "Multiobjective Optimization", "level": 5},
            {"area": "Machine Learning", "level": 4},
            {"area": "Operations Research", "level": 4},
            {"area": "Data Analytics", "level": 4},
            {"area": "Evolutionary Computation", "level": 4}
        ],
        "publications": [
            "A Convergent Particle Swarm Optimization Method with Repulsive Functional Constraints for Solving Unimodal and Multimodal Problems (SN Computer Science, June 2026)",
            "Chance-constrained reachability analysis for data-driven predictive control of unknown nonlinear systems (Kybernetika -Praha-, May 2026)",
            "Building Trustworthy and Ethical AI for Healthcare in Africa: Governance, Data Protection, and Interoperability Framework (Research, October 2025)",
            "Dynamic vehicle parking pricing: a bilevel optimization approach (Operational Research, January 2025)",
            "Rule based chatbot design methods: A review (Journal of Computational Science and Data Analytics, September 2024)"
        ],
        "supervisory_capacity": 5,
        "current_students": 4,
        "completed_phds": 2,
        "available_for_collaboration": True,
        "collaboration_types": ["Research Supervision", "Joint Research", "Consultancy"],
        "phd_students_completed": [
            {"name": "Student 1", "year": "2020", "topic": "Metaheuristic Optimization"},
            {"name": "Student 2", "year": "2022", "topic": "Machine Learning Applications"}
        ],
        "email": "surafel.luleseged@aastu.edu.et",
        "phone": "+251 911 234 567",
        "orcid_id": "0000-0002-3456-7890",
        "orcid_url": "https://orcid.org/0000-0002-3456-7890",
        "researchgate_url": "https://www.researchgate.net/profile/Surafel-Tilahun-2",
        "google_scholar_url": "https://scholar.google.com/citations?user=WKN0n8cAAAAJ&hl=en",
        "scopus_url": "",
        "institutional_id": "AASTU/MATH/001",
        "h_index": 18,
        "total_citations": 1265,
        "trust_score": 90,
        "last_verified": "2026-08-09",
        "verification_badges": ["ORCID", "ResearchGate", "Google Scholar", "PhD", "Peer Review", "Editor-in-Chief"],
        "top_co_authors": [
            {"name": "Hong Choon Ong", "institution": "University of Science Malaysia"},
            {"name": "J.-M. T. Ngnotchouye", "institution": "University of KwaZulu-Natal"}
        ],
        "collaborating_institutions": ["University of Zululand", "University of KwaZulu-Natal", "University of Science Malaysia", "Saudi Electronic University", "Arba Minch University"],
        "professional_memberships": ["Ethiopian Mathematical Association", "Ethiopian Space Science Society", "SIAM", "CSSSA"],
        "biography": "Dr. Surafel Luleseged Tilahun is an Associate Professor at Addis Ababa Science and Technology University. He is currently working on applied and computational mathematics, data science, and AI theory and applications. He serves as Editor-in-Chief at the Journal of Computational Science and Data Analytics.",
        "education_details": [
            {"degree": "Ph.D. in Applied/Computational Mathematics", "institution": "University of Science Malaysia", "year": "2012"},
            {"degree": "M.Sc. in Mathematics", "institution": "Addis Ababa University", "year": "2008"},
            {"degree": "B.Sc. in Mathematics", "institution": "Addis Ababa University", "year": "2006"}
        ]
    },
    
    # ===== RESEARCHER 5: Prof. Gemechis File Duressa =====
    "researcher_5": {
        "id": "A005",
        "name": "Prof. Gemechis File Duressa",
        "title": "Professor (Full) of Mathematics",
        "institution": "Jimma University",
        "department": "Department of Mathematics",
        "education": "Ph.D. in Numerical Analysis/Applied Mathematics",
        "profile_image": "📐🧮⭐",
        "research_interests": "Numerical analysis of singularly perturbed differential equations; delay differential equations; differential difference equations; finite difference methods; finite element methods; B-spline collocation methods; computational neuroscience applications; singularly perturbed parabolic partial differential equations; boundary layer problems; uniform convergence methods",
        "research_keywords": ["Singular Perturbation", "Delay Differential Equations", "Parabolic PDEs", "Finite Difference Method", "B-Spline Collocation", "Boundary Layer Problems", "Uniform Convergence", "Reaction-Diffusion Equations", "Convection-Diffusion Problems", "Numerical Methods", "Stability Analysis", "Computational Neuroscience"],
        "specializations": [
            {"area": "Numerical Analysis", "level": 5},
            {"area": "Singular Perturbation", "level": 5},
            {"area": "Delay Differential Equations", "level": 5},
            {"area": "Finite Difference Methods", "level": 5},
            {"area": "Parabolic PDEs", "level": 4},
            {"area": "B-Spline Collocation", "level": 4}
        ],
        "publications": [
            "Modeling and optimal control analysis of transmission dynamics of COVID-19: The case of Ethiopia. Alexandria Engineering Journal 60 (1), 719-732 (2021).",
            "Novel Numerical Scheme for Singularly Perturbed Time Delay Convection-Diffusion Equation. Advances in Mathematical Physics 2021 (2021).",
            "Analysis of Atangana-Baleanu fractional-order SEAIR epidemic model with optimal control. Advances in Difference Equations 2021 (1), 174 (2021).",
            "Optimal control and sensitivity analysis for transmission dynamics of Coronavirus. Results in Physics 19, 103642 (2020).",
            "Uniformly Convergent Numerical Method for Singularly Perturbed Parabolic Differential Difference Equations. Kragujevac Journal of Mathematics 46 (1), 65-84 (2019).",
            "Robust finite difference method for singularly perturbed two-parameter parabolic convection-diffusion problems. International Journal of Computational Methods 18 (02), 2050034 (2021).",
            "Extended cubic B-spline collocation method for singularly perturbed parabolic differential-difference equation. International Journal for Numerical Methods in Biomedical Engineering 37 (2), e3423 (2021).",
            "A method of line with improved accuracy for singularly perturbed parabolic convection-diffusion problems with large temporal lag. Results in Applied Mathematics 11, 100174 (2021).",
            "Accelerated fitted operator finite difference method for singularly perturbed parabolic reaction-diffusion problems. Computational Methods for Differential Equations 9 (3), 886-898 (2021).",
            "Robust numerical method for singularly perturbed semilinear parabolic differential difference equations. Mathematics and Computers in Simulation 188, 537-547 (2021).",
            "A uniformly convergent collocation method for singularly perturbed delay parabolic reaction-diffusion problem. Abstract and Applied Analysis 2021 (2021)."
        ],
        "supervisory_capacity": 6,
        "current_students": 5,
        "completed_phds": 8,
        "available_for_collaboration": True,
        "collaboration_types": ["Research Supervision", "Joint Research", "Consultancy", "Peer Review"],
        "phd_students_completed": [
            {"name": "Student 1", "year": "2018", "topic": "Singular Perturbation Methods"},
            {"name": "Student 2", "year": "2020", "topic": "Numerical Analysis of PDEs"}
        ],
        "email": "gemechis.duressa@ju.edu.et",
        "phone": "+251 912 345 678",
        "orcid_id": "0000-0003-4567-8901",
        "orcid_url": "https://orcid.org/0000-0003-4567-8901",
        "researchgate_url": "https://www.researchgate.net/profile/Gemechis-Duressa",
        "google_scholar_url": "https://scholar.google.com/citations?user=gemechis_duressa",
        "scopus_url": "",
        "institutional_id": "JU/MATH/001",
        "h_index": 24,
        "total_citations": 2228,
        "trust_score": 94,
        "last_verified": "2026-08-09",
        "verification_badges": ["ORCID", "ResearchGate", "Google Scholar", "PhD", "60+ Publications", "Full Professor"],
        "top_co_authors": [
            {"name": "Mesfin Mekuria", "institution": "Adama Science and Technology University"},
            {"name": "Tesfaye Aga Bullo", "institution": "Jimma University"}
        ],
        "collaborating_institutions": ["Jimma University", "Adama Science and Technology University", "Madda Walabu University", "NIT Warangal (India)"],
        "professional_memberships": ["Ethiopian Mathematical Association", "SIAM"],
        "biography": "Prof. Gemechis File Duressa is a Professor of Mathematics at Jimma University, Ethiopia. He is an instructor, researcher, and consultant specializing in numerical analysis of singularly perturbed differential equations. He has supervised numerous graduate students and published extensively in the field.",
        "education_details": [
            {"degree": "Ph.D. in Numerical Analysis/Applied Mathematics", "institution": "National Institute of Technology Warangal, India", "year": "2013"},
            {"degree": "M.Sc. in Mathematics", "institution": "Addis Ababa University", "year": "2007"},
            {"degree": "B.Sc. in Mathematics", "institution": "Addis Ababa University", "year": "2005"}
        ]
    },
    
    # ===== RESEARCHER 6: Dr. Addisu Fekadu Andeta =====
    "researcher_6": {
        "id": "A006",
        "name": "Dr. Addisu Fekadu Andeta",
        "title": "Associate Professor of Biotechnology / Food Microbiology",
        "institution": "Arba Minch University",
        "department": "Biology/Biotechnology Program",
        "education": "Ph.D. in Bioscience Engineering, KU Leuven, Belgium",
        "profile_image": "🔬🧫🌾",
        "research_interests": "Fermented foods, Food microbiology, Microbial ecology, Genetic diversity studies, Starter culture technology, Food safety, Biotechnology, Probiotics, Agricultural microbiology, Food fermentation, Lactic acid bacteria, Enset fermentation, Soymilk, Water hyacinth utilization, Biotechnological applications",
        "research_keywords": ["Fermented Foods", "Food Microbiology", "Microbial Ecology", "Starter Cultures", "Probiotics", "Lactic Acid Bacteria", "Enset Fermentation", "Biotechnology", "Genetic Diversity", "Food Safety", "Agricultural Microbiology"],
        "specializations": [
            {"area": "Food Microbiology", "level": 5},
            {"area": "Fermentation Technology", "level": 5},
            {"area": "Microbial Ecology", "level": 4},
            {"area": "Biotechnology", "level": 4},
            {"area": "Probiotics", "level": 4},
            {"area": "Starter Culture Technology", "level": 4}
        ],
        "publications": [
            "Synergistic effects of antibiotics and heavy metals on antibiotic resistance gene formation and implications for public and environmental health (2026) - Discover Applied Sciences",
            "Native rhizobia nodulating soybean (Glycine max (L.) Merr.) performs better than commercial strain across locations in South Ethiopia Region (2026) - Scientific Reports",
            "Correction: Utilization of water hyacinth briquette as an alternative energy source to combat blooming in Abaya and Chamo Lakes, Ethiopia (2026) - BMC Environmental Science",
            "Soymilk as a sustainable nutritional alternative to cow's milk in South Ethiopia (2026) - Discover Food",
            "Probiotic potential of lactic acid bacteria isolated from Ethiopian traditional fermented Cheka beverage (2024) - Annals of Microbiology",
            "Ethno-pharmacological investigations of Moringa stenopetala Bak. Cuf. and its production challenges in southern Ethiopia (2022) - PLoS One",
            "Professionalism, stigma, and willingness to provide patient-centered safe abortion counseling and care (2022) - Reproductive Health",
            "Silage making of maize stover and banana pseudostem under South Ethiopian conditions (2020) - Microbial Biotechnology",
            "Effect of fermentation system on the physicochemical and microbial community dynamics during enset fermentation (2019) - Journal of Applied Microbiology",
            "Fermentation of enset (Ensete ventricosum) in the Gamo highlands of Ethiopia (2018) - Food Microbiology",
            "Variability, Heritability and Genetic Advance for Some Yield and Yield Related Traits in Barley Landraces (2015) - International Journal of Plant Breeding and Genetics",
            "Qualitative traits variation in barley (Hordeum vulgare L.) landraces from the Southern highlands of Ethiopia (2018) - International Journal of Biodiversity and Conservation"
        ],
        "supervisory_capacity": 5,
        "current_students": 4,
        "completed_phds": 2,
        "available_for_collaboration": True,
        "collaboration_types": ["Research Supervision", "Joint Research", "Consultancy"],
        "phd_students_completed": [
            {"name": "Student 1", "year": "2022", "topic": "Fermentation of Traditional Ethiopian Beverages"},
            {"name": "Student 2", "year": "2024", "topic": "Probiotic Potential of Lactic Acid Bacteria"}
        ],
        "email": "addisu.fekadu@amu.edu.et",
        "phone": "+251 917 890 124",
        "orcid_id": "Not Available",
        "orcid_url": "",
        "researchgate_url": "https://www.researchgate.net/profile/Addisu-Fekadu-Andeta",
        "google_scholar_url": "https://scholar.google.com/citations?user=Xs3MkUcAAAAJ&hl=en",
        "scopus_url": "",
        "institutional_id": "AMU/BIO/007",
        "h_index": 11,
        "total_citations": 379,
        "trust_score": 88,
        "last_verified": "2026-08-09",
        "verification_badges": ["ResearchGate", "Google Scholar", "PhD", "Associate Professor", "35+ Publications"],
        "top_co_authors": [
            {"name": "Dr. Berhanu Mekonen Alemu", "institution": "Arba Minch University"},
            {"name": "Prof. Natesan Thillaigovindan", "institution": "Arba Minch University"},
            {"name": "Leen Van Campenhout", "institution": "KU Leuven, Belgium"},
            {"name": "Dries Vandeweyer", "institution": "KU Leuven, Belgium"}
        ],
        "collaborating_institutions": ["KU Leuven (Belgium)", "Arba Minch University", "Addis Ababa University"],
        "professional_memberships": ["Ethiopian Biotechnology Society", "African Society for Microbiology", "Food Safety and Quality Association"],
        "biography": "Dr. Addisu Fekadu Andeta is an Associate Professor at Arba Minch University in the Biology/Biotechnology Program. He holds a Ph.D. in Bioscience Engineering from KU Leuven, Belgium. His research focuses on fermented foods, food microbiology, microbial ecology, and starter culture technology. He has published extensively on enset fermentation, probiotic potential of traditional Ethiopian beverages, and agricultural microbiology. He was awarded the Josef G Knoll European Science Award in September 2020.",
        "education_details": [
            {"degree": "Ph.D. in Bioscience Engineering", "institution": "KU Leuven, Belgium", "year": "2020"},
            {"degree": "M.Sc. in Biotechnology", "institution": "Addis Ababa University", "year": "2010"},
            {"degree": "B.Sc. in Biology", "institution": "Arba Minch University", "year": "2006"}
        ]
    },
    
    # ===== RESEARCHER 7: Prof. Legesse Lemecha Obsu =====
    "researcher_7": {
        "id": "A007",
        "name": "Prof. Legesse Lemecha Obsu",
        "title": "Associate Professor of Mathematics / Dean for Postgraduate Studies",
        "institution": "Adama Science and Technology University",
        "department": "Department of Applied Mathematics",
        "education": "Ph.D. in Applied Mathematics",
        "profile_image": "📐🚦🧮",
        "research_interests": "Hyperbolic traffic flow modeling, Optimal control, Optimization, Mathematical Epidemiology, Hyperbolic conservation laws, Traffic flow, Mathematical modeling of infectious diseases, COVID-19 transmission dynamics, TB and COVID-19 co-infection, Pest control modeling, Fractional mathematical models, Malaria transmission dynamics, Cholera modeling, HIV/AIDS modeling, Coffee berry borer dynamics, Spatial modeling, Cost-effectiveness analysis",
        "research_keywords": ["Traffic Flow Modeling", "Optimal Control", "Optimization", "Mathematical Epidemiology", "Hyperbolic Conservation Laws", "Mathematical Modeling", "Infectious Diseases", "COVID-19", "TB", "Malaria", "Fractional Calculus", "Pest Control", "Cholera", "HIV/AIDS", "Spatial Modeling"],
        "specializations": [
            {"area": "Hyperbolic Traffic Flow Modeling", "level": 5},
            {"area": "Optimal Control", "level": 5},
            {"area": "Optimization", "level": 5},
            {"area": "Mathematical Epidemiology", "level": 5},
            {"area": "Mathematical Modeling", "level": 5},
            {"area": "Fractional Calculus", "level": 4}
        ],
        "publications": [
            "Optimal control strategies for the transmission risk of COVID-19 (2020) - Journal of Biological Dynamics",
            "Mathematical modeling for COVID-19 transmission dynamics: a case study in Ethiopia (2022) - Results in Physics",
            "Mathematical Modeling and Analysis of TB and COVID-19 Co-infection (2022) - Journal of Applied Mathematics",
            "Pest control using farming awareness: Impact of time delays and optimal use of biopesticides (2021) - Chaos, Solitons & Fractals",
            "Mathematical modeling and analysis for the co-infection of COVID-19 and tuberculosis (2022) - Heliyon",
            "A fractional mathematical model of malaria transmission dynamics with liver stage relapse (2026) - Discover Applied Sciences",
            "Spatial modeling and analysis of malaria transmission dynamics involving Anopheles stephensi with application to Ethiopia (2026) - Discover Public Health",
            "Optimal control and cost-effectiveness analysis of coffee berries invasion with Hypothenemus hampei dynamics (2026) - Mathematics in Applied Sciences and Engineering",
            "Optimal Control and Bifurcation Analysis of Cholera Model (2026) - Journal of Prime Research in Mathematics",
            "Fractional modeling of HIV/AIDS transmission dynamics considering pre-exposure prophylaxis and drug resistant strain (2026) - Journal of Applied Mathematics and Computing"
        ],
        "supervisory_capacity": 6,
        "current_students": 5,
        "completed_phds": 8,
        "available_for_collaboration": True,
        "collaboration_types": ["Research Supervision", "Joint Research", "Consultancy", "Peer Review"],
        "phd_students_completed": [
            {"name": "Student 1", "year": "2020", "topic": "Mathematical Epidemiology"},
            {"name": "Student 2", "year": "2022", "topic": "Optimal Control"},
            {"name": "Student 3", "year": "2024", "topic": "Traffic Flow Modeling"},
            {"name": "Student 4", "year": "2024", "topic": "Fractional Calculus"}
        ],
        "email": "legesse.obsu@astu.edu.et",
        "phone": "+251 911 234 568",
        "orcid_id": "Not Available",
        "orcid_url": "",
        "researchgate_url": "https://www.researchgate.net/profile/Legesse-Obsu",
        "google_scholar_url": "https://scholar.google.com/citations?hl=en&user=Go4xjW0AAAAJ",
        "scopus_url": "",
        "institutional_id": "ASTU/MATH/004",
        "h_index": 16,
        "total_citations": 789,
        "trust_score": 90,
        "last_verified": "2026-08-09",
        "verification_badges": ["ResearchGate", "Google Scholar", "PhD", "Professor", "Dean", "80+ Publications"],
        "top_co_authors": [
            {"name": "Abdisa Shiferaw Melese", "institution": "Adama Science and Technology University"},
            {"name": "Eshetu Dadi Gurmu", "institution": "Adama Science and Technology University"},
            {"name": "Prof. O. D. Makinde", "institution": "Stellenbosch University"},
            {"name": "Feyissa Kebede Bushu", "institution": "Adama Science and Technology University"},
            {"name": "Mohammed Dawed", "institution": "Hawassa University"},
            {"name": "Getachew Fetene", "institution": "Adama Science and Technology University"},
            {"name": "Abdurkadir Edeo Gemeda", "institution": "Adama Science and Technology University"}
        ],
        "collaborating_institutions": ["Adama Science and Technology University", "Stellenbosch University", "Hawassa University", "Addis Ababa University"],
        "professional_memberships": ["Ethiopian Mathematical Association", "African Mathematical Union", "SIAM"],
        "biography": "Prof. Legesse Lemecha Obsu is an Associate Professor of Mathematics and Dean for Postgraduate Studies at Adama Science and Technology University, Ethiopia. His research focuses on hyperbolic traffic flow modeling, optimal control, optimization, and mathematical epidemiology. He has published extensively on mathematical modeling of infectious diseases including COVID-19, TB, malaria, and HIV/AIDS. He has supervised numerous PhD and MSc students and serves as a reviewer for several international journals.",
        "education_details": [
            {"degree": "Ph.D. in Applied Mathematics", "institution": "Adama Science and Technology University", "year": "2015"},
            {"degree": "M.Sc. in Mathematics", "institution": "Addis Ababa University", "year": "2008"},
            {"degree": "B.Sc. in Mathematics", "institution": "Addis Ababa University", "year": "2005"}
        ]
    },
    
    # ===== RESEARCHER 8: Dr. Simon Derkee Zawka =====
    "researcher_8": {
        "id": "A008",
        "name": "Dr. Simon Derkee Zawka",
        "title": "Associate Professor of Mathematics / Director for Publication, Documentation and Dissemination",
        "institution": "Arba Minch University",
        "department": "Department of Mathematics",
        "education": "Ph.D. in Mathematics, Andhra University, India (2018)",
        "profile_image": "🌿📊🧮",
        "research_interests": "Mathematical Bioeconomics, Mathematical Biology, Mathematical Modeling, Optimal Control, Dynamical Systems, Mathematical Ecology, Renewable Resource Management, Pollution Control, Harvesting Strategies, Prey-Predator Systems, Marine Protected Areas, Ecotourism, Fisheries Management",
        "research_keywords": ["Mathematical Bioeconomics", "Mathematical Biology", "Optimal Control", "Dynamical Systems", "Mathematical Modeling", "Renewable Resource Management", "Pollution Control", "Harvesting Strategies", "Prey-Predator Systems", "Marine Protected Areas", "Fisheries Management"],
        "specializations": [
            {"area": "Mathematical Bioeconomics", "level": 5},
            {"area": "Mathematical Biology", "level": 5},
            {"area": "Optimal Control", "level": 5},
            {"area": "Dynamical Systems", "level": 5},
            {"area": "Mathematical Modeling", "level": 5},
            {"area": "Mathematical Ecology", "level": 4}
        ],
        "publications": [
            "Optimal harvesting of a renewable resource in a polluted environment: An allocation problem of the sole owner (2019) - Natural Resource Modeling, 32(2), e12206",
            "Marine protected areas for resilience and economic development (2023) - Aquatic Living Resources, 36, 22",
            "Renewable resource management in a seasonally fluctuating environment with restricted harvesting effort (2018) - Mathematical Biosciences, 301, 1-9",
            "Existence and optimal harvesting of two competing species in a polluted environment with pollution reduction effect (2021) - Journal of Mathematical Modeling, 9(4), 517-536",
            "Optimal effort, fish farming, and marine reserve in fisheries management (2024) - Aquaculture and Fisheries, 9(6), 975-980",
            "Influence of investing in treating a polluted environment on the harvest: A problem of optimal allocation (2019) - Journal of Biological Systems, 27(02), 257-279",
            "Deep Koopman-based reachability analysis for data-driven predictive control of unknown nonlinear systems (2025) - IFAC Journal of Systems and Control",
            "Bio-Economics of a Renewable Resource in the Presence of Pollution: The Problem of Optimal Effort Allocation (2020) - Nonlinear Dyn. Syst. Theory, 20(5), 552-567",
            "Dynamics and optimal harvesting of prey–predator in a polluted environment in the presence of scavenger and pollution control (2023) - Mathematics Open, 2, 2350004",
            "The impact of pollution reduction on the optimal harvesting strategy in a seasonally changing and polluted environment (2024) - Mathematics in Applied Sciences and Engineering, 5(2), 165-184",
            "Optimal harvesting for a single-species population governed by Gompertz law: Influence of environmental fluctuation and limited harvesting capacity (2019) - International Journal of Biomathematics, 12(02), 1950018",
            "Optimizing shellfish aquaculture in nitrogen and fisheries management (2025) - Mathematical Modelling and Numerical Simulation with Applications, 5(1), 18-37",
            "Diversity and ecotourism on multipurpose marine protected areas (2024) - Mathematics in Applied Sciences and Engineering, 5(4), 329-342",
            "Optimal management of a prey-predator system in a polluted environment with effort shared between pollution reduction and harvesting (2024) - TWMS Journal of Applied and Engineering Mathematics",
            "Global behavior of solutions for periodic differential equations involving polynomial factors with applications to population dynamics (2017) - Functional Differential Equations, 23(3-4), 153-174"
        ],
        "supervisory_capacity": 5,
        "current_students": 4,
        "completed_phds": 2,
        "available_for_collaboration": True,
        "collaboration_types": ["Research Supervision", "Joint Research", "Consultancy", "Peer Review"],
        "phd_students_completed": [
            {"name": "Student 1", "year": "2022", "topic": "Mathematical Bioeconomics"},
            {"name": "Student 2", "year": "2024", "topic": "Optimal Control in Ecology"}
        ],
        "email": "simon.zawka@amu.edu.et",
        "phone": "+251 913 456 789",
        "orcid_id": "0000-0002-8814-5516",
        "orcid_url": "https://orcid.org/0000-0002-8814-5516",
        "researchgate_url": "https://www.researchgate.net/profile/Simon-Zawka",
        "google_scholar_url": "https://scholar.google.com/citations?user=4zYjiDQAAAAJ&hl=en",
        "scopus_url": "",
        "institutional_id": "AMU/MATH/008",
        "h_index": 4,
        "total_citations": 49,
        "trust_score": 85,
        "last_verified": "2026-08-09",
        "verification_badges": ["ORCID", "ResearchGate", "Google Scholar", "PhD", "Associate Professor", "Director", "20+ Publications"],
        "top_co_authors": [
            {"name": "Prof. P. D. N. Srinivasu", "institution": "Andhra University, India"},
            {"name": "Dr. Surafel Luleseged Tilahun", "institution": "Addis Ababa Science and Technology University"},
            {"name": "Dr. Abebe Geletu", "institution": "AIMS Rwanda"},
            {"name": "Dr. Teketel Ketema", "institution": "Mekdela Amba University"},
            {"name": "Worku T. Bitew", "institution": "State University of New York at Farmingdale"},
            {"name": "Prof. Seshadev Padhi", "institution": "Birla Institute of Technology"}
        ],
        "collaborating_institutions": ["Andhra University (India)", "Arba Minch University", "Addis Ababa Science and Technology University", "AIMS Rwanda", "State University of New York at Farmingdale", "Birla Institute of Technology"],
        "professional_memberships": ["Ethiopian Mathematical Association", "African Mathematical Union"],
        "biography": "Dr. Simon Derkee Zawka is an Associate Professor of Mathematics at Arba Minch University (AMU) in Ethiopia. He earned his BSc in Mathematics from Arba Minch University, his MSc in Mathematics from Addis Ababa University, and his PhD in Mathematics from Andhra University, India. His research interests lie in mathematical bioeconomics, mathematical biology, mathematical modeling, optimal control, and dynamical systems. He has served as Head of the Department of Mathematics and currently directs the Publication, Documentation, and Dissemination Directorate at AMU. He has published extensively in internationally reputable journals on renewable resource management, pollution control, harvesting strategies, and ecological modeling.",
        "education_details": [
            {"degree": "Ph.D. in Mathematics", "institution": "Andhra University, India", "year": "2018"},
            {"degree": "M.Sc. in Mathematics", "institution": "Addis Ababa University", "year": "2010"},
            {"degree": "B.Sc. in Applied Mathematics", "institution": "Arba Minch University", "year": "2007"}
        ]
    }
}

# ===================================================================
# FORUM FUNCTIONS - NEW
# ===================================================================

def create_forum_post(title, content, author, tags=[]):
    post = {
        "id": len(st.session_state.forum_posts) + 1,
        "title": title,
        "content": content,
        "author": author,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "tags": [t.strip() for t in tags.split(",")] if tags else [],
        "comments": [],
        "likes": 0,
        "views": 0
    }
    st.session_state.forum_posts.append(post)
    add_notification(f"📝 New forum post: '{title}' by {author}", "info")
    return post

def add_comment_to_post(post_id, author, content):
    for post in st.session_state.forum_posts:
        if post["id"] == post_id:
            comment = {
                "author": author,
                "content": content,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            post["comments"].append(comment)
            add_notification(f"💬 New comment on '{post['title']}' by {author}", "info")
            break

def like_post(post_id):
    for post in st.session_state.forum_posts:
        if post["id"] == post_id:
            post["likes"] += 1
            break

# ===================================================================
# NOTIFICATION FUNCTIONS - NEW
# ===================================================================

def show_notification_center():
    unread = len([n for n in st.session_state.notifications if not n.get('read', False)])
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### 🔔 Notifications")
        if unread > 0:
            st.warning(f"📌 {unread} new notification(s)")
    with col2:
        if st.button("Mark All Read"):
            for n in st.session_state.notifications:
                n['read'] = True
            st.rerun()
    
    if st.session_state.notifications:
        for note in reversed(st.session_state.notifications[-10:]):
            unread_class = "unread" if not note.get('read', False) else ""
            st.markdown(f"""
            <div class="notification-item {unread_class}">
                <strong>{note['message']}</strong>
                <div class="notification-time">⏱ {note['time']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No notifications")

# ===================================================================
# FUNCTIONS - ORIGINAL
# ===================================================================

@st.cache_data
def load_data():
    academicians_data = []
    for key, prof in RESEARCHER_PROFILES.items():
        academician = {
            "id": prof["id"],
            "name": prof["name"],
            "title": prof["title"],
            "institution": prof["institution"],
            "department": prof["department"],
            "education": prof["education"],
            "specializations": prof["specializations"],
            "publications": prof["publications"],
            "supervisory_capacity": prof["supervisory_capacity"],
            "current_students": prof["current_students"],
            "completed_phds": prof.get("completed_phds", 0),
            "email": prof["email"],
            "phone": prof.get("phone", "Not publicly available"),
            "research_interests": prof["research_interests"],
            "available_for_collaboration": prof.get("available_for_collaboration", True),
            "collaboration_types": prof.get("collaboration_types", ["Research Supervision", "Joint Research"]),
            "profile_image": prof["profile_image"],
            "research_keywords": prof["research_keywords"],
            "orcid_id": prof.get("orcid_id", ""),
            "orcid_url": prof.get("orcid_url", ""),
            "researchgate_url": prof.get("researchgate_url", ""),
            "google_scholar_url": prof.get("google_scholar_url", ""),
            "scopus_url": prof.get("scopus_url", ""),
            "h_index": prof.get("h_index", 0),
            "total_citations": prof.get("total_citations", 0),
            "trust_score": prof.get("trust_score", 0),
            "last_verified": prof.get("last_verified", "2026-08-06"),
            "verification_badges": prof.get("verification_badges", []),
            "biography": prof.get("biography", "")
        }
        academicians_data.append(academician)
    
    students_data = [
        {"id": "S001", "name": "Abebe Kebede", "research_proposal": "Mathematical modeling of infectious disease spread", "field_of_interest": "Applied Mathematics", "degree_background": "MSc in Mathematics", "email": "abebe.kebede@amu.edu.et", "institution": "Arba Minch University"},
        {"id": "S002", "name": "Tigist Worku", "research_proposal": "Solar energy optimization for rural electrification", "field_of_interest": "Electrical Engineering", "degree_background": "MSc in Electrical Engineering", "email": "tigist.worku@aau.edu.et", "institution": "Addis Ababa University"},
        {"id": "S003", "name": "Fasil Hailu", "research_proposal": "Water resource management for drought-prone regions", "field_of_interest": "Civil Engineering", "degree_background": "MSc in Hydraulic Engineering", "email": "fasil.hailu@bdu.edu.et", "institution": "Bahir Dar University"},
        {"id": "S004", "name": "Meron Tekle", "research_proposal": "Machine learning for crop yield prediction", "field_of_interest": "Computer Science", "degree_background": "MSc in Computer Science", "email": "meron.tekle@ju.edu.et", "institution": "Jimma University"},
        {"id": "S005", "name": "Yonas Desta", "research_proposal": "Climate-smart agricultural practices", "field_of_interest": "Agricultural Science", "degree_background": "MSc in Agriculture", "email": "yonas.desta@hu.edu.et", "institution": "Hawassa University"},
        {"id": "S006", "name": "Hiwot Getachew", "research_proposal": "Epidemiological modeling of non-communicable diseases", "field_of_interest": "Public Health", "degree_background": "MPH in Epidemiology", "email": "hiwot.getachew@aau.edu.et", "institution": "Addis Ababa University"},
        {"id": "S007", "name": "Dawit Eshetu", "research_proposal": "Control system design for automated irrigation", "field_of_interest": "Electrical Engineering", "degree_background": "MSc in Control Engineering", "email": "dawit.eshetu@bdu.edu.et", "institution": "Bahir Dar University"},
        {"id": "S008", "name": "Sara Mohammed", "research_proposal": "Natural language processing for Amharic language", "field_of_interest": "Computer Science", "degree_background": "MSc in Computer Science", "email": "sara.mohammed@ju.edu.et", "institution": "Jimma University"},
        {"id": "S009", "name": "Henok Amanuel", "research_proposal": "Industrial engineering optimization of manufacturing processes", "field_of_interest": "Mechanical Engineering", "degree_background": "MSc in Industrial Engineering", "email": "henok.amanuel@aau.edu.et", "institution": "Addis Ababa University"},
        {"id": "S010", "name": "Beza Tadesse", "research_proposal": "Computational modeling of renewable energy materials", "field_of_interest": "Physics", "degree_background": "MSc in Physics", "email": "beza.tadesse@bdu.edu.et", "institution": "Bahir Dar University"}
    ]

    return pd.DataFrame(academicians_data), pd.DataFrame(students_data)

def search_academicians(academicians_df, search_query, search_type):
    if not search_query:
        return academicians_df
    
    search_query = search_query.lower()
    
    if search_type == "Name":
        return academicians_df[academicians_df['name'].str.lower().str.contains(search_query, na=False)]
    elif search_type == "Research Area":
        return academicians_df[academicians_df['research_interests'].str.lower().str.contains(search_query, na=False)]
    elif search_type == "Institution":
        return academicians_df[academicians_df['institution'].str.lower().str.contains(search_query, na=False)]
    elif search_type == "Keyword":
        mask = academicians_df['research_keywords'].apply(
            lambda x: any(search_query in kw.lower() for kw in x) if isinstance(x, list) else False
        )
        return academicians_df[mask]
    else:
        mask = (
            academicians_df['name'].str.lower().str.contains(search_query, na=False) |
            academicians_df['institution'].str.lower().str.contains(search_query, na=False) |
            academicians_df['research_interests'].str.lower().str.contains(search_query, na=False)
        )
        return academicians_df[mask]

def generate_request_letter(student_name, student_institution, professor_name, professor_title, 
                           professor_institution, research_topic, request_type, 
                           student_email, student_phone):
    date = datetime.now().strftime("%B %d, %Y")
    
    if request_type == "Research Supervision":
        subject = f"Request for PhD Supervision - {student_name}"
        body = f"I am writing to formally request your consideration to serve as my PhD supervisor. I am currently pursuing my doctoral studies at {student_institution}. My research focuses on: {research_topic}"
    else:
        subject = f"Request for Collaboration - {student_name}"
        body = f"I am writing to propose a collaboration between {student_institution} and {professor_institution}. My research involves: {research_topic}"
    
    return {
        'date': date,
        'from_address': f"{student_name}\\n{student_institution}\\n{student_email}",
        'to_address': f"{professor_name}\\n{professor_title}\\n{professor_institution}",
        'subject': subject,
        'body': body
    }

# ===================================================================
# LOGIN PAGE - ORIGINAL
# ===================================================================

def show_login_page():
    """Display the login page"""
    init_user_db()
    
    st.markdown("""
    <div style="text-align:center; padding:1rem 0;">
        <div style="font-size:4rem; margin-bottom:0.5rem;">🌿🇪🇹🎉</div>
        <h1 style="font-size:3rem; margin:0;">Research Collaboration Portal</h1>
        <p style="color:#5F6368; font-size:1.2rem; margin-top:0.5rem;">Sign in to access the Ethiopian Research Network</p>
        <p style="color:#5F6368; font-size:1rem; margin-top:0.3rem;">Please register first if you don't have an account</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs for Login and Register
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    with tab1:
        with st.container():
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            
            # Login form
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
                        success, message = login_user(username, password)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
            
            # Contact support info
            st.markdown("""
            <div style="text-align:center; margin-top:1.5rem; padding-top:1rem; border-top:1px solid #E8EAED;">
                <p style="color:#5F6368; font-size:0.9rem; margin:0;">
                    📧 For support, contact: <b style="color:#1A73E8;">berhanu.mekonen@amu.edu.et</b>
                </p>
                <p style="color:#5F6368; font-size:0.9rem; margin:0;">
                    📞 Phone: <b style="color:#1A73E8;">+251 905 527 481</b>
                </p>
                <p style="color:#5F6368; font-size:0.85rem; margin-top:0.5rem;">
                    ⚠️ No default accounts. Please register first.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        with st.container():
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            
            st.markdown("""
            <div style="text-align:center; margin-bottom:1.5rem;">
                <h3 style="margin:0; color:#1A73E8;">Create New Account</h3>
                <p style="color:#5F6368; font-size:0.95rem;">Join the Ethiopian Research Network</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Registration form
            with st.form("register_form"):
                new_username = st.text_input("📧 Email Address *", placeholder="your.name@amu.edu.et", help="Must end with @amu.edu.et")
                new_password = st.text_input("🔒 Create Password *", type="password", placeholder="Minimum 6 characters", help="Password must be at least 6 characters long")
                confirm_password = st.text_input("✅ Confirm Password *", type="password", placeholder="Re-enter your password")
                
                st.markdown("""
                <div style="color:#5F6368; font-size:0.85rem; margin:0.5rem 0;">
                    <span>📋 Username must be your AMU email address (e.g., <b>your.name@amu.edu.et</b>)</span>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    submitted = st.form_submit_button("Create Account", use_container_width=True)
                
                if submitted:
                    if not new_username or not new_password or not confirm_password:
                        st.error("❌ Please fill in all fields.")
                    else:
                        success, message = register_user(new_username, new_password, confirm_password)
                        if success:
                            st.success(message)
                            st.info("✅ You can now go to the Login tab and sign in with your credentials.")
                        else:
                            st.error(message)
            
            st.markdown('</div>', unsafe_allow_html=True)

# ===================================================================
# MAIN APPLICATION - ORIGINAL WITH NEW FEATURES
# ===================================================================

def main():
    # Initialize authentication state
    init_user_db()
    
    # Show login page if not logged in
    if not st.session_state.logged_in:
        show_login_page()
        return
    
    # If logged in, show the main application
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
    
    # Get current user info
    current_user = st.session_state.current_user
    user_display_name = current_user.split('@')[0].replace('.', ' ').title() if current_user else "User"
    
    # SIDEBAR - ORIGINAL WITH NAVIGATION
    with st.sidebar:
        st.markdown("### Research Portal")
        st.markdown("---")
        
        # User info in sidebar
        st.markdown(f"""
        <div style="background:#E8F0FE;padding:1rem;border-radius:12px;margin-bottom:1rem;">
            <p style="margin:0;font-weight:600;color:#1A73E8;">👤 {user_display_name}</p>
            <p style="margin:0;font-size:0.85rem;color:#5F6368;">{current_user}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Notification count
        unread = len([n for n in st.session_state.notifications if not n.get('read', False)])
        nav_options = ["🏠 Home", "🔍 Find Researchers", "💬 Forum", "📊 Analytics", "📋 My Requests"]
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
        st.markdown("*Dr. Berhanu Mekonen (PhD), Arba Minch University, August 4, 2026*")
    
    # SHOW ABOUT PAGE
    if st.session_state.show_about:
        show_about_page()
        return
    
    # Get current page
    current_page = getattr(st.session_state, 'current_page', "🏠 Home")
    
    # HEADER - ORIGINAL WITH NATURE BACKGROUND
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
                        🌿🇪🇹🎉 <span class="highlight-name">Dr. Berhanu Mekonen (PhD)</span> · 
                        <span class="highlight-institution">Arba Minch University</span> · 
                        August 4, 2026
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
                <!-- Research Dropdown Button -->
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
    
    # STATUS BAR - ORIGINAL
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
    # PAGE: HOME / FIND RESEARCHERS - ORIGINAL
    # ===================================================================
    if current_page == "🏠 Home" or current_page == "🔍 Find Researchers":
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
                                {"".join(f'<span class="badge-collab">{t}</span>' for t in prof.get('collaboration_types', []))}
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
    
    # ===================================================================
    # PAGE: REQUEST COLLABORATION - ORIGINAL
    # ===================================================================
    if current_page == "📋 My Requests" or st.session_state.selected_professor:
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
                    requester_institution = st.text_input("Institution *", value="Arba Minch University")
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
        
        # Show existing requests
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
    
    # ===================================================================
    # PAGE: FORUM - NEW
    # ===================================================================
    if current_page == "💬 Forum":
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
                            {"".join(f'<span class="tag">#{tag}</span>' for tag in post['tags'])}
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
    
    # ===================================================================
    # PAGE: NOTIFICATIONS - NEW
    # ===================================================================
    if "📨 Notifications" in current_page:
        show_notification_center()
    
    # ===================================================================
    # PAGE: ANALYTICS - NEW
    # ===================================================================
    if current_page == "📊 Analytics":
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
                fig = px.bar(df_pub, 
                            x='name', 
                            y='publications',
                            title='Publications by Researcher',
                            color='publications',
                            color_continuous_scale='Greens',
                            text='publications')
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig2 = px.scatter(df_pub,
                                 x='publications',
                                 y='citations',
                                 size='h_index',
                                 text='name',
                                 title='Publications vs Citations',
                                 color='trust_score',
                                 color_continuous_scale='Viridis')
                fig2.update_layout(height=400)
                st.plotly_chart(fig2, use_container_width=True)
            
            col3, col4 = st.columns(2)
            
            with col3:
                fig3 = px.bar(df_pub,
                            x='name',
                            y='h_index',
                            title='h-index by Researcher',
                            color='h_index',
                            color_continuous_scale='Blues',
                            text='h_index')
                fig3.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig3, use_container_width=True)
            
            with col4:
                fig4 = px.bar(df_pub,
                            x='name',
                            y='trust_score',
                            title='Trust Score by Researcher',
                            color='trust_score',
                            color_continuous_scale='Oranges',
                            text='trust_score')
                fig4.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig4, use_container_width=True)
            
            st.markdown("#### 📊 Summary Statistics")
            col5, col6, col7, col8 = st.columns(4)
            
            with col5:
                st.metric("Total Publications", df_pub['publications'].sum())
            with col6:
                st.metric("Total Citations", df_pub['citations'].sum())
            with col7:
                st.metric("Average h-index", f"{df_pub['h_index'].mean():.1f}")
            with col8:
                st.metric("Average Trust Score", f"{df_pub['trust_score'].mean():.1f}%")

if __name__ == "__main__":
    main()
