from typing import Dict, List
from enum import Enum

from .base_codecs import Codec


class OptionType(Enum):
    """The data type of a plugin option"""

    FLOAT = "float"
    INT = "int"
    ENUM = "enum"
    BOOL = "bool"

    @classmethod
    def values(cls):
        return [v.value for v in cls]


class PluginOption(Codec):
    """A single configuration option for a plugin. Defines what type of option
    it is and its potential values.

    There are two kinds of plugin options. Stream plugin options apply only to
    the stream they are attached to. Global plugin options apply to all
    streams, but are overridden by stream plugin options.
    """

    def __init__(self, *, type_, default, constraints, description):
        self.type = type_
        self.default = default
        self.constraints = constraints
        self.description = description

    def to_dict(self):
        d = dict(self.__dict__)
        d["type"] = self.type.value
        return d

    @staticmethod
    def from_dict(d):
        type_ = OptionType(d["type"])
        return PluginOption(type_=type_,
                            default=d["default"],
                            constraints=d["constraints"],
                            description=d["description"])


class SizeType(Enum):
    """Describes the amount of DetectionNodes a plugin takes as input or
    provides as output.
    """

    NONE = "none"
    """Input: The plugin takes nothing as input, like for an object detector.
    
    Output: Plugins cannot have a NONE output.
    """
    SINGLE = "single"
    """Input: The plugin takes a single DetectionNode as input, like for a
    classifier.
    
    Output: The plugin provides a single modified DetectionNode as output, like
    for a classifier.
    """
    ALL = "all"
    """Input: The plugin takes all instances of a class as input, like for a
    tracker.
    
    Output: The plugin provides all instances of a class as output, like for a
    detector.
    """

    @classmethod
    def values(cls):
        return [v.value for v in cls]


class NodeDescription(Codec):
    """A description of a DetectionNode, used by plugins to define what kinds
    of inputs and outputs a plugin uses.
    """

    def __init__(self, *,
                 size: SizeType,
                 detections: List[str],
                 attributes: Dict[str, List[str]],
                 encoded: bool,
                 tracked: bool,
                 extra_data: List[str]):
        self.size: SizeType = size
        """Describes the amount of DetectionNodes the node either takes in as
        input or provides as output
        """
        self.detections = detections
        """A list of detection class names, like “person” or “vehicle”. A
        DetectionNode that meets this description must have a class name that
        is present in this list.
        """
        self.attributes = attributes
        """Key-value pairs whose key is the classification type and whose value
        is a list of possible attributes. A DetectionNode that meets this
        description must have a classification for each classification type
        listed here.
        """
        self.encoded = encoded
        """If true, the DetectionNode must be encoded to meet this description
        """
        self.tracked = tracked
        """If true, the DetectionNode must be tracked to meet this description
        """
        self.extra_data = extra_data
        """A list of keys in a NodeDescription's extra_data. A DetectionNode
        that meets this description must have extra data for each name listed
        here.
        """

    def to_dict(self):
        d = dict(self.__dict__)
        d["size"] = self.size.value
        return d

    @staticmethod
    def from_dict(d):
        size = NodeDescription.SizeType(d["size"])
        return NodeDescription(
            size=size,
            detections=d["detections"],
            attributes=d["attributes"],
            encoded=d["encoded"],
            tracked=d["tracked"],
            extra_data=d["extra_data"])


class Plugin(Codec):
    """Metadata on a loaded plugin."""
    def __init__(self, *,
                 name: str,
                 version: int,
                 description: str,
                 input_type: NodeDescription,
                 output_type: NodeDescription,
                 capability: NodeDescription,
                 options: Dict[str, PluginOption]):
        self.name = name
        """The name of the plugin"""
        self.version = version
        """The plugin's version"""
        self.description = description
        """A human-readable description of what the plugin does"""
        self.input_type = input_type
        """Describes the type of inference data that this plugin takes as input
        """
        self.output_type = output_type
        """Describes the type of inference data that this plugin produces"""
        self.capability = capability
        """A NodeDescription which describes what this plugin does to its
        input. It is the difference between the input and output
        NodeDescriptions. This field is useful for inspecting a plugin to find
        what it can do.
        """
        self.options = options
        """A dict describing the configurable options of this plugin"""

    def to_dict(self):
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "input_type": self.input_type.to_dict(),
            "output_type": self.output_type.to_dict(),
            "capability": self.capability.to_dict(),
            "options": {key: val.to_dict()
                        for key, val in self.options.items()},
        }

    @staticmethod
    def from_dict(d):
        return Plugin(
            name=d["name"],
            version=d["version"],
            description=d["description"],
            input_type=NodeDescription.from_dict(d["input_type"]),
            output_type=NodeDescription.from_dict(d["output_type"]),
            capability=NodeDescription.from_dict(d["capability"]),
            options={key: PluginOption.from_dict(val)
                     for key, val in d["options"].items()},
        )
