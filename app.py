# ============================================================
# FILE: app.py
# PURPOSE: AI-Powered ATS Resume Checker with Beautiful UI
# FIXED: Session state conflict issue
# ============================================================

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd
import json
from utils.resume_parser import ResumeParser
from utils.ats_scorer import ATSScorer
from utils.pdf_generator import PDFReportGenerator
from utils.text_processor import TextProcessor
import base64
import os
import time

# Page configuration
st.set_page_config(
    page_title="AI-Powered ATS Resume Checker",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# BEAUTIFUL CUSTOM CSS - 3D Effects, Glassmorphism, Animations
# ============================================================
st.markdown("""
<style>
    /* ===== IMPORT GOOGLE FONTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700&display=swap');
    
    /* ===== GLOBAL STYLES ===== */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* ===== MAIN BACKGROUND ===== */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        background-attachment: fixed;
    }
    
    /* ===== ANIMATED BACKGROUND PARTICLES ===== */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.2) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(120, 200, 255, 0.2) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
    }
    
    /* ===== HIDE STREAMLIT BRANDING ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ===== MAIN HEADER - 3D EFFECT ===== */
    .main-header {
        text-align: center;
        padding: 2.5rem 2rem;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 
            0 20px 60px rgba(102, 126, 234, 0.4),
            0 0 40px rgba(118, 75, 162, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
        animation: headerGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes headerGlow {
        0% { box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4), 0 0 40px rgba(118, 75, 162, 0.3); }
        100% { box-shadow: 0 25px 70px rgba(102, 126, 234, 0.6), 0 0 60px rgba(118, 75, 162, 0.5); }
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent 30%,
            rgba(255, 255, 255, 0.1) 50%,
            transparent 70%
        );
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) rotate(45deg); }
        100% { transform: translateX(100%) rotate(45deg); }
    }
    
    .main-header h1 {
        color: #ffffff;
        font-family: 'Orbitron', sans-serif;
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 
            0 0 20px rgba(255, 255, 255, 0.5),
            0 0 40px rgba(255, 255, 255, 0.3),
            0 4px 8px rgba(0, 0, 0, 0.3);
        letter-spacing: 2px;
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
        position: relative;
        z-index: 1;
    }
    
    /* ===== GLASSMORPHISM CARDS ===== */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 
            0 15px 40px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    /* ===== 3D SCORE CARDS ===== */
    .score-card-3d {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 
            0 25px 50px rgba(0, 0, 0, 0.3),
            0 0 0 1px rgba(255, 255, 255, 0.1) inset;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .score-card-3d::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #667eea);
        background-size: 200% 100%;
        animation: gradientMove 3s linear infinite;
    }
    
    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }
    
    .score-card-3d:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 
            0 35px 60px rgba(0, 0, 0, 0.4),
            0 0 30px rgba(102, 126, 234, 0.3);
    }
    
    .score-value {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 30px rgba(102, 126, 234, 0.5);
        margin: 0.5rem 0;
    }
    
    .score-label {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* ===== ISSUE CARDS - 3D RED THEME ===== */
    .issue-card {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.2) 0%, rgba(238, 90, 90, 0.1) 100%);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.2rem 1.5rem;
        margin: 0.8rem 0;
        border-left: 4px solid #ff6b6b;
        border: 1px solid rgba(255, 107, 107, 0.3);
        box-shadow: 
            0 10px 30px rgba(255, 107, 107, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .issue-card::before {
        content: '⚠️';
        position: absolute;
        right: 15px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.5rem;
        opacity: 0.3;
    }
    
    .issue-card:hover {
        transform: translateX(5px);
        box-shadow: 
            0 15px 40px rgba(255, 107, 107, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }
    
    .issue-card p {
        color: #ffffff;
        font-size: 0.95rem;
        margin: 0;
        font-weight: 500;
        padding-right: 40px;
    }
    
    /* ===== SUGGESTION CARDS - 3D GREEN/GOLD THEME ===== */
    .suggestion-card {
        background: linear-gradient(135deg, rgba(253, 203, 110, 0.2) 0%, rgba(255, 234, 167, 0.1) 100%);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.2rem 1.5rem;
        margin: 0.8rem 0;
        border-left: 4px solid #fdcb6e;
        border: 1px solid rgba(253, 203, 110, 0.3);
        box-shadow: 
            0 10px 30px rgba(253, 203, 110, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .suggestion-card::before {
        content: '💡';
        position: absolute;
        right: 15px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.5rem;
        opacity: 0.5;
    }
    
    .suggestion-card:hover {
        transform: translateX(5px);
        box-shadow: 
            0 15px 40px rgba(253, 203, 110, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }
    
    .suggestion-card p {
        color: #ffffff;
        font-size: 0.95rem;
        margin: 0;
        font-weight: 500;
        padding-right: 40px;
    }
    
    /* ===== KEYWORD CHIPS - 3D STYLE ===== */
    .keyword-chip {
        display: inline-block;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%);
        color: #ffffff;
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        margin: 0.3rem;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 
            0 5px 15px rgba(102, 126, 234, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        cursor: default;
    }
    
    .keyword-chip:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 
            0 10px 25px rgba(102, 126, 234, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }
    
    .keyword-chip.missing {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.3) 0%, rgba(238, 90, 90, 0.2) 100%);
        border-color: rgba(255, 107, 107, 0.3);
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.2);
    }
    
    .keyword-chip.matched {
        background: linear-gradient(135deg, rgba(0, 206, 201, 0.3) 0%, rgba(85, 239, 196, 0.2) 100%);
        border-color: rgba(0, 206, 201, 0.3);
        box-shadow: 0 5px 15px rgba(0, 206, 201, 0.2);
    }
    
    /* ===== SECTION HEADERS ===== */
    .section-header {
        color: #ffffff;
        font-family: 'Poppins', sans-serif;
        font-size: 1.8rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid transparent;
        background: linear-gradient(90deg, rgba(102, 126, 234, 0.5), transparent) border-box;
        position: relative;
    }
    
    .section-header::before {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100px;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 3px;
    }
    
    /* ===== FILE UPLOADER STYLING ===== */
    .stFileUploader > div {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border: 2px dashed rgba(102, 126, 234, 0.5);
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div:hover {
        border-color: rgba(102, 126, 234, 0.8);
        background: rgba(102, 126, 234, 0.1);
    }
    
    /* ===== TEXT AREA STYLING ===== */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        color: #ffffff !important;
        font-size: 0.95rem !important;
        padding: 1rem !important;
    }
    
    .stTextArea textarea:focus {
        border-color: rgba(102, 126, 234, 0.8) !important;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stTextArea textarea::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    /* ===== BUTTON STYLING - 3D EFFECT ===== */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 15px;
        box-shadow: 
            0 10px 30px rgba(102, 126, 234, 0.4),
            0 0 0 1px rgba(255, 255, 255, 0.1) inset;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 
            0 20px 40px rgba(102, 126, 234, 0.5),
            0 0 30px rgba(118, 75, 162, 0.4),
            0 0 0 1px rgba(255, 255, 255, 0.2) inset;
    }
    
    .stButton > button:active {
        transform: translateY(-2px) scale(1);
    }
    
    /* ===== SIDEBAR STYLING ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(26, 26, 46, 0.95) 0%, rgba(22, 33, 62, 0.95) 100%);
        backdrop-filter: blur(20px);
    }
    
    [data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }
    
    .sidebar-header {
        color: #ffffff;
        font-family: 'Orbitron', sans-serif;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(102, 126, 234, 0.5);
    }
    
    .sidebar-info {
        background: rgba(102, 126, 234, 0.1);
        border-radius: 15px;
        padding: 1rem;
        border: 1px solid rgba(102, 126, 234, 0.3);
        margin-bottom: 1rem;
    }
    
    .sidebar-info p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }
    
    /* ===== DATAFRAME STYLING ===== */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        overflow: hidden;
    }
    
    /* ===== EXPANDER STYLING ===== */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        color: #ffffff !important;
    }
    
    /* ===== SUCCESS/ERROR/INFO MESSAGES ===== */
    .stSuccess {
        background: linear-gradient(135deg, rgba(0, 206, 201, 0.2) 0%, rgba(85, 239, 196, 0.1) 100%);
        border: 1px solid rgba(0, 206, 201, 0.3);
        border-radius: 10px;
        color: #ffffff;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.2) 0%, rgba(238, 90, 90, 0.1) 100%);
        border: 1px solid rgba(255, 107, 107, 0.3);
        border-radius: 10px;
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 10px;
    }
    
    /* ===== DIVIDER ===== */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.5), transparent);
        margin: 2rem 0;
    }
    
    /* ===== METRIC STYLING ===== */
    [data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif;
        color: #667eea;
    }
    
    /* ===== CUSTOM SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #667eea);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# INITIALIZE SESSION STATE - FIXED VERSION
# ============================================================
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'results' not in st.session_state:
    st.session_state.results = None
if 'resume_filename' not in st.session_state:
    st.session_state.resume_filename = None
if 'jd_text' not in st.session_state:  # CHANGED: Use different name
    st.session_state.jd_text = None

# ============================================================
# CHART FUNCTIONS
# ============================================================
def create_gauge_chart(score, title):
    """Create a beautiful gauge chart for scores"""
    if score >= 70:
        bar_color = "#00cec9"
    elif score >= 40:
        bar_color = "#fdcb6e"
    else:
        bar_color = "#ff6b6b"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={
            'text': f"<b>{title}</b>",
            'font': {'size': 18, 'color': '#ffffff', 'family': 'Poppins'}
        },
        number={
            'font': {'size': 50, 'color': '#ffffff', 'family': 'Orbitron'},
            'suffix': '%'
        },
        gauge={
            'axis': {
                'range': [None, 100],
                'tickwidth': 2,
                'tickcolor': "rgba(255,255,255,0.3)",
                'tickfont': {'color': 'rgba(255,255,255,0.7)'}
            },
            'bar': {'color': bar_color, 'thickness': 0.75},
            'bgcolor': "rgba(255,255,255,0.1)",
            'borderwidth': 2,
            'bordercolor': "rgba(255,255,255,0.2)",
            'steps': [
                {'range': [0, 40], 'color': 'rgba(255, 107, 107, 0.3)'},
                {'range': [40, 70], 'color': 'rgba(253, 203, 110, 0.3)'},
                {'range': [70, 100], 'color': 'rgba(0, 206, 201, 0.3)'}
            ],
            'threshold': {
                'line': {'color': "#ffffff", 'width': 4},
                'thickness': 0.8,
                'value': score
            }
        }
    ))
    
    fig.update_layout(
        height=280,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#ffffff'}
    )
    
    return fig

def create_radar_chart(scores_dict):
    """Create a beautiful radar chart for score breakdown"""
    categories = list(scores_dict.keys())
    values = list(scores_dict.values())
    
    categories = categories + [categories[0]]
    values = values + [values[0]]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(102, 126, 234, 0.3)',
        line=dict(color='#667eea', width=3),
        marker=dict(size=8, color='#ffffff', line=dict(color='#667eea', width=2)),
        name='Your Score'
    ))
    
    ref_values = [70] * len(categories)
    fig.add_trace(go.Scatterpolar(
        r=ref_values,
        theta=categories,
        line=dict(color='rgba(0, 206, 201, 0.5)', width=2, dash='dash'),
        name='Target (70%)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color='rgba(255,255,255,0.7)', size=10),
                gridcolor='rgba(255,255,255,0.1)',
                linecolor='rgba(255,255,255,0.2)'
            ),
            angularaxis=dict(
                tickfont=dict(color='#ffffff', size=12, family='Poppins'),
                gridcolor='rgba(255,255,255,0.1)',
                linecolor='rgba(255,255,255,0.2)'
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=True,
        legend=dict(
            font=dict(color='#ffffff'),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=450,
        margin=dict(l=80, r=80, t=40, b=40)
    )
    
    return fig

# ============================================================
# MAIN APPLICATION
# ============================================================
def main():
    """Main application function"""
    
    # ===== HEADER =====
    st.markdown("""
        <div class="main-header">
            <h1>🚀 AI-Powered ATS Resume Checker</h1>
            <p>Optimize your resume for Applicant Tracking Systems with AI-powered analysis</p>
        </div>
    """, unsafe_allow_html=True)
    
    # ===== SIDEBAR =====
    with st.sidebar:
        st.markdown('<p class="sidebar-header">📋 About This Tool</p>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="sidebar-info">
            <p>🎯 <strong>Check ATS Compatibility</strong></p>
            <p>📊 <strong>Get Detailed Scoring</strong></p>
            <p>💡 <strong>Receive AI Suggestions</strong></p>
            <p>📈 <strong>Understand Rejection Reasons</strong></p>
            <p>📄 <strong>Download PDF Reports</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<p class="sidebar-header">🎯 How It Works</p>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="sidebar-info">
            <p><strong>1.</strong> Upload your resume (PDF/DOCX)</p>
            <p><strong>2.</strong> Paste the job description</p>
            <p><strong>3.</strong> Click 'Analyze Resume'</p>
            <p><strong>4.</strong> Review scores & suggestions</p>
            <p><strong>5.</strong> Download detailed report</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown('<p class="sidebar-header">⚡ Quick Stats</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Analyses", "1,234+", "+12%")
        with col2:
            st.metric("Success Rate", "89%", "+5%")
    
    # ===== MAIN CONTENT =====
    st.markdown('<p class="section-header">📤 Upload Your Resume & Job Description</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #ffffff; margin-bottom: 1rem;">📄 Resume Upload</h3>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Drag and drop your resume here",
            type=['pdf', 'docx', 'txt'],
            help="Supported formats: PDF, DOCX, TXT"
        )
        
        if uploaded_file is not None:
            st.success(f"✅ File uploaded successfully: **{uploaded_file.name}**")
            
            with st.expander("👁️ Preview Resume Content"):
                try:
                    parser = ResumeParser()
                    resume_text = parser.extract_text(uploaded_file)
                    preview_text = resume_text[:1500] + "..." if len(resume_text) > 1500 else resume_text
                    st.text_area("Preview", preview_text, height=250, disabled=True, label_visibility="collapsed")
                except Exception as e:
                    st.error(f"Error reading file: {e}")
    
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #ffffff; margin-bottom: 1rem;">📝 Job Description</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # FIXED: Removed the key parameter to avoid session state conflict
        job_description = st.text_area(
            "Paste the complete job description",
            height=280,
            placeholder="Copy and paste the job description here...\n\nInclude:\n• Job requirements\n• Required skills\n• Qualifications\n• Responsibilities"
        )
    
    # ===== ANALYZE BUTTON =====
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_button = st.button(
            "🔍 ANALYZE RESUME",
            type="primary",
            use_container_width=True
        )
    
    # ===== ANALYSIS LOGIC =====
    if analyze_button:
        if uploaded_file and job_description:
            
            progress_placeholder = st.empty()
            status_placeholder = st.empty()
            
            with progress_placeholder.container():
                progress_bar = st.progress(0)
                
            steps = [
                ("🔄 Extracting resume content...", 15),
                ("📝 Parsing document structure...", 30),
                ("🔍 Analyzing keywords...", 45),
                ("🎯 Matching skills...", 60),
                ("📊 Calculating scores...", 75),
                ("💡 Generating suggestions...", 90),
                ("✅ Finalizing report...", 100)
            ]
            
            for status, progress in steps:
                status_placeholder.markdown(f"""
                <div style="text-align: center; color: #ffffff; font-size: 1.1rem;">
                    {status}
                </div>
                """, unsafe_allow_html=True)
                progress_bar.progress(progress)
                time.sleep(0.3)
            
            progress_placeholder.empty()
            status_placeholder.empty()
            
            try:
                parser = ResumeParser()
                scorer = ATSScorer()
                text_processor = TextProcessor()
                
                uploaded_file.seek(0)
                resume_text = parser.extract_text(uploaded_file)
                resume_data = parser.parse_resume(resume_text)
                
                cleaned_resume = text_processor.clean_text(resume_text)
                cleaned_jd = text_processor.clean_text(job_description)
                
                results = scorer.calculate_ats_score(cleaned_resume, cleaned_jd, resume_data)
                
                # FIXED: Store results properly
                st.session_state.results = results
                st.session_state.analysis_complete = True
                st.session_state.resume_filename = uploaded_file.name
                st.session_state.jd_text = job_description  # FIXED: Use different variable name
                
                st.success("✅ Analysis completed successfully!")
                
            except Exception as e:
                st.error(f"❌ An error occurred during analysis: {str(e)}")
                st.session_state.analysis_complete = False
        else:
            st.error("⚠️ Please upload a resume and provide a job description to continue")
    
    # ===== DISPLAY RESULTS =====
    if st.session_state.analysis_complete and st.session_state.results:
        results = st.session_state.results
        
        st.markdown("---")
        
        # ===== OVERALL SCORE SECTION =====
        st.markdown('<p class="section-header">📊 Analysis Results</p>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3, gap="large")
        
        with col1:
            st.markdown("""
            <div class="score-card-3d">
                <p class="score-label">Overall ATS Score</p>
            </div>
            """, unsafe_allow_html=True)
            fig = create_gauge_chart(results['overall_score'], "")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
            <div class="score-card-3d">
                <p class="score-label">Keyword Match</p>
            </div>
            """, unsafe_allow_html=True)
            fig = create_gauge_chart(results['keyword_match_score'], "")
            st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            st.markdown("""
            <div class="score-card-3d">
                <p class="score-label">Skills Match</p>
            </div>
            """, unsafe_allow_html=True)
            fig = create_gauge_chart(results['skills_score'], "")
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # ===== DETAILED BREAKDOWN =====
        st.markdown('<p class="section-header">📈 Detailed Analysis Breakdown</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1], gap="large")
        
        with col1:
            radar_scores = {
                'Keywords': results['keyword_match_score'],
                'Skills': results['skills_score'],
                'Experience': results['experience_score'],
                'Education': results['education_score'],
                'Format': results['format_score']
            }
            fig = create_radar_chart(radar_scores)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
            <div class="glass-card">
                <h3 style="color: #ffffff; margin-bottom: 1rem;">📋 Score Breakdown</h3>
            </div>
            """, unsafe_allow_html=True)
            
            for category, score in radar_scores.items():
                if score >= 70:
                    color = "#00cec9"
                    icon = "✅"
                elif score >= 40:
                    color = "#fdcb6e"
                    icon = "⚠️"
                else:
                    color = "#ff6b6b"
                    icon = "❌"
                
                st.markdown(f"""
                <div style="
                    background: rgba(255,255,255,0.05);
                    border-radius: 10px;
                    padding: 0.8rem 1rem;
                    margin: 0.5rem 0;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    border-left: 4px solid {color};
                ">
                    <span style="color: #ffffff; font-weight: 500;">{icon} {category}</span>
                    <span style="color: {color}; font-family: 'Orbitron', sans-serif; font-weight: 700;">{score}%</span>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ===== ISSUES AND SUGGESTIONS =====
        st.markdown('<p class="section-header">🔍 Issues & Suggestions</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("""
            <div class="glass-card">
                <h3 style="color: #ff6b6b; margin-bottom: 1rem;">❌ Issues Found</h3>
            </div>
            """, unsafe_allow_html=True)
            
            issues = results.get('issues', [])
            if issues:
                for issue in issues:
                    st.markdown(f"""
                    <div class="issue-card">
                        <p>{issue}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="text-align: center; padding: 2rem; color: #00cec9;">
                    <h2>🎉</h2>
                    <p>No critical issues found!</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="glass-card">
                <h3 style="color: #fdcb6e; margin-bottom: 1rem;">💡 Suggestions for Improvement</h3>
            </div>
            """, unsafe_allow_html=True)
            
            suggestions = results.get('suggestions', [])
            if suggestions:
                for suggestion in suggestions:
                    st.markdown(f"""
                    <div class="suggestion-card">
                        <p>{suggestion}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="text-align: center; padding: 2rem; color: #00cec9;">
                    <h2>✨</h2>
                    <p>Your resume looks great!</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ===== SKILLS ANALYSIS =====
        st.markdown('<p class="section-header">🛠️ Skills Analysis</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("""
            <div class="glass-card">
                <h3 style="color: #00cec9; margin-bottom: 1rem;">✅ Matched Skills</h3>
            </div>
            """, unsafe_allow_html=True)
            
            matched_skills = results.get('matched_skills', [])
            if matched_skills:
                skills_html = ""
                for skill in matched_skills:
                    skills_html += f'<span class="keyword-chip matched">{skill}</span>'
                st.markdown(f'<div style="padding: 0.5rem;">{skills_html}</div>', unsafe_allow_html=True)
            else:
                st.info("No matching skills found")
        
        with col2:
            st.markdown("""
            <div class="glass-card">
                <h3 style="color: #ff6b6b; margin-bottom: 1rem;">❌ Missing Skills</h3>
            </div>
            """, unsafe_allow_html=True)
            
            missing_skills = results.get('missing_skills', [])
            if missing_skills:
                skills_html = ""
                for skill in missing_skills[:15]:
                    skills_html += f'<span class="keyword-chip missing">{skill}</span>'
                st.markdown(f'<div style="padding: 0.5rem;">{skills_html}</div>', unsafe_allow_html=True)
            else:
                st.success("All required skills present!")
        
        st.markdown("---")
        
        # ===== MISSING KEYWORDS =====
        st.markdown('<p class="section-header">🔑 Missing Keywords</p>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="glass-card">
            <p style="color: rgba(255,255,255,0.7); margin-bottom: 1rem;">
                These important keywords from the job description are missing from your resume:
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        missing_keywords = results.get('missing_keywords', [])
        if missing_keywords:
            keywords_html = ""
            for keyword in missing_keywords[:20]:
                keywords_html += f'<span class="keyword-chip">{keyword}</span>'
            st.markdown(f'<div style="padding: 0.5rem;">{keywords_html}</div>', unsafe_allow_html=True)
        else:
            st.success("✅ Great! All important keywords are present in your resume!")
        
        st.markdown("---")
        
        # ===== DOWNLOAD REPORT =====
        st.markdown('<p class="section-header">📥 Download Report</p>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("📄 GENERATE PDF REPORT", type="secondary", use_container_width=True):
                with st.spinner("📝 Generating your PDF report..."):
                    try:
                        pdf_gen = PDFReportGenerator()
                        pdf_buffer = pdf_gen.generate_report(
                            results,
                            st.session_state.resume_filename,
                            st.session_state.jd_text  # FIXED: Use correct variable
                        )
                        
                        b64 = base64.b64encode(pdf_buffer.getvalue()).decode()
                        filename = f"ATS_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                        
                        st.markdown(f"""
                        <div style="text-align: center; padding: 2rem;">
                            <a href="data:application/pdf;base64,{b64}" download="{filename}"
                               style="
                                   background: linear-gradient(135deg, #00cec9 0%, #55efc4 100%);
                                   color: #1a1a2e;
                                   padding: 1rem 2rem;
                                   border-radius: 15px;
                                   text-decoration: none;
                                   font-weight: 600;
                                   font-size: 1.1rem;
                                   box-shadow: 0 10px 30px rgba(0, 206, 201, 0.4);
                               ">
                                📥 Download PDF Report
                            </a>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.success("✅ Report generated successfully!")
                        
                    except Exception as e:
                        st.error(f"❌ Error generating PDF: {str(e)}")
        
        # ===== FOOTER =====
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; padding: 2rem; color: rgba(255,255,255,0.5);">
            <p>Made with ❤️ using AI | © 2024 ATS Resume Checker</p>
        </div>
        """, unsafe_allow_html=True)

# Run the application
if __name__ == "__main__":
    main()