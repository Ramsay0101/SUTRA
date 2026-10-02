from enum import Enum

class SuiteCategory(str, Enum):
    LEARNING= "learning"
    INSTRUCTION= "instruction"
    COMMAND= "command"
    GUARDIAN= "guardian"
    WELFARE= "welfare"

class CustomFieldType(str, Enum):
    # Text & Content
    TEXT = "text"
    LONG_TEXT = "long_text"
    EMAIL = "email"
    PHONE = "phone"
    URL = "url"

    # Numerical
    INTEGER = "integer"
    DECIMAL = "decimal"
    PERCENTAGE = "percentage"
    CURRENCY = "currency"

    # Date & Time
    DATE = "date"
    DATETIME = "datetime"
    TIME = "time"

    # Choice & Boolean
    BOOLEAN = "boolean"
    SINGLE_SELECT = "single_select"
    MULTI_SELECT = "multi_select"

    # Relational & Structured
    LOOKUP = "lookup"
    FILE_ATTACHMENT = "file_attachment"
    JSON_OBJECT = "json_object"
