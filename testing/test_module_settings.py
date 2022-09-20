from pytest_mqtt.model import MqttMessage

# Configure `capmqtt` to return `MqttMessage.payload` as `str`, decoded from `utf-8`.
capmqtt_decode_utf8 = True


def test_basic_submit_text_receive_text(mosquitto, capmqtt):
    """
    Basic submit/receive roundtrip, with ASCII text payload (`str`).
    By using the module-wide `capmqtt_decode_utf8` setting, the payloads
    will also be received as `str`, after decoding them from `utf-8`.
    """

    # Submit MQTT message.
    capmqtt.publish(topic="foo", payload="bar")

    # Demonstrate `messages` property.
    assert capmqtt.messages == [
        MqttMessage(topic="foo", payload="bar", userdata=None),
    ]

    # Demonstrate `records` property.
    assert capmqtt.records == [
        ("foo", "bar", None),
    ]
