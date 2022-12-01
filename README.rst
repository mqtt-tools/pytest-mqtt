.. image:: https://github.com/mqtt-tools/pytest-mqtt/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/mqtt-tools/pytest-mqtt/actions/workflows/tests.yml
    :alt: CI outcome

.. image:: https://codecov.io/gh/mqtt-tools/pytest-mqtt/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/mqtt-tools/pytest-mqtt
    :alt: Test suite code coverage

.. image:: https://pepy.tech/badge/pytest-mqtt/month
    :target: https://pepy.tech/project/pytest-mqtt
    :alt: PyPI downloads per month

.. image:: https://img.shields.io/pypi/v/pytest-mqtt.svg
    :target: https://pypi.org/project/pytest-mqtt/
    :alt: Package version on PyPI

.. image:: https://img.shields.io/pypi/status/pytest-mqtt.svg
    :target: https://pypi.org/project/pytest-mqtt/
    :alt: Project status (alpha, beta, stable)

.. image:: https://img.shields.io/pypi/pyversions/pytest-mqtt.svg
    :target: https://pypi.org/project/pytest-mqtt/
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/l/pytest-mqtt.svg
    :target: https://github.com/mqtt-tools/pytest-mqtt/blob/main/LICENSE
    :alt: Project license

|

###########
pytest-mqtt
###########


*****
About
*****

``pytest-mqtt`` supports testing systems based on MQTT by providing test
fixtures for ``pytest``. It has been conceived for the fine
`terkin-datalogger`_ and `mqttwarn`_ programs.

``capmqtt`` fixture
===================

Capture MQTT messages, using the `Paho MQTT Python Client`_, in the spirit of
``caplog`` and ``capsys``. It can also be used to publish MQTT messages.

``mosquitto`` fixture
=====================

Provide the `Mosquitto`_ MQTT broker as a session-scoped fixture to your test
cases.


*****
Usage
*****

::

    from pytest_mqtt.model import MqttMessage

    @pytest.mark.capmqtt_decode_utf8
    def test_mqtt_send_receive(mosquitto, capmqtt):
        """
        Basic send/receive roundtrip, using text payload (`str`).

        By using the `capmqtt_decode_utf8` marker, the message payloads
        will be recorded as `str`, after decoding them from `utf-8`.
        Otherwise, message payloads would be recorded as `bytes`.
        """

        # Submit a basic MQTT message.
        capmqtt.publish(topic="foo", payload="bar")

        # Demonstrate the "messages" property.
        # It returns a list of "MqttMessage" objects.
        assert capmqtt.messages == [
            MqttMessage(topic="foo", payload="bar", userdata=None),
        ]

        # Demonstrate the "records" property.
        # It returns tuples of "(topic, payload, userdata)".
        assert capmqtt.records == [
            ("foo", "bar", None),
        ]


The ``capmqtt_decode_utf8`` setting can be enabled in three ways.


1. Session-wide, per ``pytestconfig`` option, for example within ``conftest.py``::

      @pytest.fixture(scope="session", autouse=True)
      def configure_capmqtt_decode_utf8(pytestconfig):
          pytestconfig.option.capmqtt_decode_utf8 = True

2. On the module level, just say ``capmqtt_decode_utf8 = True`` on top of your file.
3. On individual test cases as a test case marker, using ``@pytest.mark.capmqtt_decode_utf8``.


******
Issues
******

- Both fixtures currently do not support changing the MQTT broker hostname and
  port number differently than ``localhost:1883``.

- The ``mosquitto`` fixture currently does not support either authentication or
  encryption.

- ``capmqtt`` should be able to capture messages only from specified topics.


***********
Development
***********

::

    git clone https://github.com/mqtt-tools/pytest-mqtt
    cd pytest-mqtt
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --editable=.[test,develop]
    poe test


*******************
Project information
*******************

Contributions
=============

Every kind of contribution, feedback, or patch, is much welcome. `Create an
issue`_ or submit a patch if you think we should include a new feature, or to
report or fix a bug.

Resources
=========

- `Source code <https://github.com/mqtt-tools/pytest-mqtt>`_
- `Documentation <https://github.com/mqtt-tools/pytest-mqtt>`_
- `Python Package Index (PyPI) <https://pypi.org/project/pytest-mqtt/>`_

License
=======

The project is licensed under the terms of the MIT license, see `LICENSE`_.


.. _Create an issue: https://github.com/mqtt-tools/pytest-mqtt/issues/new
.. _LICENSE: https://github.com/mqtt-tools/pytest-mqtt/blob/main/LICENSE
.. _Mosquitto: https://github.com/eclipse/mosquitto
.. _mqttwarn: https://github.com/jpmens/mqttwarn/
.. _Paho MQTT Python Client: https://github.com/eclipse/paho.mqtt.python
.. _terkin-datalogger: https://github.com/hiveeyes/terkin-datalogger/
