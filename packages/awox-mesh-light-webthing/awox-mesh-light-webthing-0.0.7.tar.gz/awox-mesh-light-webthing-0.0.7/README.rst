========================
AWOX-MESH-LIGHT-WEBTHING
========================

|GitHub|
|License|
|PyPi|
|Fediverse|

Webthings RESTful API for Awox's "SmartLight" (SKRLm-c9-E27).

This lightbulb is supporting Bluetooth mesh.

.. image:: https://peertube.mastodon.host/static/previews/058df607-2ca9-4a2c-be42-286644e5071e.jpg
   :target: https://mastodon.social/@rzr/104250255817500884#

USAGE
=====

Prerequisite, smart light BLE's network configuration
should be first set from any system supporting BLE as
explained on following page.
Success has been reported using Raspberry Pi3+
or some USB dongle (eg: 0a12:0001)

* https://github.com/Leiaz/python-awox-mesh-light
  
For WebThings users, addon can be installed from the addon repository:

* http://gateway.local:8080/settings/addons/discovered

Then once added and enabled, mesh's credentials should be configured from addon page:

* http://gateway.local:8080/settings/addons/

Note: Mesh's default name is "unpaired" and "1234" is default password.

For developers, check standalone webthing example:

::

   MAC=A4:C1:38:FF:FF:FF ./awox_mesh_light_single_webthing.py

   curl http://localhost:8888/properties
   #| {"on": true, "brightness": 50, "color": "#ffffff"}

   curl -X PUT --data '{"color": "#00A000"}' \
     -H 'Content-Type: "application/json" ' \
     "http://localhost:8888/properties/color"


DEVELOP
=======

On WebThings Gateway, adapter can be run from shell using:

::
   
   sudo hcitool lescan
   #| LE Scan ...
   #| A4:C1:38:ff:ff:ff unpaired
   #| A4:C1:38:ff:ff:ff (unknown)

   pip3 install --user -r requirements.txt
   MAC=A4:C1:38:ff:ff:ff ./main.py


RESOURCES
=========

* https://github.com/Leiaz/python-awox-mesh-light
* https://iot.mozilla.org
* https://www.amazon.fr/dp/B01L3C1V5G/rzr-21
* https://www.awox.com/en/awox_product/smartlight-mesh-c9/
* https://www.upcitemdb.com/upc/3760118941004
* https://en.wikipedia.org/wiki/Bluetooth_mesh_networking
* https://purl.org/rzr/presentations
* https://libregraphicsmeeting.org/2020/en/program.html
* https://github.com/WebThingsIO/addon-list/pull/851
* https://libraries.io/pypi/webthing
* https://github.com/WebThingsIO/wiki/wiki/HOWTO:-Create-an-add-on
  
.. |GitHub| image:: https://img.shields.io/github/forks/rzr/awox-mesh-light-webthing.svg?style=social&label=Fork&maxAge=2592000
   :target: https://GitHub.com/rzr/awox-mesh-light-webthing/network/
.. |License| image:: https://img.shields.io/badge/License-MIT-blue.svg
   :target: https://github.com/rzr/awox-mesh-light-webthing/blob/master/LICENSE
.. |PyPI| image:: https://img.shields.io/pypi/v/awox-mesh-light-webthing.svg
   :target: https://pypi.org/project/awox-mesh-light-webthing
.. |Fediverse| image:: https://img.shields.io/mastodon/follow/279303?domain=https%3A%2F%2Fmastodon.social&style=social
   :target: https://mastodon.social/@rzr/104246455002891688
