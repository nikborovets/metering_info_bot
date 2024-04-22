import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv, find_dotenv

authorized_users = map(int(), os.getenv('AUTHORIZED_USERS').split(","))
print(authorized_users)