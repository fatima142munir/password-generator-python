import streamlit as st
import re
import random
import string

def check_password_strength(password: str) -> tuple[str, str, list[str]]:
    score: int = 0
    feedback: list[str] = []
    
    # Check password length
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")
    
    # check Upper & Lowercase
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")
    
    # check Digit
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")
    
    # check Special Character
    if re.search(rf"[{re.escape('!@#$%^&*')}]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")
    
    # Password strength Rating
    if score == 4:
        return "✅ Strong Password!", "green", feedback
    elif score > 2:
        return "⚠️ Moderate Password - Consider adding more security features.", "orange", feedback
    else:
        return "❌ Weak Password - Improve it using the suggestions above.", "red", feedback

def generate_password(length: int = 12) -> str:
    characters: str = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(length))

# Use of streamlit UI
st.title("🔐 Password Strength Checker & Generator")

def password_form() -> None:
    with st.form("password_form"):
        password: str = st.text_input("Enter your password:", type="password")
        submitted: bool = st.form_submit_button("Check Password")
    
    if submitted and password:
        result, color, suggestions = check_password_strength(password)
        if color == "green":
            st.success(result)
        elif color == "orange":
            st.warning(result)
        else:
            st.error(result)
        
        if suggestions:
            st.write("### Suggestions:")
            for suggest in suggestions:
                st.write(suggest)
password_form()

# create Password Generator
st.write("---")
st.subheader("🔑 Generate a Strong Password")
password_length: int = st.slider("Select password length:", min_value=8, max_value=20, value=12)

if "generated_password" not in st.session_state:
    st.session_state.generated_password = ""

if st.button("Generate Password"):
    st.session_state.generated_password = generate_password(password_length)

st.text_input("Generated Password:", value=st.session_state.generated_password, disabled=True)
