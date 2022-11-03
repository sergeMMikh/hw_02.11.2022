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

app = Flask('app')
bcrypt = Bcrypt(app)


class HttpError(Exception):
    def __init__(self, stats_code: int, message: str | dict | list):
        self.stats_code = stats_code
        self.message = message


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({
        'status': 'error',
        'message': error.message
    })
    response.status_code = error.stats_code
    return response


DSN = 'postgresql://app:1234@localhost:5432/adv_rest_api'

engine = create_engine(DSN)
Base = declarative_base()
Session = sessionmaker(bind=engine)

password_regex = re.compile(
    "^(?=.*[a-z_])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&_])[A-Za-z\d@$!#%*?&_]{8,200}$"
)

email_regex = re.compile(
    "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
)


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    advertisement = relationship("AdvModel", backref="user")


class AdvModel(Base):
    __tablename__ = 'adv'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False, unique=True)
    description = Column(String(2000), nullable=False)
    creation_time = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))


Base.metadata.create_all(engine)


class CreateUserSchema(pydantic.BaseModel):
    name: str
    email: str
    password: str

    @pydantic.validator("name")
    def check_name(cls, value: str):
        if len(value) > 100:
            raise ValueError("name mast be less 32 chars")

        return value

    @pydantic.validator("email")
    def check_email(cls, value: str):
        if not re.search(email_regex, value):
            raise ValueError("email is wrong")

        return value

    @pydantic.validator("password")
    def check_password(cls, value: str):
        if not re.search(password_regex, value):
            raise ValueError("password to easy")

        value.encode()
        value = bcrypt.generate_password_hash(value, rounds=None)
        value = value.decode()

        return value


class PatchUserSchema(pydantic.BaseModel):
    name: Optional[str]
    email: str
    password: Optional[str]

    @pydantic.validator("password")
    def check_name(cls, value: str):
        if len(value) > 32:
            raise ValueError("name mast be less 32 chars")

        return value

    @pydantic.validator("email")
    def check_email(cls, value: str):
        if not re.search(email_regex, value):
            raise ValueError("email is wrong")

        return value

    @pydantic.validator("password")
    def check_password(cls, value: str):
        if not re.search(password_regex, value):
            raise ValueError("password to easy")

        value = value.encode()
        value = bcrypt.generate_password_hash(value)
        value = value.decode()

        return value


class CreateAdvSchema(pydantic.BaseModel):
    title: str
    description: str

    @pydantic.validator("title")
    def check_title(cls, value: str):
        if len(value) > 200:
            raise ValueError("The title length mast be less 200 chars")

        return value

    @pydantic.validator("description")
    def check_description(cls, value: str):
        if len(value) > 2000:
            raise ValueError("The advertisement length mast be less 2000 chars")

        return value


def validate(data_to_validate: dict,
             validation_class: Type[CreateUserSchema] | Type[PatchUserSchema] | Type[CreateAdvSchema]):
    try:
        return validation_class(**data_to_validate).dict(exclude_none=True)
    except pydantic.ValidationError as err:
        raise HttpError(400, err.errors())


def get_by_id(item_id: int, orm_model: Type[UserModel], session: Session):
    orm_item = session.query(orm_model).get(item_id)

    if orm_item is None:
        raise HttpError(404, 'item not found')

    return orm_item


def get_user_id(item_json: dict, orm_model: Type[UserModel], session: Session):
    user = session.query(orm_model).filter_by(name=item_json['name']).first()

    pw_hash = bcrypt.generate_password_hash('secret')
    print(f'pw_hash: {pw_hash}')
    print(bcrypt.check_password_hash(pw_hash, 'secret'))

    if user is None:
        raise HttpError(404, 'user not found')

    if not bcrypt.check_password_hash(user.password, item_json['password']):
        raise HttpError(404, f'wrong password')

    return user.id


class UserView(MethodView):

    def get(self, user_id: int):
        with Session() as session:
            user = get_by_id(user_id, UserModel, session)

            if user is None:
                raise HttpError(404, 'user not found')

            return jsonify({
                'user': user.name,
                'email': user.email
            })

    def post(self):
        json_data = request.json
        with Session() as session:
            try:
                new_user = UserModel(**validate(json_data, CreateUserSchema))
                session.add(new_user)
                session.commit()
            except IntegrityError:
                raise HttpError(409, 'User name already exists')
            return jsonify({'status': 'ok', 'id': new_user.id})

    def patch(self, user_id: int):
        data_to_patch = validate(request.json, PatchUserSchema)

        with Session() as session:
            user = get_by_id(user_id, UserModel, session)

            for field, value in data_to_patch.items():
                setattr(user, field, value)
            session.commit()
            return jsonify({'status': 'success', 'id': user.id})

    def delete(self, user_id: int):
        with Session() as session:
            user = get_by_id(user_id, UserModel, session)
            session.delete(user)
            session.commit()
            return jsonify({'status': 'success', 'id': user.id})


class AdvView(MethodView):

    def get(self, adv_id: int):
        with Session() as session:
            adv = get_by_id(adv_id, AdvModel, session)

            if adv is None:
                raise HttpError(404, 'user not found')

            return jsonify({
                'Title': adv.title,
                'Description': adv.description
            })

    def post(self):
        json_data = request.json
        with Session() as session:
            try:
                new_adv = AdvModel(**validate(json_data, CreateAdvSchema))
                user_id = get_user_id(json_data, UserModel, session)
                setattr(new_adv, 'user_id', user_id)
                session.add(new_adv)
                session.commit()
            except IntegrityError:
                raise HttpError(409, 'This title already exists')
            return jsonify({'status': 'ok', 'id': new_adv.id})

    def patch(self, adv_id: int):
        return jsonify({
            'status': 'ok',
            'request': 'patch',
            'id': adv_id
        })

    def delete(self, adv_id: int):
        return jsonify({
            'status': 'ok',
            'request': 'delete',
            'id': adv_id
        })


app.add_url_rule('/user/<int:user_id>', view_func=UserView.as_view('users_get'), methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/user/', view_func=UserView.as_view('users'), methods=['POST'])
app.add_url_rule('/adv/<int:adv_id>', view_func=AdvView.as_view('adv_get'), methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/adv/', view_func=AdvView.as_view('adv'), methods=['POST'])

app.run()
