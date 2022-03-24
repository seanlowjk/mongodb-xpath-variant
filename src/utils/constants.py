from enum import Enum


# Axes Related 
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

# Path Related 
STEP_STARTER = "/"
STEP_SEPERATOR = "::"
XPATH_AXES = [axes.value for axes in Axes]

# Predicate Related 
class Predicate(Enum):
    LEFT_BRACKET = "["
    RIGHT_BRACKET = "]"
    LEFT_PARANTHESIS = "("
    RIGHT_PARANTHESIS = ")"
