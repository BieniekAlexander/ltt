import os

raw_env = [
    f"MONGODB_URI={os.getenv('MONGODB_URI')}",
    f"JWT_AUTH_OPTIONAL={os.getenv('JWT_AUTH_OPTIONAL')}"
]