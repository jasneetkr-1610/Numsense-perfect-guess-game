import streamlit as st
import random
import time
import plotly.express as px

#-------------PAGE CONFIG----------------
st.set_page_config(
    page_title="NUMSENSE DASHBOARD",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>
.num-header {
    text-align: center;
    padding: 20px 0 10px 0;
}
.num-title {
    font-size: 42px;
    font-weight: 800;
    color: #00D4FF;
    letter-spacing: 1px;
}
.num-tagline {
    font-size: 14px;
    color: #8B949E;
    margin-top: -5px;
}
</style>

<div class="num-header">
    <div class="num-title">NumSense</div>
    <div class="num-tagline">An Intelligent Number Guessing Dashboard</div>
</div>
<hr style="border:1px solid #30363D;">
""", unsafe_allow_html=True)


#-------------DARK THEME CSS (Updated for the "Too Low/High" Badge)----------------
st.markdown("""
<style>
    .stApp { background-color: #0F111A; color: #FFFFFF; }
    section[data-testid="stSidebar"] { background-color: #161B22 !important; border-right: 1px solid #30363D; }
    
    /* Metric Circles */
    .metric-card { background-color: #161B22; border: 1px solid #30363D; border-radius: 10px; padding: 20px; text-align: center; }
    .circle-stat { border: 4px solid #00D4FF; border-radius: 50%; width: 80px; height: 80px; margin: auto; 
                   display: flex; align-items: center; justify-content: center; font-size: 22px; font-weight: bold; 
                   color: #00D4FF; box-shadow: 0 0 10px #00D4FF; }
    
    /* Action Zone & Feedback Badge */
    .action-zone { background-color: #1c2128; border-radius: 15px; padding: 30px; text-align: center; border: 1px solid #30363D; position: relative; }
    .guess-box { font-size: 54px; font-weight: bold; background: #0D1117; border: 2px solid #5865F2; border-radius: 10px; 
                 display: inline-block; padding: 10px 40px; margin-bottom: 10px; }
    
    .feedback-badge {
        background-color: #1E88E5;
        color: white;
        padding: 8px 15px;
        border-radius: 5px;
        font-weight: bold;
        display: inline-block;
        margin-left: 10px;
        vertical-align: middle;
    }
</style>
""", unsafe_allow_html=True)

#----------------SESSION STATE----------------
if 'secret_number' not in st.session_state:
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.history = []
    st.session_state.game_over = False
    st.session_state.status = "Waiting"
    st.session_state.feedback = ""
    st.session_state.start_time = time.time()

#----------------SIDEBAR----------------------

with st.sidebar:
    st.title("🎯 Settings")
    st.subheader("Game Stats")
    username = st.text_input("Player Name", value="Guest_User")
    if username:
        st.sidebar.write(f"Good Luck, {username}!")
    else:
        st.sidebar.write("Good Luck, Guest!")
    st.sidebar.title("GAME RULES")
    st.markdown(""" 
    1. Guess the correct number.
    2. Limited attempts.
    3. Difficulty affects range.""")
    
    
    st.divider()
    level = st.select_slider("Select Difficulty", options=["Easy", "Medium", "Hard"], value="Hard")
    max_range = {"Easy": 10, "Medium": 50, "Hard": 100}[level]
    
    # Reset if level changes
    if 'current_level' not in st.session_state or st.session_state.current_level != level:
        st.session_state.current_level = level
        st.session_state.secret_number = random.randint(1, max_range)
        st.session_state.attempts = 0
        st.session_state.history = []
        st.session_state.game_over = False
        st.session_state.feedback = ""
        st.session_state.start_time = time.time()

    if st.button("Reset Game"):
        st.session_state.secret_number = random.randint(1, max_range)
        st.session_state.attempts = 0
        st.session_state.history = []
        st.session_state.game_over = False
        st.session_state.feedback = ""
        st.session_state.start_time = time.time()
        st.rerun()

#----------------TOP METRIC ROW------------------------
current_elapsed = int(time.time() - st.session_state.start_time) if not st.session_state.game_over else st.session_state.get('final_time', 0)
last_guess = st.session_state.history[-1] if st.session_state.history else "--"

col1, col2, col3, col4 = st.columns(4)
with col1: st.markdown(f'<div class="metric-card"><p>Attempts</p><div class="circle-stat">{st.session_state.attempts}</div></div>', unsafe_allow_html=True)
with col2: st.markdown(f'<div class="metric-card"><p>Timer</p><div class="circle-stat" style="border-color:#00FFD4; color:#00FFD4;">{current_elapsed}s</div></div>', unsafe_allow_html=True)
with col3: st.markdown(f'<div class="metric-card"><p>Current Guess</p><div class="circle-stat" style="border-color:#5865F2; color:#5865F2;">{last_guess}</div></div>', unsafe_allow_html=True)
with col4: 
    color = {"Waiting": "#FFF", "Cold":"#00D4FF", "Warm": "#FFA500", "Hot": "#FF4B4B", "Win!": "#00FF00"}[st.session_state.status]
    st.markdown(f'<div class="metric-card"><p>Status</p><div class="circle-stat" style="border-color:{color}; color:{color};">{st.session_state.status}</div></div>', unsafe_allow_html=True)

#----------------ACTION ZONE------------------------
st.markdown("### Action Zone")
with st.container():
    c1, mid, c3 = st.columns([1, 2, 1])
    with mid:
        # Layout for the Guess Box and the Blue Feedback Badge
        feedback_html = f'<span class="feedback-badge">{st.session_state.feedback}</span>' if st.session_state.feedback else ""
        st.markdown(f'''
            <div class="action-zone">
                <div class="guess-box">{last_guess}</div>
                {feedback_html}
            </div>
        ''', unsafe_allow_html=True)
        
        user_guess = st.number_input(f"Input Number", min_value=1, max_value=max_range, key="main_input")
        
        if st.button("Submit Guess"):
            if not st.session_state.game_over:
                st.session_state.attempts += 1
                st.session_state.history.append(user_guess)
                
                diff = abs(user_guess - st.session_state.secret_number)
                
                if user_guess == st.session_state.secret_number:
                    st.session_state.status = "Win!"
                    st.session_state.feedback = "Correct!"
                    st.session_state.game_over = True
                    st.session_state.final_time = int(time.time() - st.session_state.start_time)
                    st.balloons()
                elif user_guess < st.session_state.secret_number:
                    st.session_state.feedback = "Too Low!"
                    st.session_state.status = "Cold" if diff > 15 else "Warm"
                else:
                    st.session_state.feedback = "Too High!"
                    st.session_state.status = "Cold" if diff > 15 else "Warm"
                
                st.rerun()


#----------------CHARTS------------------------
chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    st.subheader("Your Path to the Number")
    if st.session_state.history:
        fig_path = px.line(x=range(1, len(st.session_state.history)+1), y=st.session_state.history, markers=True)
        fig_path.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", height=250)
        st.plotly_chart(fig_path, use_container_width=True)

with chart_col2:
    st.subheader("Guess Distribution")
    if st.session_state.history:
        fig_dist = px.histogram(x=st.session_state.history, nbins=10)
        fig_dist.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", height=250)
        st.plotly_chart(fig_dist, use_container_width=True)

st.markdown("""
<hr style="border:1px solid #30363D;">
<p style="text-align:center; font-size:12px; color:#8B949E;">
Built with ❤️ by Jasneet Kaur
</p>
""", unsafe_allow_html=True)
