from calendar import c
from datetime import datetime, timedelta

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from src.utils.Logger import Logger
from src.utils.Dotenv import Dotenv
from src.languages.Ru import MONTHS_RU
from src.users.InitialUsers import InitialUsers

from src.data.schedule_days import SCHEDULE_DAYS


#! Когда-нибудь руки дойдут до хеширования данных (как минимум: user_id, real_name)


class MongoDB:
    _mongoDB_instance = None

    client: MongoClient = None

    database: Database = None
    replica_db: Database = None

    def __new__(cls, *args, **kwargs):
        DATABASE_NAME = "school-bot"
        REPLICA_DB_NAME = "replica"

        MONGO_URI = Dotenv().mongodb_string

        if cls._mongoDB_instance is None:
            cls._mongoDB_instance = super().__new__(cls)
            cls._mongoDB_instance.client = MongoClient(MONGO_URI, maxPoolSize=1)
            cls._mongoDB_instance.database = cls._mongoDB_instance.client[DATABASE_NAME]
            cls._mongoDB_instance.replica_db = cls._mongoDB_instance.client[
                REPLICA_DB_NAME
            ]

            Logger().info(f"База данных {DATABASE_NAME} подключена!")

        return cls._mongoDB_instance

    def __init__(self) -> None:
        self.log = Logger().info
        self.dotenv = Dotenv()

        # ? bot's collections
        self.users_collection: Collection = self.database["users"]
        self.versions_collection: Collection = self.database["versions"]
        self.schedule_collection: Collection = self.database["schedule"]

        #? handles schedule days
        self.ScheduleDays = ScheduleDays(self.schedule_collection)

    def show_users(self):
        self.log(f"Коллекция юзеров: {list(self.users_collection.find({}))}")

    def get_all_users(self):
        return list(self.users_collection.find({}))

    def get_all_versions(self):
        return list(self.versions_collection.find({}))

    def get_replica_documents(self, collection_name="users"):
        return list(self.replica_db[collection_name].find({}))

    def get_all_documents(self, database_name="school-bot", collection_name="users"):
        database = self.client[database_name]

        return list(database[collection_name].find({}))

    def check_if_user_exists(self):
        """returns True if user is in the collection, False - if not"""
        user = self.users_collection.find_one({"user_id": self.user_id})

        if user:
            # self.log(f"Чувачок (чувиха) с id {self.user_id} уже зарегистрирован(а) в БД")
            return True
        else:
            # self.log(f"Новенький юзер с id {self.user_id}! Сохраняю в базу данных... 😋")
            return False

    def save_user(self, new_user: dict) -> None:
        self.users_collection.insert_one(new_user)
        # self.log(f"before: { new_user }  ⏳ ")

        self.log(f"Юзер с id { new_user["user_id"] } сохранён в БД ⏳ ")

    def remove_user(self, user_id: int) -> None:
        filter = {"user_id": user_id}
        self.users_collection.delete_one(filter=filter)
        print(f"User removed from MongoDB!")

    def update_user(self, user_id: int, key: str, new_value: str | int | bool):
        filter_by_id = {"user_id": user_id}
        update_operation = {"$set": {key: new_value}}

        self.users_collection.update_one(filter=filter_by_id, update=update_operation)

    # ? Admin commands

    def clean_users(self):
        admin_ids = InitialUsers().admin_ids
        delete_filter = {"user_id": {"$nin": admin_ids}}

        self.users_collection.delete_many(filter=delete_filter)
        self.log(f"Коллекция пользователей MongoDB очищена! 🧹")

    # ? Versions
    def get_latest_versions_info(self, versions_limit: int = 3):
        self.versions_collection = self.database["versions"]
        latest_versions = list(
            self.versions_collection.find({}).sort("id", -1).limit(versions_limit)
        )

        latest_versions.reverse()
        print("🐍 latest_versions from mongo: ", latest_versions)

        return latest_versions

    def send_new_version_update(self, version_number: int, changelog: str):
        now = datetime.now()

        if Dotenv().environment == "production":
            now = now + timedelta(hours=3)

        current_time = now.strftime(f"%d {MONTHS_RU[now.month]}, %H:%M")

        versions_count = self.versions_collection.count_documents({})

        new_update = {
            "id": versions_count + 1,
            "date": current_time,
            "version": version_number,
            "changelog": changelog,
        }

        self.versions_collection.insert_one(new_update)

        self.log(f"⌛ New version { version_number } published! ")

    def replicate_collection(self, collection_name: str = "users"):
        """replicates users or versions collection"""
        existing_documents = self.get_all_users()

        if collection_name == "versions":
            existing_documents = self.get_all_versions()

        replica_collection = self.replica_db[collection_name]

        # ? clear replica
        replica_collection.delete_many({})
        replica_collection.insert_many(existing_documents)

        self.log(f"Коллекция {collection_name} успешно реплицирована 🐱‍🐉")

    def load_replica(self, collection_name: str = "users"):
        collection_to_erase = self.database[collection_name]
        collection_to_erase.delete_many({})

        new_documents = self.get_all_documents(
            database_name="replica", collection_name=collection_name
        )

        collection_to_erase.insert_many(new_documents)

        self.log(
            f"Коллекция {collection_name} успешно восстановлена из реплики в основную базу данных! 🐱‍🐉"
        )


class ScheduleDays:
    def __init__(self, schedule_collection: Collection):
        self.schedule_collection = schedule_collection
        self.days = list(schedule_collection.find({}))
        # print("🐍 self.days", self.days)

    def check_days_integrity(self):
        if len(self.days) < 7:
            print("Не все дни в порядке...")
            self.create_days()
        else: print("Все 7 дней расписания на месте!")

    def create_days(self):
        for day in SCHEDULE_DAYS:
            self.schedule_collection.insert_one(day)
            print(f"day {day} created in schedule!")

    def change_day_schedule(self, day_id, new_schedule):
        for day in self.days:
            self.logger.info(f"day: {day}")
            if day["id"] == day_id:
                day["lessons"] = new_schedule
                print(f"{day["lessons"]} changed for {new_schedule}")