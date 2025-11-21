from sqlalchemy import create_engine, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import scoped_session, relationship
from sqlalchemy.orm.decl_api import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String
from datetime import datetime, timedelta, UTC
import os
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from repository.abstract_repository import AbstractRepository
from sdk.request.register_parameters import RegisterRequestParameters


def utc_now():
    return datetime.now(UTC)

# Database configuration
USERNAME = os.getenv("DB_USERNAME", "postgres")
PASSWORD = os.getenv("DB_PASSWORD", "12345")
HOSTNAME = os.getenv("DB_HOSTNAME", "127.0.0.1")
PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "todo-db")
USERS_TABLE_NAME = "users"
TODOS_TABLE_NAME = "todos"

# Create the database engine
DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=True)

# Base class for ORM models
Base = declarative_base()

# Create a session to interact with the database
Session = scoped_session(sessionmaker(bind=engine))

class User(Base):
    __tablename__ = USERS_TABLE_NAME
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), default=utc_now)

    # Relationship to Todos
    todos = relationship("Todo", back_populates="user", cascade="all, delete-orphan")

class Todo(Base):
    __tablename__ = TODOS_TABLE_NAME
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), default=utc_now)
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), default=utc_now)

    # Relationship to Users
    user = relationship("User", back_populates="todos")


def verify_password(stored_hash: str, password: str) -> bool:
    """Verify a password against its hash"""
    return check_password_hash(stored_hash, password)

def create_jwt_token(user_id: int) -> str:
    payload = {
        'user_id': user_id,
        'exp': datetime.now(UTC) + timedelta(hours=24)
    }
    return jwt.encode(payload, 'your-secret-key', algorithm='HS256')

class PostgresRepository(AbstractRepository):
    def _is_user_exists_with_email(self, email: str) -> bool:
        existing_user = Session.query(User).filter(User.email == email).first()
        if (existing_user):
            return True
        return False

    def create_user(self, register_parameters: RegisterRequestParameters) -> str:
        password_hash = generate_password_hash(register_parameters.password)
        # if self._is_user_exists_with_email(register_parameters.email):


        new_user = User(
            name=register_parameters.name,
            email=register_parameters.email,
            password_hash=password_hash
        )

        Session.add(new_user)
        Session.commit()

        return password_hash