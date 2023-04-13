#!/usr/bin/env python3

import os
import argparse
import secrets
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.database import Base, User, Token

from utils import get_config

config = get_config()
DB_PATH = config["MAIN"]["DB_PATH"]

engine = create_engine(DB_PATH)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def generate_unique_id(session):
    max_id = session.query(User.user_id).order_by(User.user_id.desc()).first()

    if max_id:
        return max_id[0] + 1
    else:
        return 1
    

def delete_user(user_id):
    session = Session()
    user = session.query(User).filter_by(user_id=user_id).first()

    if not user:
        print(f"No user found with ID: {user_id}")
        return

    tokens = session.query(Token).filter_by(user_id=user_id).all()

    for token in tokens:
        session.delete(token)

    session.delete(user)
    session.commit()
    session.close()

    print(f"User with ID {user_id} and their associated tokens have been deleted.")



def create_user(user_id=None):
    session = Session()

    if user_id is None:
        user_id = generate_unique_id(session)

    existing_user = session.query(User).filter_by(user_id=user_id).first()

    if existing_user:
        print(f"User with ID {user_id} already exists.")
        return

    new_user = User(user_id=user_id)
    session.add(new_user)
    session.flush()

    default_token = secrets.token_hex(16)
    new_token = Token(token=default_token, user_id=new_user.user_id)
    session.add(new_token)

    session.commit()
    session.close()

    print(f"User with ID {user_id} has been created with default token: {default_token}")


def find_user(email):
    session = Session()
    user = session.query(User).filter_by(email=email).first()

    if user:
        print(f"User with email {email} exists.")
    else:
        print(f"User with email {email} does not exist.")


def list_tokens(user_id):
    session = Session()
    user = session.query(User).filter_by(user_id=user_id).first()

    if not user:
        print(f"No user found with Telegram ID: {user_id}")
        return

    tokens = session.query(Token).filter_by(user_id=user.user_id).all()

    if not tokens:
        print(f"No tokens found for Telegram ID: {user_id}")
        return

    print("Tokens:")
    for token in tokens:
        print(f"- {token.token}")


def list_users():
    session = Session()
    users = session.query(User).all()

    if not users:
        print("No users found in the database.")
        return

    print("Users:")
    for user in users:
        print(f"- User ID: {user.user_id}")


def create_database():
    if os.path.exists(DB_PATH):
        print(f"Database already exists at {DB_PATH}")
    else:
        engine = create_engine(DB_PATH)
        Base.metadata.create_all(engine)
        print(f"Database created at {DB_PATH}")


def main():
    parser = argparse.ArgumentParser(description="Token Manager")
    subparsers = parser.add_subparsers(dest="command")

    create_user_parser = subparsers.add_parser("create-user", 
                                               help="Create a new user")
    create_user_parser.add_argument("--user_id", type=int, default=None, 
                                     help="User ID (optional)")
    
    find_user_parser = subparsers.add_parser("find-user", 
                                             help="Find user by ID")
    find_user_parser.add_argument("user_id", type=int, help="User ID")

    list_tokens_parser = subparsers.add_parser("list-tokens", 
                                               help="List all tokens for a user by ID")
    list_tokens_parser.add_argument("user_id", type=int, help="User ID")
    
    list_users_parser = subparsers.add_parser("list-users", 
                                              help="List all users in the database")

    create_database_parser = subparsers.add_parser("create-database", 
                                                   help="Create the database at the specified path in the config file")
    delete_user_parser = subparsers.add_parser("delete-user", 
                                               help="Delete a user by ID and all their associated tokens")
    delete_user_parser.add_argument("user_id", type=int, help="User ID")


    args = parser.parse_args()

    if args.command == "create-user":
        create_user(args.user_id)
    elif args.command == "find-user":
        find_user(args.user_id)
    elif args.command == "list-tokens":
        list_tokens(args.user_id)
    elif args.command == "list-users":
        list_users()
    elif args.command == "create-database":
        create_database()
    elif args.command == "delete-user":
        delete_user(args.user_id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
