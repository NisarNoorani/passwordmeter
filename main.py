import streamlit as st
import re
import string
import math

def calculate_entropy(password):
    """Calculate password entropy (bits of information)"""
    if not password:
        return 0
    
    charset_size = 0
    if any(c in string.ascii_lowercase for c in password):
        charset_size += 26
    if any(c in string.ascii_uppercase for c in password):
        charset_size += 26
    if any(c in string.digits for c in password):
        charset_size += 10
    if any(c in string.punctuation for c in password):
        charset_size += 33
    
    if charset_size == 0:  # If no standard chars found, use extended ASCII
        charset_size = 256
        
    # Calculate entropy bits
    entropy = math.log2(charset_size) * len(password)
    return entropy

def check_password_strength(password):
    """Evaluate password strength and return score and feedback"""
    if not password:
        return {
            "score": 0, 
            "strength": "None",
            "color": "gray",
            "feedback": ["Enter a password to check its strength"]
        }
    
    score = 0
    feedback = []
    
    # Length check - base score
    if len(password) >= 12:
        score += 30
    elif len(password) >= 8:
        score += 20
    elif len(password) >= 6:
        score += 10
    else:
        feedback.append("Password is too short (minimum 8 characters recommended)")
    
    # Character variety checks
    if re.search(r'[A-Z]', password):
        score += 10
    else:
        feedback.append("Add uppercase letters")
        
    if re.search(r'[a-z]', password):
        score += 10
    else:
        feedback.append("Add lowercase letters")
        
    if re.search(r'[0-9]', password):
        score += 10
    else:
        feedback.append("Add numbers")
        
    if re.search(r'[^A-Za-z0-9]', password):
        score += 15
    else:
        feedback.append("Add special characters (!@#$%^&*)")
    
    # Complexity deductions
    if re.search(r'(.)\1{2,}', password):  # Repeated characters
        score -= 10
        feedback.append("Avoid repeated characters")
        
    if re.search(r'(123|abc|qwerty|password|admin)', password.lower()):
        score -= 15
        feedback.append("Avoid common patterns and words")
    
    # Calculate entropy bonus
    entropy = calculate_entropy(password)
    if entropy > 60:
        score += 25
    elif entropy > 40:
        score += 15
    elif entropy > 30:
        score += 10
    
    # Cap score between 0-100
    score = max(0, min(100, score))
    
    # Determine strength category
    if score >= 80:
        strength = "Very Strong"
        color = "green"
    elif score >= 60:
        strength = "Strong"
        color = "lightgreen"
    elif score >= 40:
        strength = "Medium"
        color = "orange"
    elif score >= 20:
        strength = "Weak"
        color = "red"
    else:
        strength = "Very Weak"
        color = "darkred"
    
    # Add default feedback if empty
    if not feedback:
        feedback.append("Password meets basic security requirements")
    
    return {
        "score": score,
        "strength": strength,
        "color": color,
        "feedback": feedback,
        "entropy": entropy
    }

def main():
    st.set_page_config(
        page_title="Password Strength Checker",
        page_icon="🔒",
        layout="centered"
    )
    
    st.title("🔒 Password Strength Checker")
    st.write("Enter your password below to check its strength")
    
    # Password input with toggle visibility
    col1, col2 = st.columns([4, 1])
    with col1:
        password = st.text_input("Password", type="password", key="password_input")
    with col2:
        if st.button("👁️ Show" if st.session_state.get("hide_password", True) else "🙈 Hide"):
            st.session_state["hide_password"] = not st.session_state.get("hide_password", True)
            
    if not st.session_state.get("hide_password", True):
        st.code(password)
        
    # Check password strength
    result = check_password_strength(password)
    
    # Display strength meter
    st.write(f"**Strength: {result['strength']}**")
    st.progress(result["score"] / 100)
    
    # Display additional stats in expandable section
    with st.expander("Password Details", expanded=True):
        st.write(f"**Score:** {result['score']}/100")
        if password:
            st.write(f"**Length:** {len(password)} characters")
            st.write(f"**Entropy:** {result['entropy']:.1f} bits")
        
        st.write("**Feedback:**")
        for item in result["feedback"]:
            st.markdown(f"- {item}")
    
    # Password security tips
    with st.expander("Password Security Tips", expanded=False):
        st.markdown("""
        ### Tips for a strong password:
        
        - Use at least 12-16 characters
        - Include uppercase letters, lowercase letters, numbers, and special characters
        - Avoid personal information like names, birthdays, etc.
        - Don't use common words or patterns (123456, qwerty, password)
        - Consider using a passphrase - a series of random words
        - Use a different password for each account
        - Consider using a password manager
        """)
    
    # Footer
    st.divider()
    st.caption("This tool evaluates passwords locally and does not store or transmit them anywhere.")

if __name__ == "__main__":
    main()
