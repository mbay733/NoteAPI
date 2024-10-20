from api import ma
from api.models.user import UserModel


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel
        fields = ('id', 'username', "role")


user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Десериализация запроса("put" request)
class UserEditSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

    username = ma.Str()
    role = ma.Str()


# Десериализация запроса("post" request)
class UserRequestSchema(UserEditSchema):
    password = ma.Str()