import sqlite3
import streamlit as st

# Database setup
conn = sqlite3.connect('banking_simulation.db')
cursor = conn.cursor()

# Create table for tracking user progress if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS user_progress (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    step TEXT,
                    account_opened BOOLEAN DEFAULT 0,
                    transactions_successful BOOLEAN DEFAULT 0,
                    budget_balanced BOOLEAN DEFAULT 0,
                    quiz_passed BOOLEAN DEFAULT 0)''')

conn.commit()

# Functions to interact with the database and update user progress
def create_user():
    cursor.execute("INSERT INTO user_progress (step) VALUES ('Introduction to Banking Concepts')")
    conn.commit()
    user_id = cursor.lastrowid
    st.session_state['user_id'] = user_id
    st.session_state['step'] = 'Introduction to Banking Concepts'
    st.write(f"New user created with ID: {user_id}")
    return user_id

def update_step(new_step):
    user_id = st.session_state['user_id']
    cursor.execute("UPDATE user_progress SET step = ? WHERE user_id = ?", (new_step, user_id))
    conn.commit()
    st.session_state['step'] = new_step

def open_virtual_account():
    user_id = st.session_state['user_id']
    cursor.execute("UPDATE user_progress SET account_opened = 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    update_step('Practice Virtual Deposits and Withdrawals')
    st.success("Account created successfully!")

def retry_open_account():
    st.warning("Retrying account opening...")

def process_transactions(success):
    user_id = st.session_state['user_id']
    if success:
        cursor.execute("UPDATE user_progress SET transactions_successful = 1 WHERE user_id = ?", (user_id,))
        conn.commit()
        update_step('Budgeting 101')
        st.success("Transaction successful!")
    else:
        st.warning("Transaction failed, retrying...")

def track_budget(balanced):
    user_id = st.session_state['user_id']
    if balanced:
        cursor.execute("UPDATE user_progress SET budget_balanced = 1 WHERE user_id = ?", (user_id,))
        conn.commit()
        update_step('Take Quiz on Saving vs. Spending')
        st.success("Budget balanced!")
    else:
        st.warning("Budget not balanced, retrying...")

def take_quiz(passed):
    user_id = st.session_state['user_id']
    if passed:
        cursor.execute("UPDATE user_progress SET quiz_passed = 1 WHERE user_id = ?", (user_id,))
        conn.commit()
        update_step('Completion of Level 1')
        st.success("Quiz passed! Level 1 complete.")
    else:
        st.warning("Quiz failed, retrying...")

# Streamlit UI
st.title("Banking Simulation")

# Check if user is in session state, else create one
if 'user_id' not in st.session_state:
    st.write("Welcome to the banking simulation!")
    if st.button("Start Simulation"):
        create_user()
else:
    # Display the current step
    step = st.session_state.get('step', 'Introduction to Banking Concepts')

    st.write(f"Current Step: {step}")

    # Handle each step in the flow
    if step == 'Introduction to Banking Concepts':
        st.write("Step: Introduction to Banking Concepts")
        update_step('Understand Savings/Checking Accounts')

    elif step == 'Understand Savings/Checking Accounts':
        ready = st.radio("Are you ready to open an account?", ('Yes', 'No'))
        if ready == 'Yes':
            open_virtual_account()
        else:
            retry_open_account()

    elif step == 'Practice Virtual Deposits and Withdrawals':
        transaction = st.radio("Was the transaction successful?", ('Yes', 'No'))
        if transaction == 'Yes':
            process_transactions(True)
        else:
            process_transactions(False)

    elif step == 'Budgeting 101':
        budget = st.radio("Is the budget balanced?", ('Yes', 'No'))
        if budget == 'Yes':
            track_budget(True)
        else:
            track_budget(False)

    elif step == 'Take Quiz on Saving vs. Spending':
        quiz = st.radio("Did you pass the quiz?", ('Yes', 'No'))
        if quiz == 'Yes':
            take_quiz(True)
        else:
            take_quiz(False)

    elif step == 'Completion of Level 1':
        st.write("Congratulations! You've completed Level 1.")
        if st.button("Unlock Level 2"):
            update_step('Unlock Level 2')
            st.write("Level 2 is coming soon!")

# Close database connection when done
conn.close()
