from enum import Enum


class Configuration(object):
    DEBUG: bool = True


class TypeSocial(str, Enum):
    yandex = "yandex"
    google = "google"
