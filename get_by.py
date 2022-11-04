# from typing import Type
#
# from app import HttpError, bcrypt
# from models import UserModel, Session
#
#
# def get_by_id(item_id: int, orm_model: Type[UserModel], session: Session):
#     orm_item = session.query(orm_model).get(item_id)
#
#     if orm_item is None:
#         raise HttpError(404, 'item not found')
#
#     return orm_item
#
#
# def get_user_id(item_json: dict, orm_model: Type[UserModel], session: Session):
#     user = session.query(orm_model).filter_by(name=item_json['name']).first()
#
#     pw_hash = bcrypt.generate_password_hash('secret')
#     print(f'pw_hash: {pw_hash}')
#     print(bcrypt.check_password_hash(pw_hash, 'secret'))
#
#     if user is None:
#         raise HttpError(404, 'user not found')
#
#     if not bcrypt.check_password_hash(user.password, item_json['password']):
#         raise HttpError(403, f'wrong password')
#
#     return user.id