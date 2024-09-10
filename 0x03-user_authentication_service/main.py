#!/usr/bin/env python3
"""
Main file
"""
from db import DB
from user import User

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


my_db = DB()

user = my_db.add_user("test@test.com", "PwdHashed")
print(user.id)

try:
    found_user = my_db.find_user_by(email="test@test.com")
    print(found_user.id)
except NoResultFound:
    print("Not found")

try:
    found_user = my_db.find_user_by(email="test2@test.com")
    print(found_user.id)
except NoResultFound:
    print("Not found")

try:
    found_user = my_db.find_user_by(no_email="test@test.com")
    print(found_user.id)
except InvalidRequestError:
    print("Invalid")
