# -*- coding: utf-8 -*-

# Copyright (c) 2020-2022 Andreas Motl <andreas.motl@panodata.org>
# Copyright (c) 2020-2022 Richard Pobering <richard.pobering@panodata.org>
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
"""
Provide the `Mosquitto`_ MQTT broker as a session-scoped fixture to your test
harness.

Source: https://github.com/hiveeyes/terkin-datalogger/blob/0.13.0/test/fixtures/mosquitto.py

.. _Mosquitto: https://github.com/eclipse/mosquitto
"""
import os

import docker
import pytest
from pytest_docker_fixtures import images
from pytest_docker_fixtures.containers._base import BaseImage

from pytest_mqtt.model import MqttSettings
from pytest_mqtt.util import probe_tcp_connect

images.settings["mosquitto"] = {
    "image": "eclipse-mosquitto",
    "version": "2.0.15",
    "options": {
        "command": "mosquitto -c /mosquitto-no-auth.conf",
        "publish_all_ports": False,
        "ports": {"1883/tcp": "1883"},
    },
}


class Mosquitto(BaseImage):

    name = "mosquitto"

    def __init__(self, host: str = "localhost", port: int = 1883) -> None:
        self.host = host
        self.port = port

    def check(self):
        # TODO: Add real implementation.
        return True

    def pull_image(self):
        """
        Image needs to be pulled explicitly.
        Workaround against `404 Client Error: Not Found for url: http+docker://localhost/v1.23/containers/create`.

        - https://github.com/jpmens/mqttwarn/pull/589#issuecomment-1249680740
        - https://github.com/docker/docker-py/issues/2101
        """
        docker_client = docker.from_env(version=self.docker_version)
        image_name = self.image
        docker_client.images.pull(image_name)

    def run(self):
        try:
            docker_client = docker.from_env(version=self.docker_version)
            docker_url = docker_client.api.base_url
        except Exception:
            raise ConnectionError("Cannot connect to the Docker daemon. Is the docker daemon running?")
        try:
            docker_client.ping()
        except Exception:
            raise ConnectionError(f"Cannot connect to the Docker daemon at {docker_url}. Is the docker daemon running?")
        self.pull_image()
        return super(Mosquitto, self).run()


mosquitto_image = Mosquitto()


def is_mosquitto_running(host: str, port: int) -> bool:
    return probe_tcp_connect(host, port)


def pytest_addoption(parser) -> None:
    parser.addoption("--mqtt-host", action="store", type=str, default="localhost", help="MQTT host name")
    parser.addoption("--mqtt-port", action="store", type=int, default=1883, help="MQTT port number")


@pytest.fixture(scope="session")
def mqtt_settings(pytestconfig) -> MqttSettings:
    return MqttSettings(
        host=pytestconfig.getoption("--mqtt-host"),
        port=pytestconfig.getoption("--mqtt-port"),
    )


@pytest.fixture(scope="session")
def mosquitto(mqtt_settings: MqttSettings):

    host, port = mqtt_settings.host, mqtt_settings.port

    # Gracefully skip spinning up the Docker container if Mosquitto is already running.
    if is_mosquitto_running(host, port):
        yield host, port
        return

    # Spin up Mosquitto container.
    if os.environ.get("MOSQUITTO"):
        yield os.environ["MOSQUITTO"].split(":")
    else:
        yield mosquitto_image.run()
        mosquitto_image.stop()
