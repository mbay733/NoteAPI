from api import app, docs
from config import Config
from api.handlers import user

# Для добавления в Swagger необходимо выполнить регистрацию очередного endpoint'a
docs.register(user.get_user_by_id)
docs.register(user.create_user)
docs.register(user.edit_user)
docs.register(user.delete_user)
docs.register(user.get_users)


if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)