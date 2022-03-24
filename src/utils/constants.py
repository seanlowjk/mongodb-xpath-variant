from enum import Enum


class Axes(Enum):
    # Forward axes
    CHILD = "child"
    DESCENDANT = "descendant"
    ATTRIBUTE = "attribute"
    SELF = "self"
    DESCENDANT_OR_SELF = "descendant-or-self"
    FOLLOWING_SIBLING = "following-sibling"
    FOLLOWING = "following"
    NAMESPACE = "namespace"
    # Reverse axes
    PARENT = "parent"
    ANCESTOR = "ancestor"
    PRECEDING_SIBLING = "preceding-sibling"
    PRECEDING = "preceding"
    ANCESTOR_OR_SELF = "ancestor-or-self"


STEP_STARTER = "/"
STEP_SEPERATOR = "::"
XPATH_AXES = [axes.value for axes in Axes]
