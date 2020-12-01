# visidata-plugins

## Installation

### Plugins

Installation involves the following:

* Copy the desired plugin `.py` file to the `~/.visidata/plugins/` directory
* Add `import plugins.<plugin name>` to the `__init__.py` file

**Example**

Copy the `pojobuddy.py` file to `~/.visidata/plugins/pojobuddy.py` and add the following to `~/.visidata/plugins/__init__.py`

```
import plugins.pojobuddy
```

## Usage

### pojobuddy

`pojobuddy` allows you to save `.pojo` files, which contain a
[Plain-old-Java-object](https://en.wikipedia.org/wiki/Plain_old_Java_object).
It is meant as a tool to either build a hierarchical structure in
VisiData and generate a boilerplate class from, or to allow the
eminently lazy to convert existing JSON directly to a boilerplate POJO

To do direct conversions between `JSON` and a POJO, just do a VisiData conversion with the following

```
vd some-data.json -b -o some-data.pojo
```

As an example, this will convert the following nonsensical `JSON`

```
{
    "name": "Polly Joel",
    "role": "extraordinaire",
    "nameParts": {
        "first": "Polly",
        "last": "Joel"
    },
    "one": 1,
    "onePointOne": 1.1,
    "friends": [
        { "name": "Alfred" },
        { "name": "Bruce" },
        { "name": "Cassandra" },
        { "name": "Dick" }
    ],
    "fishes": [
        "red",
        "blue"
    ]
}}
```

into the following nonsensical Java object, which can be modified
as necessary

```
class SomeData {
    private String name;
    private String role;
    private NameParts nameParts;
    private Integer one;
    private Double onePointOne;
    private List<Friend> friends;
    private List<String> fishes;
}
```

Currently this handles only one "level" of object, and although
it will make references to sub-objects class names, it will not
create the classes for these objects