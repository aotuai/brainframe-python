from typing import Dict, List
from enum import Enum

from .base_codecs import Codec


class OptionType(Enum):
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
    OptionType = OptionType

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
        type_ = PluginOption.OptionType(d["type"])
        return PluginOption(type_=type_,
                            default=d["default"],
                            constraints=d["constraints"],
                            description=d["description"])


class SizeType(Enum):
    NONE = "none"
    SINGLE = "single"
    ALL = "all"

    @classmethod
    def values(cls):
        return [v.value for v in cls]


class NodeDescription(Codec):
    """A description of a DetectionNode, used by plugins to define what kinds
    of inputs and outputs a plugin uses.
    """
    SizeType = SizeType

    def __init__(self, *,
                 size: SizeType,
                 detections: List[str],
                 attributes: Dict[str, List[str]],
                 encoded: bool,
                 tracked: bool,
                 extra_data: List[str]):
        self.size = size
        self.detections = detections
        self.attributes = attributes
        self.encoded = encoded
        self.tracked = tracked
        self.extra_data = extra_data

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
        self.version = version
        self.description = description
        self.input_type = input_type
        self.output_type = output_type
        self.capability = capability
        self.options = options

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
