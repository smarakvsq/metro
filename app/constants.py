import os.path as op


class TransportType:
    RAIL = "rail"
    BUS = "bus"
    SYSTEM_WIDE = "systemwide"


class PageType:
    CRIME = "crime"
    ARREST = "arrest"
    CALLS_FOR_SERVICE = "calls_for_service"


class Vet:
    VETTED = True
    UNVETTED = False


class CrimeSectionHeading:
    SERIOUS_CRIME = "serious_crime"
    systemwide_crime = "systemwide_crime"
    AGENCY_WIDE = "agency_wide"


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