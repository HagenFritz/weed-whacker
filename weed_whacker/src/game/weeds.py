"""
Weed type definitions and attributes
"""

import math

from dataclasses import dataclass


@dataclass
class Weed:
    """Represents a weed type with toughness and regrowth attributes"""
    
    name: str
    sprite_name: str
    toughness: float
    regrow: int
    
    def __post_init__(self):
        """Validate weed attributes"""
        if self.toughness <= 0:
            raise ValueError(f"Weed {self.name} toughness must be positive")
        if self.regrow < 0:
            raise ValueError(f"Weed {self.name} regrow must be non-negative")
    
    def chops_required(self, tool_efficiency: float) -> int:
        """Calculate number of chops required to destroy this weed with given tool
        
        Args:
            tool_efficiency: Tool's efficiency value (damage per chop)
            
        Returns:
            Number of chops needed to destroy the weed
        """
        return math.ceil(self.toughness / tool_efficiency)


WEED_BASIC = Weed(
    name="Basic Weed",
    sprite_name="weed_basic",
    toughness=1.0,
    regrow=3
)

WEEDS = {
    'weed_basic': WEED_BASIC
}


def get_weed(sprite_name: str) -> Weed:
    """Get weed by sprite name
    
    Args:
        sprite_name: Name of the weed sprite
        
    Returns:
        Weed instance
        
    Raises:
        KeyError: If weed not found
    """
    return WEEDS[sprite_name]
