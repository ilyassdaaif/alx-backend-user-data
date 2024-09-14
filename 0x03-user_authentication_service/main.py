#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

auth = Auth()

# Register a new user
email = "bob@bob.com"
password = "mySuperPwd"
auth.register_user(email, password)
print(f"User {email} created")

# Generate a reset password token
reset_token = auth.get_reset_password_token(email)
print(f"Reset token: {reset_token}")

# Update the password
try:
    auth.update_password(reset_token, "newSuperPwd")
    print("Password updated")
except ValueError:
    print("Invalid reset token")

# Verify the new password works
if auth.valid_login(email, "newSuperPwd"):
    print("New password is valid")
else:
    print("New password is invalid")

# Try to update password with invalid token
try:
    auth.update_password("invalid_token", "anotherPassword")
    print("Password updated")
except ValueError:
    print("Invalid reset token")
