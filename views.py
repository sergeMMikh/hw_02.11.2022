from typing import Type
from flask import jsonify, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from app import bcrypt
from errors import HttpError
from models import UserModel, Session, AdvModel
from validation import validate, CreateUserSchema, PatchUserSchema, CreateAdvSchema, PatchAdvSchema


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
        raise HttpError(403, f'wrong password')

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
        data_to_patch = validate(request.json, PatchAdvSchema)
        json_data = request.json
        with Session() as session:
            user_id = get_user_id(json_data, UserModel, session)

            if user_id != adv_id:
                raise HttpError(403, "You don't have rights to delete this advertisement!")

        adv = get_by_id(adv_id, AdvModel, session)

        for field, value in data_to_patch.items():
            setattr(adv, field, value)
        session.commit()
        return jsonify({'status': 'success', 'id': adv.id})

    def delete(self, adv_id: int):
        json_data = request.json
        with Session() as session:
            user_id = get_user_id(json_data, UserModel, session)

            if user_id != adv_id:
                raise HttpError(403, "You don't have rights to delete this advertisement!")

            adv = get_by_id(adv_id, AdvModel, session)
            session.delete(adv)
            session.commit()
            return jsonify({'status': 'success', 'id': adv.id, 'user_id': user_id})
