import pytest

from pytest_mqtt.model import MqttMessage


def test_basic_submit_text_receive_binary(mosquitto, capmqtt):
    """
    Basic submit/receive roundtrip, with ASCII text payload (`str`).
    Without further ado, the payloads will be received as `bytes`.
    """
    # Submit two MQTT messages.
    capmqtt.publish(topic="foo", payload="bar")
    capmqtt.publish(topic="baz", payload="qux")

    # Demonstrate the `messages` property.
    assert capmqtt.messages == [
        MqttMessage(topic="foo", payload=b"bar", userdata=None),
        MqttMessage(topic="baz", payload=b"qux", userdata=None),
    ]

    # Demonstrate the `records` property.
    assert capmqtt.records == [
        ("foo", b"bar", None),
        ("baz", b"qux", None),
    ]


def test_basic_submit_and_receive_binary(mosquitto, capmqtt):
    """
    Basic submit/receive roundtrip, with binary payload (`bytes`).
    """

    # Submit two MQTT messages.
    capmqtt.publish(topic="foo", payload=b"bar")
    capmqtt.publish(topic="baz", payload=b"qux")

    # Demonstrate the `messages` property.
    assert capmqtt.messages == [
        MqttMessage(topic="foo", payload=b"bar", userdata=None),
        MqttMessage(topic="baz", payload=b"qux", userdata=None),
    ]

    # Demonstrate the `records` property.
    assert capmqtt.records == [
        ("foo", b"bar", None),
        ("baz", b"qux", None),
    ]


@pytest.mark.capmqtt_decode_utf8
def test_basic_submit_text_receive_text_marker(mosquitto, capmqtt):
    """
    Basic submit/receive roundtrip, with ASCII text payload (`str`).
    By using the `capmqtt_decode_utf8` marker, the payloads will also be received
    as `str`, after decoding them from `utf-8`.
    """

    # Submit two MQTT messages.
    capmqtt.publish(topic="foo", payload="bar")
    capmqtt.publish(topic="baz", payload="qux")

    # Demonstrate the `messages` property.
    assert capmqtt.messages == [
        MqttMessage(topic="foo", payload="bar", userdata=None),
        MqttMessage(topic="baz", payload="qux", userdata=None),
    ]

    # Demonstrate the `records` property.
    assert capmqtt.records == [
        ("foo", "bar", None),
        ("baz", "qux", None),
    ]


@pytest.fixture
def configure_capmqtt_decode_utf8(pytestconfig):
    pytestconfig.option.capmqtt_decode_utf8 = True


def test_basic_submit_text_receive_text_config(configure_capmqtt_decode_utf8, mosquitto, capmqtt):
    """
    Basic submit/receive roundtrip, with ASCII text payload (`str`).
    By using the global `capmqtt_decode_utf8` config option, the payloads
    will also be received as `str`, after decoding them from `utf-8`.
    """

    # Submit two MQTT messages.
    capmqtt.publish(topic="foo", payload="bar")
    capmqtt.publish(topic="baz", payload="qux")

    # Demonstrate the `messages` property.
    assert capmqtt.messages == [
        MqttMessage(topic="foo", payload="bar", userdata=None),
        MqttMessage(topic="baz", payload="qux", userdata=None),
    ]

    # Demonstrate the `records` property.
    assert capmqtt.records == [
        ("foo", "bar", None),
        ("baz", "qux", None),
    ]
