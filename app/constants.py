import os.path as op


class TransportType:
    RAIL = "rail"
    BUS = "bus"
    SYSTEM_WIDE = "systemwide"


class PageType:
    CRIME = "crime"
    ARREST = "arrest"
    CALLS_FOR_SERVICE = "calls_for_service"
    LANDING_PAGE = "landing_page"


class Vet:
    VETTED = True
    UNVETTED = False


class GraphType:
    BAR = "bar"
    LINE = "line"
    PIE = "pie"
    GEO = "geo"


class Gender:
    MALE = "male"
    FEMALE = "female"


class CrimeSeverity:
    VIOLENT_CRIME = "violent_crime"
    SYSTEM_WIDE_CRIME = "systemwide_crime"


class Ucr:
    PERSONS = "persons"


class FilePath:
    APP_LOG_PATH = op.join(op.dirname(op.dirname(__file__)), "logs", "app")
    TASK_LOG_PATH = op.join(op.dirname(op.dirname(__file__)), "logs", "task")


class Auth:
    SECRET_KEY = b"pKFBkgvH7eonpbf2iIdorgt6D56Ys44aU8WT-HFDivQ="
