import streamlit as st
import re 
import math
import requests
import hashlib

def check_common_passwords(password):
    with open("10-million-password-list-top-1000000.txt", "r") as file:
        common_passwords = file.read().splitlines()
    if password.lower in common_passwords:
        return True
    else:
        return False

def check_pwned_password(password):
    # SHA1 hash of the password
    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    
    try:
        res = requests.get(url)
        if res.status_code != 200:
            return False
        hashes = (line.split(':') for line in res.text.splitlines())
        return any(h == suffix for h, count in hashes)
    except:
        return False  # Assume not pwned if API fails

def create_web_page():
    st.set_page_config(page_title="Password Strength Checker", page_icon="🔒")
    st.title("🔐 Password Strength checker ")
    st.markdown(""" 
    ## Welcome to the Password Strength Checker!!
    This simple tool helps you evaluate the strength of your password based on various criteria.
    The stronger your password, the better protected you are against unauthorized access.""")

    password = st.text_input("Enter your password: ", type="password")
    if password:
        st.markdown("**Password Strength Evaluation with regex:**")
        strength = regex_password_checker(password)
        for feedback in strength:
            st.write(feedback)
        st.markdown("**Password Strength Evaluation with entropy calculation:**")
        feed = calculate_entropy(password)
        st.write(feed)
        st.markdown("**Checking With common Password List**")
        if check_common_passwords(password):
            st.warning("⚠️ Your password is too common!") 
        else:
            st.success("✅ Your password is not common.") 
        st.markdown("**Checking if Your Password has been compromised in data breach**") 
        if check_pwned_password(password):
            st.warning("⚠️ Your password has been compromised in a data breach!")
        else:
            st.success("✅ Your password has not been compromised in a data breach.")
    else:
        st.info("Please enter a password to check its strength.")
        

def regex_password_checker(password):
    score = 0
    feedback = []
    if len(password) < 8:
        feedback.append("❌Password should be at least 8 characters long.")
    else:
        score += 1
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌Password should contain at least one uppercase letter and one lowercase letter.")
   
    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("❌Password should contain at least one digit.")
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("❌Password should contain at least one special character.")
    
    if score == 4: 
        feedback.append("✅ Your password is strong!")
    elif score == 3:
        feedback.append("⚠️ Your password is medium strength.")
    elif score == 2:
        feedback.append("❗ Your password is weak.")
    elif score == 1:
        feedback.append("❗ Your password is very weak.")
    return feedback

def calculate_entropy(password):
    length = len(password)
    charset_size = 0
    if re.search(r"[A-Z]", password):
        charset_size += 26
    if re.search(r"[a-z]", password):
        charset_size += 26
    if re.search(r"/d",password):
        charset_size += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        charset_size += 32
    if re.search(r"\s", password):
        charset_size += 1   
    
    entropy = length * math.log2(charset_size)

    if entropy < 28 :
        return "🟥 Very Week Password"
    if entropy < 40:
        return "🟧 Weak Password"
    if entropy < 56:
        return "🟨 Medium Password"
    if entropy < 64:
        return "🟩 Strong Password"
    if entropy >= 64:
        return "🟦 Very Strong Password" 
    
create_web_page()

