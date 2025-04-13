import streamlit as st
from iracingdataapi.client import irDataClient as ir

# Session state setup
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_input" not in st.session_state:
    st.session_state.login_input = ""
if "password_input" not in st.session_state:
    st.session_state.password_input = ""
if "idc" not in st.session_state:
    st.session_state.idc = None

# Login form
if not st.session_state.logged_in:
    st.title("iPython")
    st.text_input("Please, enter your login", key="login_input")
    st.text_input("Please, enter your password", type="password", key="password_input")

    def login_procedure():
        try:
            # Initialize the iRacing client and login
            idc = ir(username=st.session_state.login_input, password=st.session_state.password_input)
            idc._login()  # Assuming _login() method handles the actual login
            member = idc.member_info()
            print(member)  # Debugging: Print the member info

            # Store the iRacing client (idc) in session state for use across pages
            st.session_state.idc = idc
            st.session_state.logged_in = True

        except Exception as e:
            st.warning(f"Login failed: {str(e)}")

    if st.session_state.login_input and st.session_state.password_input:
        st.button("Login", type="primary", on_click=login_procedure)

# After login → Show navigation options
else:
    # Debugging: Ensure client is initialized correctly
    print("iRacing client ready:", st.session_state.idc)

    # Define pages for navigation after login
    pages = {
        "Main": [
            st.Page("dashboard.py", title="Dashboard"),
            st.Page("dashboard2.py", title="Manage your account"),
        ]
    }

    pg = st.navigation(pages)
    pg.run()
