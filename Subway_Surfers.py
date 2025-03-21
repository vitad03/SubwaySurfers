import streamlit as st
import time

# 🎮 Intro Section for Recruiters
st.title("👥 Subway Surfers Team Play: Race Against Time! ⏳")
st.write("""
This simulator shows a simple idea: players teaming up to complete missions together.

In this example, the mission is collecting coins, but it could easily be about anything else, like gathering power-ups or hitting a combined score. The key point is bringing players together, encouraging teamwork, boosting engagement, and adding excitement with limited-time challenges.

Try it out yourself to see how cooperative gameplay might feel in Subway Surfers!
""")
st.divider()  # Adds a clean visual break


# Initialize session state variables
if 'mission_index' not in st.session_state:
    st.session_state.mission_index = 0

if 'mission_complete' not in st.session_state:
    st.session_state.mission_complete = False

if 'total_score' not in st.session_state:
    st.session_state.total_score = 0  # Store total coins collected

if 'missions_completed' not in st.session_state:
    st.session_state.missions_completed = 0  # Track missions completed

# Define only 2 missions (as requested)
missions = [
    {"coins_per_player": 200, "time_limit": 300},  # 5 min
    {"coins_per_player": 400, "time_limit": 360},  # 6 min
]

# If all missions are completed, show final results
if st.session_state.mission_index >= len(missions):
    st.title("🏆 **Final Results**")
    st.success("You have completed all missions! Here's your final performance:")

    st.metric(label="💰 **Total Coins Collected**", value=st.session_state.total_score)
    st.metric(label="✅ **Missions Completed**", value=st.session_state.missions_completed)

    st.write("**Awesome job! Want to restart the challenge?**")
    if st.button("🔄 Restart Game"):
        st.session_state.mission_index = 0
        st.session_state.total_score = 0
        st.session_state.missions_completed = 0
        st.session_state.mission_complete = False
        st.rerun()

    st.stop()  # Prevents further execution

# Get current mission
mission = missions[st.session_state.mission_index]

# UI: Mission Header
st.title(f"🏁 Team Mission {st.session_state.mission_index + 1}")
st.info(f"Your mission is to collect **{mission['coins_per_player']} coins each** in "
        f"**{mission['time_limit']//60} minutes** with your partner. Work as a team!")

# Buttons Row (Start + Skip)
col1, col2 = st.columns(2)
with col1:
    start_clicked = st.button("🚀 Start Mission")

with col2:
    skip_clicked = st.button("⏩ Skip Mission (For Testing)")

# If skip is clicked → Instantly complete the mission
if skip_clicked:
    st.session_state.mission_complete = True

# Countdown Timer & Game Simulation
if start_clicked and not st.session_state.mission_complete:
    countdown = mission["time_limit"]
    progress_bar = st.progress(0)
    status_text = st.empty()
    player_a_display = st.empty()
    player_b_display = st.empty()
    total_coins_display = st.empty()

    player_a_coins = 0
    player_b_coins = 0
    goal = mission['coins_per_player'] * 2  # Combined target

    for t in range(countdown, 0, -1):
        player_a_coins += min(5, mission["coins_per_player"] - player_a_coins)
        player_b_coins += min(5, mission["coins_per_player"] - player_b_coins)

        total_coins = player_a_coins + player_b_coins
        percent = min(total_coins / goal, 1.0)

        status_text.subheader(f"⏳ Time Left: {t//60} min {t%60} sec")
        player_a_display.write(f"👤 **Player A Coins:** {player_a_coins}")
        player_b_display.write(f"👤 **Player B Coins:** {player_b_coins}")
        total_coins_display.subheader(f"💰 **Total Coins Collected: {total_coins}**")
        progress_bar.progress(percent)

        if total_coins >= goal:
            st.session_state.mission_complete = True
            break

        time.sleep(1)

    if total_coins >= goal:
        st.success(f"🎉 Mission Complete! You collected {total_coins} coins.")
        st.session_state.total_score += total_coins  # Add to total score
        st.session_state.missions_completed += 1  # Increment mission count
    else:
        st.error(f"❌ Mission Failed. Needed {goal} coins but collected {total_coins}.")

# If mission complete: show Continue button
if st.session_state.mission_complete:
    st.success("🎉 Congratulations! You've passed this mission.")
    if st.button("➡️ Continue to Next Mission"):
        st.session_state.mission_index += 1
        st.session_state.mission_complete = False
        st.rerun()

