#!/usr/bin/env python3
"""user module"""

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker, mapper

# Initialize the metadata
metadata = MetaData()

# Define the table
users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('email', String, nullable=False),
    Column('hashed_password', String, nullable=False),
    Column('session_id', String, nullable=True),
    Column('reset_token', String, nullable=True),
)

# Define the class
class User:
    def __init__(self, email, hashed_password, session_id=None, reset_token=None):
        self.email = email
        self.hashed_password = hashed_password
        self.session_id = session_id
        self.reset_token = reset_token

# Map the class to the table
mapper(User, users_table)
