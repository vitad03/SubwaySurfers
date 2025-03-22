import streamlit as st
import time

# --- Missions Configuration ---
missions = [
    {"name": "Team Mission 1", "coins_per_player": 200, "time_limit": 300},  # 5 minutes
    {"name": "Team Mission 2", "coins_per_player": 400, "time_limit": 420},  # 7 minutes
]

# --- Session State Setup ---
if "page" not in st.session_state:
    st.session_state.page = 'intro'
if "mission_index" not in st.session_state:
    st.session_state.mission_index = 0
if "mission_complete" not in st.session_state:
    st.session_state.mission_complete = False
if "total_score" not in st.session_state:
    st.session_state.total_score = 0
if "missions_completed" not in st.session_state:
    st.session_state.missions_completed = 0

# --- Intro Page ---
if st.session_state.page == 'intro':
    st.image(
        "https://i0.wp.com/9to5mac.com/wp-content/uploads/sites/6/2023/03/subway-surfers-4-billion-downloads.jpg?w=1500&quality=82&strip=all&ssl=1",
        use_container_width=True
    )

    st.title("🏆 Subway Surfers Multiplayer Co-op Missions Demo")

    st.write("""
    This simulator shows a simple idea: players teaming up to complete missions together.

    In this example, the mission is collecting coins, but it could easily be about anything else,
    like gathering power-ups or hitting a combined score. The key point is bringing players together,
    encouraging teamwork, boosting engagement, and adding excitement with limited-time challenges.

    Try it out yourself to see how cooperative gameplay might feel in Subway Surfers!
    """)

    st.divider()
    st.subheader("🎮 How would you like to play?")
    match_type = st.radio("Choose your match type:", ["Invite a Friend", "Random Match"])

    if match_type:
        if st.button("➡️ Start Mission"):
            st.session_state.page = 'mission'

# --- Mission Gameplay ---
elif st.session_state.page == 'mission':

    if st.session_state.mission_index >= len(missions):
        st.title("🏁 All Missions Completed!")
        st.success("You’ve completed all cooperative missions!")
        st.metric("💰 Total Coins Collected", st.session_state.total_score)
        st.metric("✅ Missions Completed", st.session_state.missions_completed)
        if st.button("🔄 Restart"):
            st.session_state.page = 'intro'
            st.session_state.mission_index = 0
            st.session_state.total_score = 0
            st.session_state.missions_completed = 0
            st.session_state.mission_complete = False
            st.rerun()
        st.stop()

    # Load active mission
    mission = missions[st.session_state.mission_index]

    st.title(f"🚨 {mission['name']}")
    st.info(f"Your mission is to collect **{mission['coins_per_player']} coins each** "
            f"in **{mission['time_limit'] // 60} minutes** with your partner. Work as a team!")

    col1, col2 = st.columns(2)
    with col1:
        start_clicked = st.button("🚀 Start Mission")
    with col2:
        skip_clicked = st.button("⏩ Skip Mission")

    if skip_clicked:
        st.session_state.mission_complete = True

    if start_clicked and not st.session_state.mission_complete:
        countdown = mission["time_limit"]
        progress_bar = st.progress(0)
        status_text = st.empty()
        player_a_display = st.empty()
        player_b_display = st.empty()
        total_coins_display = st.empty()

        player_a_coins = 0
        player_b_coins = 0
        goal = mission['coins_per_player'] * 2

        for t in range(countdown, 0, -1):
            player_a_coins += min(5, mission["coins_per_player"] - player_a_coins)
            player_b_coins += min(5, mission["coins_per_player"] - player_b_coins)
            total_coins = player_a_coins + player_b_coins
            percent = min(total_coins / goal, 1.0)

            status_text.subheader(f"⏳ Time Left: {t // 60} min {t % 60} sec")
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
            st.session_state.total_score += total_coins
            st.session_state.missions_completed += 1
        else:
            st.error(f"❌ Mission Failed. Needed {goal} coins but collected {total_coins}.")

    if st.session_state.mission_complete:
        st.success("✅ Mission Complete!")
        if st.button("➡️ Continue to Next Mission"):
            st.session_state.mission_index += 1
            st.session_state.mission_complete = False
            st.rerun()
