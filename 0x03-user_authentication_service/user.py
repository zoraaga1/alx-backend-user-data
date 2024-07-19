#!/usr/bin/env python3
"""user module"""

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import mapper

metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String(250), nullable=False),
    Column('hashed_password', String(250), nullable=False),
    Column('session_id', String(250), nullable=True),
    Column('reset_token', String(250), nullable=True),
)

class User:
    def __init__(self, email, hashed_password, session_id=None, reset_token=None):
        self.email = email
        self.hashed_password = hashed_password
        self.session_id = session_id
        self.reset_token = reset_token

mapper(User, users_table)
