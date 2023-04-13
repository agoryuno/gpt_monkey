import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.database import Base, User, Token 

from utils import get_config

config = get_config()
DB_PATH = config["MAIN"]["DB_PATH"]

engine = create_engine(DB_PATH)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def get_token_by_user_id(user_id):
    session = Session()
    user = session.query(User).filter_by(user_id=user_id).first()

    if not user:
        print(f"No user found with user ID: {user_id}")
        return None

    token = session.query(Token).filter_by(user_id=user.user_id).first()

    if not token:
        print(f"No tokens found for user ID: {user_id}")
        return None

    return token.token


def main():
    parser = argparse.ArgumentParser(description="Token Template")
    parser.add_argument("user_id", type=int, help="User ID")

    args = parser.parse_args()

    token = get_token_by_user_id(args.user_id)

    if token:
        with open("userscript.template", "r") as file:
            content = file.read()

        formatted_string = eval(f"f'{content}'")
        print(formatted_string)


if __name__ == "__main__":
    main()