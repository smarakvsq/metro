class TransportType:
    RAIL = "rail"
    BUS = "bus"
    SYSTEM_WIDE = "systemwide"


class PageType:
    CRIME = "crime"
    ARREST = "arrest"
    CALL_FOR_SERVICE = "call_for_service"


class Vet:
    VETTED = True
    UNVETTED = False


class CrimeSectionHeading:
    SERIOUS_CRIME = "serious_crime"
    GENERAL_CRIME = "general_crime"
    AGENCY_WIDE = "agency_wide"


class GraphType:
    BAR = "bar"
    LINE = "line"
    PIE = "pie"
    GEO = "geo"