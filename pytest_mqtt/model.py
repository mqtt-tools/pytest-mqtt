import dataclasses
import typing as t


@dataclasses.dataclass
class MqttMessage:
    """
    Container for `capmqtt`'s `message` response items.
    """

    topic: str
    payload: t.Union[str, bytes]
    userdata: t.Optional[t.Union[t.Dict, None]]
