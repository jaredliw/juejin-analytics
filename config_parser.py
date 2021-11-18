import configparser

from __init__ import config_filename
from check_in import get_check_in_status, get_check_in_days, get_total_points
from users import get_profile


# noinspection PyMissingOrEmptyDocstring
class ConfigParser(configparser.ConfigParser):
    def read(self, filenames, encoding="utf-8"):
        super().read(filenames, encoding)
    
    def write(self, filename, encoding="utf-8"):
        with open(filename, "w", encoding=encoding) as file:
            super().write(file)


if __name__ == "__main__":
    parser = ConfigParser()
    parser.read(config_filename)

    user_data = get_profile()
    parser["user"] = {
        "user_id": user_data["user_id"],
        "username": user_data["user_name"],
        "level": user_data["level"],
        "power": user_data["power"]
    }

    parser["check_in"] = {
        "status": get_check_in_status(),
        "day": get_check_in_days()["sum_count"],
        "point": get_total_points()
    }

    parser.write(config_filename)
