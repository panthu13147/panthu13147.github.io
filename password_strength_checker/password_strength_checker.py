import re

def check_password_strength(password):
    score = 0
    feedback = []

    # Check Length
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password is too short (needs 8+ chars).")

    # Check for Uppercase
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("❌ Add uppercase letters (A-Z).")

    # Check for Numbers
    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("❌ Add numbers (0-9).")

    # Check for Special Characters
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("❌ Add special characters (!@#$...).")

    # Final Result
    print(f"\n--- Password Score: {score}/4 ---")
    if score == 4:
        print("✅ Strong Password! Great job.")
    elif score >= 2:
        print("⚠️ Moderate Password. You can do better.")
    else:
        print("⛔ Weak Password. Please improve it.")
    
    for tip in feedback:
        print(tip)

if __name__ == "__main__":
    print("🔐 Welcome to the Password Strength Checker!")
    while True:
        user_pass = input("\nEnter a password to check (or 'q' to quit): ")
        if user_pass.lower() == 'q':
            break
        check_password_strength(user_pass)