# NumSense 🔢  
An Intelligent Number Guessing Dashboard

NumSense is an interactive number guessing dashboard built using **Python and Streamlit**, designed to transform a simple guessing game into a clean, data-driven and visually engaging user experience.

---

##  FEATURES

### 🎯 Difficulty-Based Gameplay
- Three difficulty levels: **Easy, Medium, Hard**
- Each difficulty dynamically changes the guessing range
- Game resets automatically when difficulty is changed

---

### 📊 Real-Time Game Statistics
- **Attempts counter** to track total guesses
- **Live timer** showing elapsed time
- **Current guess display**
- **Status indicator** (`Waiting`, `Cold`, `Warm`, `Win`)
- All stats update instantly using Streamlit session state

---

### 🧠 Intelligent Feedback System
- Instant feedback after every guess:
  - *Too Low*
  - *Too High*
  - *Correct*
- Status logic based on proximity to the secret number
- Clear visual cues for better decision-making

---

### 📈 Interactive Data Visualizations
Powered by **Plotly**:
- **Guess Progression Chart**  
  Visualizes how the player approaches the correct number over attempts
- **Guess Distribution Histogram**  
  Shows the frequency of guesses to analyze player behavior

---

### 🎨 Modern Dark UI (Custom CSS)
- Fully customized **dark theme**
- Styled metric cards, badges, and action zones
- Clean dashboard layout for a product-like experience
- Focused on readability and minimalism

---

### 🔄 Session-Based Gameplay
- Uses Streamlit **session state** to:
  - Maintain game progress
  - Preserve history across interactions
  - Prevent unwanted resets on reruns

---

### ♻️ Reset & Replay Support
- Manual **Reset Game** option
- Automatic reset on difficulty change
- Smooth replay experience without page reload issues

---

## 🛠 Tech Stack
- **Python**
- **Streamlit**
- **Plotly**
- **HTML/CSS**

---

## 📌 Project Focus
This project focuses on:
- Interactive UI development
- State management in Streamlit
- Game logic implementation
- Data visualization for user insights
- Writing clean, readable, and modular code
