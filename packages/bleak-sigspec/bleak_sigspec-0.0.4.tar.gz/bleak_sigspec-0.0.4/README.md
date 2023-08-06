## bleak_sigspec
### Bleak SIG Bluetooth Characteristic Specification Formatter

This package enables characteristic metadata parsing and automatic formatting (bytes unpacking) into the proper characteristic values.

To install

```
pip install bleak_sigspec
```

or to get the latest version

```
pip install https://github.com/Carglglz/bleak_sigspec.git
```

Compatibility with +200 GATT characteristics following [GATT Specifications](https://www.bluetooth.com/specifications/gatt/characteristics/)

### Usage example

`service_explorer.py` in bleak examples:

`char --> Temperature Characteristic`

```python
from bleak_sigspec.utils import get_char_value
[...]
37
			bytes_value = bytes(await client.read_gatt_char(char.uuid))
			formatted_value = get_char_value(bytes_value, char)
[...]
43
			log.info(
				"Characteristic Name: {0}, Bytes Value: {1}, Formatted
				Value: {2}".format(char.description, bytes_value, formatted_value))


```

```bash
$ python3 service_explorer.py
[...]
Characteristic Name: Temperature, Bytes Value: b'Z\x16', Formatted Value: {'Temperature': {'Quantity': 'thermodynamic temperature',
  'Unit': 'degree celsius',
  'Symbol': '°C',
  'Value': 57.22}}
```

### See characteristic metadata

```python
Python 3.7.6 (v3.7.6:43364a7ae0, Dec 18 2019, 14:18:50)
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from bleak_sigspec.utils import get_xml_char
>>> temp = get_xml_char('Temperature')
>>> temp
Characteristic Metadata:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    - NAME: Temperature
    - UUID: 2A6E
    - ABSTRACT: None
    - SUMMARY: None
    - FIELDS:
        - Temperature:
            - InformativeText: Unit is in degrees Celsius with a resolution of 0.01 degrees Celsius
            - Requirement: Mandatory
            - Format: sint16
            - Ctype: h
            - Unit_id: org.bluetooth.unit.thermodynamic_temperature.degree_celsius
            - Quantity: thermodynamic temperature
            - Unit: degree celsius
            - Symbol: °C
            - DecimalExponent: -2
    - TYPE: org.bluetooth.characteristic.temperature
    - INFO TEXT: Unit is in degrees Celsius with a resolution of 0.01 degrees Celsius
    - DESCRIPTION: None
    - NOTE: None
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

>>>

```


### Documentation

See the documentation at  [https://bleak-sigspec.readthedocs.io](https://bleak-sigspec.readthedocs.io)
