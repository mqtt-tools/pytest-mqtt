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

from pytest_mqtt.model import MqttMessage
from pytest_mqtt.util import delay

logger = logging.getLogger(__name__)


class MqttClientAdapter(threading.Thread):
    def __init__(self, on_message_callback: t.Optional[t.Callable] = None):
        super().__init__()
        self.client: mqtt.Client = mqtt.Client()
        self.on_message_callback = on_message_callback
        self.setup()

    def setup(self):
        client = self.client
        client.on_socket_open = self.on_socket_open
        client.on_connect = self.on_connect
        client.on_subscribe = self.on_subscribe
        client.on_message = self.on_message
        if self.on_message_callback:
            client.on_message = self.on_message_callback

        logger.debug("[PYTEST] Connecting to MQTT broker")
        client.connect("localhost", port=1883)
        client.subscribe("#")

    def run(self):
        self.client.loop_start()

    def stop(self):
        logger.debug("[PYTEST] Disconnecting from MQTT broker")
        self.client.disconnect()
        self.client.loop_stop()

    def on_socket_open(self, client, userdata, sock):
        logger.debug("[PYTEST] Opened socket to MQTT broker")

    def on_connect(self, client, userdata, flags, rc):
        logger.debug("[PYTEST] Connected to MQTT broker")

    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        logger.debug("[PYTEST] Subscribed to MQTT topic(s)")

    def on_message(self, client, userdata, msg):
        logger.debug("[PYTEST] MQTT message received: %s", msg)

    def publish(self, topic: str, payload: str, **kwargs) -> mqtt.MQTTMessageInfo:
        message_info = self.client.publish(topic, payload, **kwargs)
        message_info.wait_for_publish()
        return message_info


class MqttCaptureFixture:
    """Provides access and control of log capturing."""

    def __init__(self, decode_utf8: t.Optional[bool]) -> None:
        """Creates a new funcarg."""
        self._buffer: t.List[MqttMessage] = []
        self._decode_utf8: bool = decode_utf8

        self.mqtt_client = MqttClientAdapter(on_message_callback=self.on_message)
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
    def records(self) -> t.List[t.Tuple[str, t.Union[str, bytes], t.Dict]]:
        return [(item.topic, item.payload, item.userdata) for item in self._buffer]

    def publish(self, topic: str, payload: str, **kwargs) -> mqtt.MQTTMessageInfo:
        message_info = self.mqtt_client.publish(topic=topic, payload=payload, **kwargs)
        # Make the MQTT client publish and receive the message.
        delay()
        return message_info


@pytest.fixture(scope="function")
def capmqtt(request):
    """Access and control MQTT messages."""

    # Configure `capmqtt` fixture, obtaining the `capmqtt_decode_utf8` setting from
    # either a global or module-wide setting, or from a test case marker.
    # https://docs.pytest.org/en/7.1.x/how-to/fixtures.html#fixtures-can-introspect-the-requesting-test-context
    # https://docs.pytest.org/en/7.1.x/how-to/fixtures.html#using-markers-to-pass-data-to-fixtures
    capmqtt_decode_utf8 = (
        getattr(request.config.option, "capmqtt_decode_utf8", False)
        or getattr(request.module, "capmqtt_decode_utf8", False)
        or request.node.get_closest_marker("capmqtt_decode_utf8") is not None
    )

    result = MqttCaptureFixture(decode_utf8=capmqtt_decode_utf8)
    delay()
    yield result
    result.finalize()
