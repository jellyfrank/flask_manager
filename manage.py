from types import ModuleType
from flask_script import Manager, Server
from app import app, db
from app import model
import inspect
from flask_migrate import Migrate, MigrateCommand

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command("db", MigrateCommand)
manager.add_command("server", Server())


@manager.shell
def make_shell_context():
    model_class = {
        k: v for key, value in inspect.getmembers(model) if inspect.ismodule(
            value) for k, v in inspect.getmembers(value) if inspect.isclass(v)
        and issubclass(v, db.Model)
    }
    model_class.update(dict(app=app, db=db))
    return model_class


if __name__ == "__main__":
    manager.run()
