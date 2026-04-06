import streamlit as st
import random as rd

# --- 1. Initialize Game State ---
# This helps Streamlit remember things between button clicks
if 'stage' not in st.session_state:
    st.session_state.stage = 'toss' # Stages: toss, choice, innings1, innings2, game_over
    st.session_state.user_score = 0
    st.session_state.comp_score = 0
    st.session_state.is_user_batting = True 
    st.session_state.target = None
    st.session_state.logs = [] # To keep a commentary of the match

st.title("🏏 Hand Cricket Web App")

# Helper function to add commentary
def log_event(message):
    st.session_state.logs.insert(0, message) # Add to top of the list

# --- 2. Toss Stage ---
if st.session_state.stage == 'toss':
    st.subheader("Coin Toss")
    toss_choice = st.radio("Choose Heads or Tails:", ["Heads", "Tails"])
    
    if st.button("Flip Coin"):
        result = rd.choice(["Heads", "Tails"])
        st.write(f"The coin landed on: **{result}**")
        
        if toss_choice == result:
            st.success("You won the toss!")
            st.session_state.stage = 'choice'
            st.rerun()
        else:
            st.error("Computer won the toss!")
            st.session_state.is_user_batting = rd.choice([True, False])
            choice_text = "Bowl" if st.session_state.is_user_batting else "Bat"
            st.info(f"Computer chose to {choice_text}.")
            st.session_state.stage = 'innings1'
            if st.button("Start Match"):
                st.rerun()

# --- 3. Choice Stage (If User Wins Toss) ---
elif st.session_state.stage == 'choice':
    st.subheader("What will you do?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Bat First"):
            st.session_state.is_user_batting = True
            st.session_state.stage = 'innings1'
            st.rerun()
    with col2:
        if st.button("Bowl First"):
            st.session_state.is_user_batting = False
            st.session_state.stage = 'innings1'
            st.rerun()

# --- 4. Gameplay Stage (Innings 1 & 2) ---
elif st.session_state.stage in ['innings1', 'innings2']:
    batter = "You" if st.session_state.is_user_batting else "Computer"
    st.subheader(f"{batter} are BATTING")
    
    # Display Scores
    col1, col2 = st.columns(2)
    col1.metric("Your Score", st.session_state.user_score)
    col2.metric("Computer Score", st.session_state.comp_score)
    
    if st.session_state.target:
        st.warning(f"Target to win: {st.session_state.target}")

    # Play a ball
    user_input = st.number_input("Enter a number (0-6):", min_value=0, max_value=6, step=1)
    
    if st.button("Bowl/Bat!"):
        comp_input = rd.randint(0, 6)
        
        bat = user_input if st.session_state.is_user_batting else comp_input
        bowl = comp_input if st.session_state.is_user_batting else user_input
        
        log_event(f"You played: {user_input} | Computer played: {comp_input}")
        
        # OUT condition
        if bat == bowl:
            log_event(f"**WICKET! {batter} are OUT!**")
            st.error(f"OUT! {batter} scored a total of " + 
                     str(st.session_state.user_score if st.session_state.is_user_batting else st.session_state.comp_score))
            
            # Switch innings or end game
            if st.session_state.stage == 'innings1':
                st.session_state.stage = 'innings2'
                st.session_state.target = (st.session_state.user_score if st.session_state.is_user_batting else st.session_state.comp_score) + 1
                st.session_state.is_user_batting = not st.session_state.is_user_batting
            else:
                st.session_state.stage = 'game_over'
            st.rerun()
            
        # Add Runs
        else:
            if st.session_state.is_user_batting:
                st.session_state.user_score += bat
            else:
                st.session_state.comp_score += bat
                
            # Check if target is reached in Innings 2
            if st.session_state.target:
                current_score = st.session_state.user_score if st.session_state.is_user_batting else st.session_state.comp_score
                if current_score >= st.session_state.target:
                    st.session_state.stage = 'game_over'
                    st.rerun()
                    
    # Show commentary
    with st.expander("Match Commentary", expanded=True):
        for log in st.session_state.logs:
            st.write(log)

# --- 5. Game Over Stage ---
elif st.session_state.stage == 'game_over':
    st.subheader("Match Finished!")
    col1, col2 = st.columns(2)
    col1.metric("Your Final Score", st.session_state.user_score)
    col2.metric("Computer Final Score", st.session_state.comp_score)
    
    if st.session_state.user_score > st.session_state.comp_score:
        st.balloons()
        st.success("🏆 YOU WON THE MATCH!")
    elif st.session_state.comp_score > st.session_state.user_score:
        st.error("💻 COMPUTER WON THE MATCH!")
    else:
        st.info("🤝 IT'S A DRAW!")
        
    if st.button("Play Again"):
        # Reset everything
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()s
