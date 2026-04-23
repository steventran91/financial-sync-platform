from backend.app.db.base import Base
from backend.app.db.session import engine
from backend.app.db.models import SyncJobDB


def main():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")


if __name__ == "__main__":
    main()