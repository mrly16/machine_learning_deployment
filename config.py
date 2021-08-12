import configparser
import os

from constant import CONFIG_PATH


class Config:
    def __init__(self):
        config_file_path = os.path.join(os.path.dirname(__file__), CONFIG_PATH)
        self.conf = configparser.ConfigParser()
        self.conf.read(config_file_path, encoding="utf-8")

    @property
    def PG_HOST(self):
        host = self.conf.get("data_warehouse", "PG_HOST")
        return host

    @property
    def PG_PORT(self):
        port = self.conf.get("data_warehouse", "PG_PORT")
        return port

    @property
    def PG_PASSWORD(self):
        password = self.conf.get("data_warehouse", "PG_PASSWORD")
        return password

    @property
    def PG_USER(self):
        user = self.conf.get("data_warehouse", "PG_USER")
        return user

    @property
    def PG_DBNAME(self):
        dbname = self.conf.get("data_warehouse", "PG_DBNAME")
        return dbname


config = Config()
