def pytest_addoption(parser) -> None:
    parser.addoption("--mqtt_host", action="store", default="localhost", help="mqtt host to be connected through")
    parser.addoption("--mqtt_port", action="store", default=1883, help="mqtt port to be connected through")
