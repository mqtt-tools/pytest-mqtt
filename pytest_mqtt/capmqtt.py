# -*- coding: utf-8 -*-
# Copyright (c) 2020-2022 Andreas Motl <andreas.motl@panodata.org>
# Copyright (c) 2020-2022 Richard Pobering <richard.pobering@panodata.org>
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
"""
Capture MQTT messages, using the `Paho MQTT Python Client`_, in the spirit of
`caplog` and `capsys`.

Source: https://github.com/hiveeyes/terkin-datalogger/blob/0.13.0/test/fixtures/mqtt.py

.. _Paho MQTT Python Client: https://github.com/eclipse/paho.mqtt.python
"""

import logging
import threading
import typing as t

import paho.mqtt.client as mqtt
import pytest

from pytest_mqtt.model import MqttMessage, MqttSettings
from pytest_mqtt.util import delay

logger = logging.getLogger(__name__)


class MqttClientAdapter(threading.Thread):
    def __init__(
        self,
        on_message_callback: t.Optional[t.Callable] = None,
        host: str = "localhost",
        port: int = 1883,
        username: str = "guest",
        password: str = "guest",
        subscribe_all: bool = True,
    ):
        super().__init__()
        self.client: mqtt.Client
        if not hasattr(mqtt, "CallbackAPIVersion"):
            # paho-mqtt 1.x
            self.client = mqtt.Client()
            self.use_legacy_api = True
        else:
            # paho-mqtt 2.x
            self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
            self.use_legacy_api = False
        self.on_message_callback = on_message_callback
        self.host = host
        self.port = int(port)
        self.username = username
        self.password = password
        self.subscribe_all = subscribe_all

        self.setup()

    def setup(self) -> None:
        client = self.client
        client.on_socket_open = self.on_socket_open
        client.on_connect = self.on_connect_v1 if self.use_legacy_api else self.on_connect
        client.on_subscribe = self.on_subscribe_v1 if self.use_legacy_api else self.on_subscribe
        client.on_message = self.on_message
        if self.on_message_callback:
            client.on_message = self.on_message_callback
        client.username_pw_set(self.username, self.password)

        logger.debug("[PYTEST] Connecting to MQTT broker")
        client.connect(host=self.host, port=self.port)
        if self.subscribe_all:
            client.subscribe("#")

    def run(self) -> None:
        self.client.loop_start()

    def stop(self) -> None:
        logger.debug("[PYTEST] Disconnecting from MQTT broker")
        self.client.disconnect()
        self.client.loop_stop()

    def on_socket_open(self, client: mqtt.Client, userdata, sock) -> None:
        logger.debug("[PYTEST] Opened socket to MQTT broker")

    def on_connect_v1(self, client: mqtt.Client, userdata, flags, rc) -> None:  # legacy API version 1
        logger.debug("[PYTEST] Connected to MQTT broker")

    def on_connect(self, client: mqtt.Client, userdata, flags, reason_code, properties) -> None:
        logger.debug("[PYTEST] Connected to MQTT broker")

    def on_subscribe_v1(
        self, client: mqtt.Client, userdata, mid, granted_qos, properties=None
    ) -> None:  # legacy API version 1
        logger.debug("[PYTEST] Subscribed to MQTT topic(s)")

    def on_subscribe(self, client: mqtt.Client, userdata, mid, reason_codes, properties) -> None:
        logger.debug("[PYTEST] Subscribed to MQTT topic(s)")

    def on_message(self, client, userdata, msg):
        logger.debug("[PYTEST] MQTT message received: %s", msg)

    def publish(
        self,
        topic: str,
        payload: t.Union[str, bytes, bytearray, int, float, None],
        **kwargs,
    ) -> mqtt.MQTTMessageInfo:
        message_info = self.client.publish(topic, payload, **kwargs)
        message_info.wait_for_publish()
        return message_info


class MqttCaptureFixture:
    """Provides access and control of log capturing."""

    def __init__(
        self,
        decode_utf8: t.Optional[bool],
        host: str = "localhost",
        port: int = 1883,
        username: str = "guest",
        password: str = "guest",
        subscribe_all: bool = True,
    ) -> None:
        """Creates a new funcarg."""
        self._buffer: t.List[MqttMessage] = []
        self._decode_utf8: bool = decode_utf8 or False

        self.mqtt_client = MqttClientAdapter(
            on_message_callback=self.on_message, host=host, port=port, username=username, password=password, subscribe_all=subscribe_all
        )
        self.mqtt_client.start()
        # time.sleep(0.1)

    def on_message(self, client, userdata, msg):
        payload = msg.payload
        if self._decode_utf8:
            payload = payload.decode("utf-8")

        message = MqttMessage(
            topic=msg.topic,
            payload=payload,
            userdata=userdata,
        )
        self._buffer.append(message)
        logger.debug("[PYTEST] MQTT message received: %s", str(message)[:200])

    def finalize(self) -> None:
        """Finalizes the fixture."""
        self.mqtt_client.stop()
        self.mqtt_client.join(timeout=4.2)
        self._buffer = []

    @property
    def messages(self) -> t.List[MqttMessage]:
        return self._buffer

    @property
    def records(self) -> t.List[t.Tuple[str, t.Union[str, bytes], t.Union[t.Dict, None]]]:
        return [(item.topic, item.payload, item.userdata) for item in self._buffer]

    def publish(
        self,
        topic: str,
        payload: t.Union[str, bytes, bytearray, int, float, None],
        **kwargs,
    ) -> mqtt.MQTTMessageInfo:
        message_info = self.mqtt_client.publish(topic=topic, payload=payload, **kwargs)
        # Make the MQTT client publish and receive the message.
        delay()
        return message_info


@pytest.fixture(scope="function")
def capmqtt(request, mqtt_settings: MqttSettings):
    """Access and control MQTT messages."""

    # Configure `capmqtt` fixture, obtaining the `capmqtt_decode_utf8` setting from
    # either a global or module-wide setting, or from a test case marker.
    # https://docs.pytest.org/en/7.1.x/how-to/fixtures.html#fixtures-can-introspect-the-requesting-test-context
    # https://docs.pytest.org/en/7.1.x/how-to/fixtures.html#using-markers-to-pass-data-to-fixtures

    host, port = mqtt_settings.host, mqtt_settings.port
    username, password = mqtt_settings.username, mqtt_settings.password
    subscribe_all = mqtt_settings.subscribe_all

    capmqtt_decode_utf8 = (
        getattr(request.config.option, "capmqtt_decode_utf8", False)
        or getattr(request.module, "capmqtt_decode_utf8", False)
        or request.node.get_closest_marker("capmqtt_decode_utf8") is not None
    )
    result = MqttCaptureFixture(
        decode_utf8=capmqtt_decode_utf8, host=host, port=port, username=username, password=password, subscribe_all=subscribe_all
    )
    delay()
    yield result
    result.finalize()
