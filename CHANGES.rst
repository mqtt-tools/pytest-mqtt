#####################
pytest-mqtt changelog
#####################


in progress
===========
- paho-mqtt: Ignore deprecation warnings about Callback API v1
- mosquitto: Don't always pull OCI image
- Updated Paho API version to V2. Thank you, @hyperspacex2.

2024-07-29 0.4.2
================
- Added a little delay to the Mosquitto fixture. Possibly faster GitHub
  runners made MQTT software tests fail on the LorryStream project.

2024-05-08 0.4.1
================
- Fix command line options machinery by refactoring essential
  pytest fixtures to the main package. They have been added to ``testing``
  beforehand, which is just plain wrong, and broke the 0.4.0 release.

2024-03-31 0.4.0
================
- Accept command line options ``--mqtt-host`` and ``--mqtt-port``,
  in order to connect to an MQTT broker on a different endpoint
  than ``localhost:1883``. Thanks, @zedfmario.
- Add support for paho-mqtt 2.x, retaining compatibility for 1.x

2023-08-03 0.3.1
================

- Fix improving error handling when Docker daemon is not running.


2023-07-28 0.3.0
================

- Improve error handling when Docker daemon is not running. Thanks, @horta.


2023-03-15 0.2.0
================

- Mosquitto fixture: Add missing ``port`` attribute and fix return tuple
  of ``BaseImage.run``. Thanks, @edenhaus!


2022-09-20 0.1.0
================

- Initial commit, spawned from Terkin and mqttwarn.
