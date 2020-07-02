from enum import Enum
from typing import Dict, List, Any

from dataclasses import dataclass

from .base_codecs import Codec


@dataclass
class CapsuleOption(Codec):
    """A single configuration option for a capsule. Defines what type of option
    it is and its potential values.

    There are two kinds of capsule options. Stream capsule options apply only
    to the stream they are attached to. Global capsule options apply to all
    streams, but are overridden by stream capsule options.
    """

    class Type(Enum):
        """The data type of a capsule option"""

        FLOAT = "float"
        INT = "int"
        ENUM = "enum"
        BOOL = "bool"

        @classmethod
        def values(cls):
            return [v.value for v in cls]

    type: Type
    """The data type of this option's value"""

    default: Any
    """The default value for this option"""

    constraints: dict
    """Describes the range of valid values for this option. The content of
    this dict depends on the type field.
    
    OptionType.FLOAT:
        ``max_val``: The maximum valid float value
        
        ``min_val``: The minimum valid float value
    
    OptionType.INT:
        ``max_val``: The maximum valid int value
        
        ``min_val``: The minimum valid int value
    
    OptionType.ENUM:
        ``choices``: A list of strings. The option's value must be one of
        these strings.
    
    OptionType.BOOL:
        This object has no constraints.
    """

    description: str
    """A human-readable description of the capsule's capabilities"""

    def to_dict(self):
        d = dict(self.__dict__)
        d["type"] = self.type.value
        return d

    @staticmethod
    def from_dict(d):
        type_ = CapsuleOption.Type(d["type"])
        return CapsuleOption(type=type_,
                             default=d["default"],
                             constraints=d["constraints"],
                             description=d["description"])


@dataclass
class NodeDescription(Codec):
    """A description of a DetectionNode, used by capsules to define what kinds
    of inputs and outputs a capsule uses.
    """

    class Size(Enum):
        """Describes the amount of DetectionNodes a capsule takes as input or
        provides as output.
        """

        NONE = "none"
        """Input: The capsule takes nothing as input, like for an object
        detector.

        Output: Capsules cannot have a NONE output.
        """
        SINGLE = "single"
        """Input: The capsule takes a single DetectionNode as input, like for a
        classifier.

        Output: The capsule provides a single modified DetectionNode as output,
        like for a classifier.
        """
        ALL = "all"
        """Input: The capsule takes all instances of a class as input, like for
        a tracker.

        Output: The capsule provides all instances of a class as output, like
        for a detector.
        """

        @classmethod
        def values(cls):
            return [v.value for v in cls]

    size: Size
    """Describes the amount of DetectionNodes the node either takes in as
    input or provides as output
    """

    detections: List[str]
    """A list of detection class names, like “person” or “vehicle”. A
    DetectionNode that meets this description must have a class name that
    is present in this list.
    """

    attributes: Dict[str, List[str]]
    """Key-value pairs whose key is the classification type and whose value
    is a list of possible attributes. A DetectionNode that meets this
    description must have a classification for each classification type
    listed here.
    """

    encoded: bool
    """If True, the DetectionNode must be encoded to meet this description
    """

    tracked: bool
    """If True, the DetectionNode must be tracked to meet this description
    """

    extra_data: List[str]
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
        size = NodeDescription.Size(d["size"])
        return NodeDescription(
            size=size,
            detections=d["detections"],
            attributes=d["attributes"],
            encoded=d["encoded"],
            tracked=d["tracked"],
            extra_data=d["extra_data"])


@dataclass
class Capsule(Codec):
    """Metadata on a loaded capsule."""

    name: str
    """The name of the capsule"""

    version: int
    """The capsule's version"""

    description: str
    """A human-readable description of what the capsule does"""

    input_type: NodeDescription
    """Describes the type of inference data that this capsule takes as input
    """

    output_type: NodeDescription
    """Describes the type of inference data that this capsule produces"""

    capability: NodeDescription
    """A NodeDescription which describes what this capsule does to its
    input. It is the difference between the input and output
    NodeDescriptions. This field is useful for inspecting a capsule to find
    what it can do.
    """

    options: Dict[str, CapsuleOption]
    """A dict describing the configurable options of this capsule"""

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
        return Capsule(
            name=d["name"],
            version=d["version"],
            description=d["description"],
            input_type=NodeDescription.from_dict(d["input_type"]),
            output_type=NodeDescription.from_dict(d["output_type"]),
            capability=NodeDescription.from_dict(d["capability"]),
            options={key: CapsuleOption.from_dict(val)
                     for key, val in d["options"].items()},
        )
