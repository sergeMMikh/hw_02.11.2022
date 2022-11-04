import pydantic
import re
from typing import Type, Optional
from flask_bcrypt import Bcrypt
from flask import Flask, jsonify, request
from flask.views import MethodView
from sqlalchemy import Column, Integer, String, DateTime, create_engine, func, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

from models import UserModel, Session, AdvModel, Base, engine

app = Flask('app')
bcrypt = Bcrypt(app)

# Base.metadata.create_all(engine)




# app.add_url_rule('/user/<int:user_id>', view_func=UserView.as_view('users_get'), methods=['GET', 'PATCH', 'DELETE'])
# app.add_url_rule('/user/', view_func=UserView.as_view('users'), methods=['POST'])
# app.add_url_rule('/adv/<int:adv_id>', view_func=AdvView.as_view('adv_get'), methods=['GET', 'DELETE'])
# app.add_url_rule('/adv/', view_func=AdvView.as_view('adv'), methods=['POST'])
#
# app.run()
