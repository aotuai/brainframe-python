from typing import Optional, List, Dict, Any
import uuid

from .base_codecs import Codec
from .identity_codecs import Identity


class Detection(Codec):
    """An object detected in a video frame. Detections can have attributes
    attached to them that provide more information about the object as well as
    other metadata like a unique tracking ID.
    """

    def __init__(self, *, class_name, coords, children, attributes,
                 with_identity, extra_data, track_id):
        self.class_name: str = class_name
        """The class of object that was detected, like 'person' or 'car'"""
        self.coords: List[List[int]] = coords
        """The coordinates, in pixels, of the detection in the frame"""
        self.children: List[Detection] = children
        self.attributes: Dict[str, str] = attributes
        """A dict whose key is an attribute name and whose value is the value
        of that attribute. For example, a car detection may have an attribute
        whose key is 'type' and whose value is 'sedan'.
        """
        self.with_identity: Optional[Identity] = with_identity
        """If not None, this is the identity that this detection was recognized
        as.
        """
        self.extra_data: Dict[str, Any] = extra_data
        """Any additional metadata describing this object"""
        self.track_id: Optional[uuid.UUID] = track_id
        """If not None, this is a unique tracking ID for the object. This ID
        can be compared to detections from other frames to track the movement
        of an object over time.
        """

    @property
    def center(self):
        """Return the center of the detections coordinates"""
        x = [c[0] for c in self.coords]
        y = [c[1] for c in self.coords]
        return sum(x) / len(x), sum(y) / len(y)

    @property
    def bbox(self):
        sorted_x = sorted([c[0] for c in self.coords])
        sorted_y = sorted([c[1] for c in self.coords])
        return [[sorted_x[0], sorted_y[0]],
                [sorted_x[-1], sorted_y[0]],
                [sorted_x[-1], sorted_y[-1]],
                [sorted_x[0], sorted_y[-1]]]

    def to_dict(self):
        d = dict(self.__dict__)
        if self.with_identity:
            d["with_identity"] = Identity.to_dict(d["with_identity"])
        if self.track_id:
            d["track_id"] = str(self.track_id)

        d["children"] = [Detection.to_dict(det) for det in self.children]
        return d

    @staticmethod
    def from_dict(d):
        with_identity = None
        if d["with_identity"]:
            with_identity = Identity.from_dict(d["with_identity"])

        track_id = None
        if d["track_id"]:
            track_id = uuid.UUID(d["track_id"])

        children = [Detection.from_dict(det) for det in d["children"]]
        return Detection(class_name=d["class_name"],
                         coords=d["coords"],
                         children=children,
                         attributes=d["attributes"],
                         with_identity=with_identity,
                         extra_data=d["extra_data"],
                         track_id=track_id)


class Attribute(Codec):
    """This holds an attribute of a detection. These should _not_ be made
    on the client side
    """

    def __init__(self, *, category=None, value=None):
        self.category = category
        """The category of attribute being described"""
        self.value = value
        """The value for this attribute category"""

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(d):
        return Attribute(category=d["category"],
                         value=d["value"])
