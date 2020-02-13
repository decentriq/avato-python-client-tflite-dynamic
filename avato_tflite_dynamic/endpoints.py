from enum import Enum
from avato.api import AVATO_ACTIVE_INSTANCE_INFIX


class Endpoints(str, Enum):
    # TFLITE Dynamic Instance specific
    POST_DYNAMIC_MESSAGE = AVATO_ACTIVE_INSTANCE_INFIX + "/dynamicMessage"
