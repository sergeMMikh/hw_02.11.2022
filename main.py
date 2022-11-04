from models import Base, engine
from urls import app


if __name__ == '__main__':

    Base.metadata.create_all(engine)

    app.run()
