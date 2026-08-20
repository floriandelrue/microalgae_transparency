import streamlit as st

options = [("Email", "Home phone", "Mobile phone")]
    
contact = st.selectbox(
    "How would you like to be contacted?",
    options,
    index=None,
    placeholder="Select contact method...",
)

st.write("You selected:", options.index(contact))
