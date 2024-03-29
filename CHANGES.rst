#####################
pytest-mqtt changelog
#####################


in progress
===========
- Accept command line options ``--mqtt-host`` and ``--mqtt-port``,
  in order to connect to an MQTT broker on a different endpoint
  than ``localhost:1883``. Thanks, @zedfmario.


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
