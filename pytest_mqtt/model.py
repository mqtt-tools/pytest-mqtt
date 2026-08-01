from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class MqttMessage:
    """
    Container for `capmqtt`'s `message` response items.
    """

    topic: str
    payload: str | bytes
    userdata: None | dict


@dataclasses.dataclass
class MqttSettings:
    host: str
    port: int
    username: str
    password: str
    subscribe_all: bool
