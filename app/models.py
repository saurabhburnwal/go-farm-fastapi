
from sqlalchemy import Table, Column, Integer, String
from app.database import metadata


results = Table(
    "results",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("author", String, index=True),
    Column("content", String, index=True)
)

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("token", String, index=True),
    Column("email", String, index=True),
    Column("name", String, index=True),
    Column("username", String, index=True),
    Column("password", String, index=True)
)

