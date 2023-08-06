# json-settings 

json-settings is a Python framework for JSON configuration file handling. It
provides the following features

- Define a nested Python class structure that mirrors the desired configuration
  file. 
- Automatic type checking. 
- Implicit recursive error messaging that provides human readable information on
  the location and nature of an error in a configuration file.
- Easy and adaptable value bounding validation.
- Array and range support for numerical values.
- Ability to convert a setting object with range values into a multidimensional
  array of the settings object with singular values for each setting.

# Contents
- [json-settings](#json-settings)
- [Contents](#contents)
- [Installation](#installation)
- [Getting Started](#getting-started)
  - [Primitive-Types](#primitive-types)
  - [Reference-Types](#reference-types)
  - [Null-Types](#null-types)
  - [Terminus-Setting](#terminus-setting)
  - [Setting-Error-Messages](#setting-error-messages)
  - [Number-Settings](#number-settings)
    - [Spaces](#spaces)
    - [Range-Matching](#range-matching)
  - [String-Set-Settings](#string-set-settings)
  - [List-Settings](#list-settings)
  - [Dictionary-Settings](#dictionary-settings)


# Installation 

Install the json-settings package with the command `pip install json_settings`.

# Getting Started

## Primitive-Types

We would like to create a simple configuration file, my_json_config_file.json,
with a single setting that is an integer. The JSON file will look like this:

```json
{
    "my_integer": 1
}
```

So we use the basic unit of json_settings, the `Settings` base class, to define
a new `Settings` derived class
```python
import json

from json_settings import Settings

class MyCoolSetting(Settings):

    @Settings.assign
    def __init__(self, value: dict):
        self.my_integer = int

if __name__ == "__main__":

    with open("my_json_config_file.json", 'r') as f:
        values = json.loads(f.read())

    my_cool_setting = MyCoolSetting(values)

    print(my_cool_setting.my_integer)
    print(type(my_cool_setting.my_integer))
```

If we run the Python above the output will be
```
1
<class `int`>
```
A few things to note:

- All user defined settings classes must call their base class' `assign`
decorator on the `__init__` method.
- All user define settings class' `__init__` method take a single argument (in
  addition to `self`).
- All settings defined in the `__init__` method must be equal to their required type.
- Any variables defined in the `__init__` method will be enforced at runtime.
- JSON entries cannot contain hyphens in their id string.

## Reference-Types

We now want to have a settings file that is more complex. The configuration file
will look like this:

```json
{
    "footware": {
        "type": "formal",
        "quantity": 2
    },
    "gloves": true
}
```

The corresponding Python class structure is as follows:
```python
import json

from json_settings import Settings

class FootwareSettings(Settings):

    @Settings.assign
    def __init__(self, values):
        self.type = str
        self.quantity = int


class MyCoolSetting(Settings):

    @Settings.assign
    def __init__(self, value: dict):
        self.footware = FootwareSettings 
        self.gloves = bool

if __name__ == "__main__":

    with open("my_json_config_file.json", 'r') as f:
        values = json.loads(f.read())

    my_cool_setting = MyCoolSetting(values)

    print(my_cool_setting.footware.type)
    print(my_cool_setting.footware.quantity)
    print(my_cool_setting.gloves)
```

If we run the Python above the output will be
```
formal
2
True
```

This nesting can be of an arbitrary depth, and all error handling is automatic
and recursive, allowing for easy construction of complex configuration files.

## Null-Types

The standard json package converts `null` values to `None` type values. By
default `Settings` derived classes will assign `None` regardless of the required
type. This can be restricted by using a `TerminusSetting` derived type.

## Terminus-Setting

Sometimes we need to define a setting which has more rigorous constraints. To do
this we define a `TerminusSetting` derived class.

We want to define a setting that is the name of a king, however we require that
it starts with "king_".

```json
{
    "my_king": "king_james"
}
```

The corresponding Python class structure is as follows:
```python
import json

from json_settings import TerminusSetting
from json_settings import Settings 

class MyCoolSetting(Settings):

    @Settings.assign
    def __init__(self):
        self.my_king = KinglyName


class KinglyName(TerminusSetting):

    @TerminusSetting.assign
    def __init__(self, value: dict):
        self.type = str
    
    def check(self):
        if not self.value.startswith("king_"):
            raise ValueError('Name must start with "king_"')

if __name__ == "__main__":

    with open("my_json_config_file.json", 'r') as f:
        values = json.loads(f.read())

    my_kingly_setting = MyCoolSetting(values)

    print(my_kingly_setting.my_king)
```

If we run the Python above the output will be
```
king_james
```

A few things to note:

- TerminusSetting derived classes must define only one attribute `type` in the
  `__init__` method, which is the type of the variable stored.
- The abstract `check` method must be defined for all TerminusSetting derived
  classes.
- The check method will catch `ValueError` and `TypeError` and raise
  `SettingCheckError`, which in turn is caught by the enclosing `Settings`
  derived instance and raised as a `SettingErrorMessage`.
- The value of the setting in a `TerminusSetting` derived class is stored in the
  `value` attribute.
- When an attribute of a `Settings` object which is a `TerminusSetting` derived
  type is accessed, the value stored in the `TerminusSetting` derived instances
  is returned, NOT the `TerminusSettings` derived instance itself.

## Setting-Error-Messages

One of the key features of json_settings is the recursive exception handling. To
demonstrate we define the following configuration file and corresponding Python
class structure

```json
{
    "first": {
        "second": {
            "fourth": 1,
            "fith": "fith"
        },
        "third": false
    }
}
```

```python
import sys
import json

from json_settings import Settings
from json_settings import TerminusSetting
from json_settings import SettingErrorMessage

class MainSettings(Settings):
    @Settings.assign
    def __init__(self, values):
        self.first = SecondSettings


class SecondSettings(Settings):
    @Settings.assign
    def __init__(self, values):
        self.second = FinalSettings
        self.third = bool


class FinalSettings(Settings):
    @Settings.assign
    def __init__(self, values):
        self.fourth = int
        self.fith = FithSetting


class FithSetting(TerminusSetting):
    @TerminusSetting.assign
    def __init__(self, value):
        self.type = str

    def check(self):
        if "f" not in self.value:
            raise ValueError('Must contain the letter "f"')


if __name__ == "__main__":

    with open("my_json_config_file.json", 'r') as f:
        values = json.loads(f.read())

    try:
        my_cool_settings= MainSettings(values)
    except SettingErrorMessage as e:
        sys.exit(e)
```

Instead of running the above code with the correct JSON configuration file, we
will use the following, which contains an error

```json
{
    "first": {
        "second": {
            "fourth": 1,
            "fith": "badger"
        },
        "third": false
    }
}
```

Running the above code will yield the following output
```
first -> second -> fith -> Must contain the letter "f"
```

If we have an error in a different setting like so

```json
{
    "first": {
        "second": {
            "fourth": 1,
            "fith": "fith"
        },
        "third": 1
    }
}
```

we get the following error message
```
first -> third -> Expecting : <class 'bool'> | Received: <class 'int'>
```

In each case the location and nature of the error in the configuration file is
indicated in the error message yielded to the user.

## Number-Settings

json_settings provides a special base class for numerical settings.
`NumberSettings` is itself derived from `TerminusSetting`, but with some extra
functionality.

Imagine we wish to create a settings object with a `float` setting, that must be
greater than or equal to zero:

```json
{
    "important_number": 1.0
}

```

```python
import sys
import json

from json_settings import Settings
from json_settings import NumberSetting 
from json_settings import SettingErrorMessage


class MainSettings(Settings):

    @Settings.assign
    def __init__(self, values):
        self.important_number = ImportantNumberSetting


class ImportantNumberSetting(NumberSetting):
    @NumberSetting.assign
    def __init__(self, value):
        self.type = float

    def check(self):
        self.lower_bound(0.0)

if __name__ == "__main__":

    with open("my_json_config_file.json", 'r') as f:
        values = json.loads(f.read())

    try:
        my_cool_settings = MainSettings(values)
    except SettingErrorMessage as e:
        sys.exit(e)
    
    print(f"Important Number is: {my_cool_settings.important_number})
```

Notes:

- `NumberSetting` comes with several inbuild check methods for enforcing
  numberical bounds
  - `lower_bound`
  - `upper_bound`
  - `lower_bound_exclusive`
  - `upper_bound_exclusive`

Running the above code will return
```
Important Number is: 1.0
```

However `NumberSetting` derived settings objects also accept array and range
definitions. For example, if we use the following configuration file

```json
{
    "important_number": {
        "array": [1.0, 2.0, 3.0]
    } 
}
```

we get the following output
```
Important Number is: [1.0, 2.0, 3.0]
```

We also note that if one of entries in the array does not satisfy the range
condition we get the following output

```
important_number -> must be >= 0.
```

We can also define a set of values in the following way

```json
{
    "important_number": {
        "min": 0.0,
        "max": 5.0,
        "num": 6
    }
}

```

which gives the following output

```
Important Number is: [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
```

where we can see a linear space has been created over the defined range.

Errors in the range definition are caught and yielded to the user such as

```
important_number -> No 'min' parameter provided for range
```

Note:

- The order of the range or array does not matter.

### Spaces

Consider a situation where we have some `NumberSetting` settings in our
configuration file

```json
{
    "primary_number": {
        "array": [1.0, 2.0, 3.0]
    },
    "secondary_number": {
        "min": 4.0,
        "max": 6.0,
        "num": 3
    }
}
```

```python
import sys
import json

from json_settings import Settings
from json_settings import NumberSetting 
from json_settings import SettingErrorMessage


class MainSettings(Settings):

    @Settings.assign
    def __init__(self, values):
        self.primary_number = ImportantNumberSetting
        self.secondary_number = ImportantNumberSetting


class ImportantNumberSetting(NumberSetting):
    @NumberSetting.assign
    def __init__(self, value):
        self.type = float

    def check(self):
        self.lower_bound(0.0)

if __name__ == "__main__":

    with open("my_json_config_file.json", 'r') as f:
        values = json.loads(f.read())

    try:
        my_cool_settings = MainSettings(values)
    except SettingErrorMessage as e:
        sys.exit(e)
    
    print(f"Primary Number: {my_cool_settings.primary_number}")
    print(f"Secondary Number: {my_cool_settings.secondary_number}")
```

Running the above will output the following, indicating that the two arrays are
stored

```
Primary Number: [1.0, 2.0, 3.0]
Secondary Number: [4.0, 5.0, 6.0]
```

However what if we want to generate a set of `MainSettings` instances, each one
representing a single point in combined cartesian product space of
`primary_number` and `secondary_number`. We can do so using the `Space` class.

```python
import sys
import json

from json_settings import Settings
from json_settings import NumberSetting 
from json_settings import SettingErrorMessage
from json_settings import Space 


class MainSettings(Settings):

    @Settings.assign
    def __init__(self, values):
        self.primary_number = ImportantNumberSetting
        self.secondary_number = ImportantNumberSetting


class ImportantNumberSetting(NumberSetting):
    @NumberSetting.assign
    def __init__(self, value):
        self.type = float

    def check(self):
        self.lower_bound(0.0)

if __name__ == "__main__":

    with open("my_json_config_file.json", 'r') as f:
        values = json.loads(f.read())

    try:
        my_cool_settings = MainSettings(values)
    except SettingErrorMessage as e:
        sys.exit(e)
    
    settings_space = Space(my_cool_settings)
    
    print(f"Primary Number[0, 0]: {settings_space[0, 0].primary_number}")
    print(f"Secondary Number[0, 0]: {settings_space[0, 0].secondary_number}")
    print(f"Type of [0, 0] element: {settings_space[0, 0]}")
    print(f"Primary Number[0, 1]: {settings_space[0, 1].primary_number}")
    print(f"Secondary Number[0, 1]: {settings_space[0, 1].secondary_number}")
    print(f"Primary Number[2, 2]: {settings_space[2, 2].primary_number}")
    print(f"Secondary Number[2, 2]: {settings_space[2, 2].secondary_number}")
    print(f"Space dimensions: {settings_space.shape}")
    print(f"Space summary: {settings_space.cout_summary()}")
    print(f"Total number of elements: {len(settings_space)}")
```

The above will output

```
Primary Number[0, 0]: 1.0
Secondary Number[0, 0]: 4.0
Type of [0, 0] element: <__main__.MainSettings object at 0x000001BF79B40F10>
Primary Number[0, 1]: 1.0
Secondary Number[0, 1]: 5.0
Primary Number[2, 2]: 3.0
Secondary Number[2, 2]: 6.0
Space dimensions: (3, 3)
Space summary: Computational space dimensions: 3 x 3

axis: 0:
        primary_number
        values:  [1.0, 2.0, 3.0]
axis: 1:
        secondary_number
        values:  [4.0, 5.0, 6.0]

Total number of elements: 9
```

The `Space` instances behaves as a multidimensional `numpy` array.

A few things to note:

- You can define an arbitrary number of ranged parameters. The resultant `Space`
  instance will have the corresponding number of dimensions.
- You can restrict the space range expansion to a particular subset of the
  available settings by passing the optional `restrict` parameter to the `Space`
  constructor
  - restrict : `dict`[`str`, `str`]
            A dictionary of `str`: `str` pairs that are used to exclude
            subsetting branches from the exploration function for finding ranges.
            If when searching the settings object for ranges, a setting with the
            same name as a key in `restrict` is found, only subsettings with
            name equal to the corresponding value will be searched.

### Range-Matching

Sometimes we might have several ranges, however we want to couple some of them
together such that the resulting `Space` instance is of reduced dimension.

```json
{
    "primary_number": {
        "array": [1.0, 2.0, 3.0]
    },
    "secondary_number": {
        "min": 4.0,
        "max": 6.0,
        "num": 3
    },
    "tertiary_number": {
        "array": [-1.0, -2.0, -3.0]
    }
}
```

```python
import sys
import json

from json_settings import Settings
from json_settings import NumberSetting 
from json_settings import SettingErrorMessage
from json_settings import Space 


class MainSettings(Settings):

    @Settings.assign
    def __init__(self, values):
        self.primary_number = ImportantNumberSetting
        self.secondary_number = ImportantNumberSetting
        self.tertiary_number = MinorNumberSetting


class ImportantNumberSetting(NumberSetting):
    @NumberSetting.assign
    def __init__(self, value):
        self.type = float

    def check(self):
        self.lower_bound(0.0)


class MinorNumberSetting(NumberSetting):
    @NumberSetting.assign
    def __init__(self, value):
        self.type = float

    def check(self):
        pass

if __name__ == "__main__":

    with open("my_json_config_file.json", 'r') as f:
        values = json.loads(f.read())

    try:
        my_cool_settings = MainSettings(values)
    except SettingErrorMessage as e:
        sys.exit(e)
    
    settings_space = Space(my_cool_settings)
    
    print(f"Space dimensions: {settings_space.shape}")
    print(f"Space summary: {settings_space.cout_summary()}")
    print(f"Total number of elements: {len(settings_space)}")
```

This will result in the following output
```
Space dimensions: (3, 3, 3)
Space summary: Computational space dimensions: 3 x 3 x 3

axis: 0:
        primary_number
        values:  [1.0, 2.0, 3.0]
axis: 1:
        secondary_number
        values:  [4.0, 5.0, 6.0]
axis: 2:
        tertiary_number
        values:  [-1.0, -2.0, -3.0]

Total number of elements: 27
```

We can couple two of the ranges together, such that the resultant space iterates
through matched parameters in step. Using the following JSON file
```json
{
    "primary_number": {
        "array": [1.0, 2.0, 3.0],
        "match": "best_match"
    },
    "secondary_number": {
        "min": 4.0,
        "max": 6.0,
        "num": 3,
    },
    "tertiary_number": {
        "array": [-1.0, -2.0, -3.0],
        "match": "best_match"
    }
}
```
the resultant output is
```
Space dimensions: (3, 3)
Space summary: Computational space dimensions: 3 x 3

axis: 0:
        secondary_number
        values:  [4.0, 5.0, 6.0]

axis: 1:
        match_id: best_match
        primary_number
        tertiary_number
        values: [(1.0, -1.0), (2.0, -2.0), (3.0, -3.0)]
Total number of elements: 9
```

We can see that `primary_number` and `tertiary_number are coupled in order along
one axis.

A few things to note:

- You can match an arbitary number of ranges together at different and arbitrary
  depth.
- You can use any match string, and two ranges with the same match string will
  be coupled.
- You can define an arbitrary number of match strings.

## String-Set-Settings

A common type of setting is a restricted set of string values. As such
`json_settings` has a special base class `StringSetSetting`. For example, we
might want to define a setting that is a type of vehicle

```json
{
    "vehicle_type": "car"
}
```
```python
import sys
import json

from json_settings import Settings
from json_settings import StringSetSetting
from json_settings import SettingErrorMessage


class MainSettings(Settings):

    @Settings.assign
    def __init__(self, values):
        self.vehicle_type = VehicleTypeSetting


class VehicleTypeSetting(StringSetSetting):
    @StringSetSetting.assign
    def __init__(self, value):
        self.options = [
            "car",
            "plane",
            "boat"
        ]

if __name__ == "__main__":

    with open("my_json_config_file.json", 'r') as f:
        values = json.loads(f.read())

    try:
        my_cool_settings = MainSettings(values)
    except SettingErrorMessage as e:
        sys.exit(e)
    
```

A few things to note:

- `StringSetSetting` derived classes must have only one attribute `options`
  defined in the `__init__` method. `options` must be a `list` of `str` values.

If a value that is not in the defined list is passed in the JSON file, the
following error message is yielded to the user

```
vehicle_type -> must be one of ['car', 'plane', 'boat']
```

## List-Settings

We want to define a setting that is a list of a single arbitrary type

```json
{
    "entries": [
        {
            "kind": "car",
            "cost": 1000
        },
        {
            "kind": "car",
            "cost": 3000
        },
        {
            "kind": "plane",
            "cost": 10000 
        }
    ]
}
```
```python
import sys
import json

from json_settings import Settings
from json_settings import ListSetting
from json_settings import StringSetSetting
from json_settings import SettingErrorMessage


class MainSettings(Settings):

    @Settings.assign
    def __init__(self, values):
        self.entries = EntryListSetting 

class EntryListSetting(ListSetting):
    @ListSetting.assign
    def __init__(self, values):
        self.type = EntrySetting

class EntrySetting(Settings):
    @Settings.assign
    def __init__(self, values):
        self.kind = VehicleTypeSetting
        self.cost = int

class VehicleTypeSetting(StringSetSetting):
    @StringSetSetting.assign
    def __init__(self, value):
        self.options = [
            "car",
            "plane",
            "boat"
        ]

if __name__ == "__main__":

    with open("my_json_config_file.json", 'r') as f:
        values = json.loads(f.read())

    try:
        my_cool_settings = MainSettings(values)
    except SettingErrorMessage as e:
        sys.exit(e)
    
    print(f"Element type: {type(my_cool_settings[0])}")
    print(f"First element.kind: {my_cool_settings.entries[0].kind}")
    print(f"First element.cost: {my_cool_settings.entries[0].cost}")
    print(f"Third element.kind: {my_cool_settings.entries[2].kind}")
    print(f"Third element.cost: {my_cool_settings.entries[2].cost}")
    
```

The above code will result in the following output

```
Element type: <class '__main__.EntrySetting'>
First element.kind: car
First element.cost: 1000
Third element.kind: plane
Third element.cost: 10000
```

If we introduce an error in the configuration file
```json
{
    "entries": [
        {
            "kind": "caravan",
            "cost": 1000
        },
        {
            "kind": "car",
            "cost": 3000
        },
        {
            "kind": "plane",
            "cost": 10000 
        }
    ]
}
```

The following error message will be yielded to the user, noting the element of
the list where the error occurred
```
entries[0] -> kind -> must be one of ['car', 'plane', 'boat']
```

A few things to note:

- `ListSettings` derived classes must define only one attribute `type` in the
  `__init__` method, which is the type of the values stored.
- A list can contain an arbitrary number of elements.
- All elements of the list must adhere to the constrants of all sub elements of
  any settings objects contain within it.
- Any `ListSetting` derived object behaves like an immutable `list`.
- List order from configuration files is maintained.

## Dictionary-Settings

We want to define a setting that is a dictionary where all values are of a
single arbitrary type 

```json
{
    "entries": {
        "cheap_car": {
            "kind": "car",
            "cost": 1000
        },
        "expensive_car": {
            "kind": "car",
            "cost": 3000
        },
        "cheap_plane": {
            "kind": "plane",
            "cost": 10000 
        }
    }
}
```
```python
import sys
import json

from json_settings import Settings
from json_settings import DictionarySetting 
from json_settings import StringSetSetting
from json_settings import SettingErrorMessage


class MainSettings(Settings):

    @Settings.assign
    def __init__(self, values):
        self.entries = EntryListSetting 

class EntryListSetting(DictionarySetting):
    @DictionarySetting.assign
    def __init__(self, values):
        self.type = EntrySetting

class EntrySetting(Settings):
    @Settings.assign
    def __init__(self, values):
        self.kind = VehicleTypeSetting
        self.cost = int

class VehicleTypeSetting(StringSetSetting):
    @StringSetSetting.assign
    def __init__(self, value):
        self.options = [
            "car",
            "plane",
            "boat"
        ]

if __name__ == "__main__":

    with open("my_json_config_file.json", 'r') as f:
        values = json.loads(f.read())

    try:
        my_cool_settings = MainSettings(values)
    except SettingErrorMessage as e:
        sys.exit(e)

    print(f"Element type: {type(my_cool_settings['cheap_car'])}")
    print(f"First element.kind: {my_cool_settings.entries['cheap_car'].kind}")
    print(f"First element.cost: {my_cool_settings.entries['cheap_car'].cost}")
    print(f"Third element.kind: {my_cool_settings.entries['cheap_plane'].kind}")
    print(f"Third element.cost: {my_cool_settings.entries['cheap_plane'].cost}")
```

The above code will result in the following output

```
Element type: <class '__main__.EntrySetting'>
First element.kind: car
First element.cost: 1000
Third element.kind: plane
Third element.cost: 10000
```

If we introduce an error in the configuration file
```json
{
    "entries": {
        "cheap_car": {
            "kind": "fish",
            "cost": 1000
        },
        "expensive_car": {
            "kind": "car",
            "cost": 3000
        },
        "cheap_plane": {
            "kind": "plane",
            "cost": 10000 
        }
    }
}
```

The following error message will be yielded to the user, noting the key of
the dictionary where the error occurred
```
entries -> cheap_car -> kind -> must be one of ['car', 'plane', 'boat']
```

A few things to note:

- `DictionarySettings` derived classes must define only one attribute `type` in the
  `__init__` method, which is the type of the values stored.
- A dictionary can contain an arbitrary number of key value pairs.
- All values of the dictionary must adhere to the constrants of all sub elements of
  any settings objects contain within it.
- Any `DictionarySetting` derived object behaves like an immutable `dict`.
- The key difference between this and a normal `Settings` derived object is the
  ability for the user to define arbitrary numbers of the same type of object to a
  configuration file.