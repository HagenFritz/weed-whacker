"""
Tool definitions and attributes
"""

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Tool:
    """Represents a tool with various attributes affecting gameplay"""
    
    name: str
    sprite_name: str
    efficiency: float
    cooldown: int
    longevity: int
    reach: List[Tuple[int, int]]
    cost: int
    
    def __post_init__(self):
        """Validate tool attributes"""
        if self.efficiency <= 0:
            raise ValueError(f"Tool {self.name} efficiency must be positive")
        if self.cooldown < 0:
            raise ValueError(f"Tool {self.name} cooldown must be non-negative")
        if self.longevity <= 0:
            raise ValueError(f"Tool {self.name} longevity must be positive")


HAND_HOE = Tool(
    name="Hand Hoe",
    sprite_name="hand_hoe",
    efficiency=1.0,
    cooldown=1000,
    longevity=100,
    reach=[(0, 0)],
    cost=0
)

SCYTHE = Tool(
    name="Scythe",
    sprite_name="scythe",
    efficiency=1.5,
    cooldown=800,
    longevity=200,
    reach=[
        (0, 0),
        (-1, 0), (1, 0), (0, -1), (0, 1)
    ],
    cost=50
)

TOOLS = {
    'hand_hoe': HAND_HOE,
    'scythe': SCYTHE
}


def get_tool(sprite_name: str) -> Tool:
    """Get tool by sprite name
    
    Args:
        sprite_name: Name of the tool sprite
        
    Returns:
        Tool instance
        
    Raises:
        KeyError: If tool not found
    """
    return TOOLS[sprite_name]
