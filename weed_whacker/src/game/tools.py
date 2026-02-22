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
    description: str
    efficiency: float
    cooldown: int
    longevity: int
    reach: List[Tuple[int, int]]
    cost: int
    sound_file: str | None = None
    
    def __post_init__(self):
        """Validate tool attributes"""
        if self.efficiency <= 0:
            raise ValueError(f"Tool {self.name} efficiency must be positive")
        if self.cooldown < 0:
            raise ValueError(f"Tool {self.name} cooldown must be non-negative")


HAND_HOE = Tool(
    name="Hand Hoe",
    sprite_name="hand_hoe",
    description="A basic tool for clearing single tiles of weeds.",
    efficiency=1.0,
    cooldown=1000,
    longevity=-1,
    reach=[(0, 0)],
    cost=0,
    sound_file="assets/sounds/hand_hoe.wav"
)

SCYTHE = Tool(
    name="Scythe",
    sprite_name="scythe",
    description="A sharp blade that clears the target tile and its adjacent neighbors.",
    efficiency=1.5,
    cooldown=800,
    longevity=200,
    reach=[
        (0, 0),
        (-1, 0), (1, 0), (0, -1), (0, 1)
    ],
    cost=50,
    sound_file="assets/sounds/scythe.wav"
)

CHAINSAW = Tool(
    name="Chainsaw",
    sprite_name="chainsaw",
    description="A heavy-duty machine that clears a 3x3 area around the target.",
    efficiency=2.0,
    cooldown=700,
    longevity=400,
    reach=[
        (-1, -1), (0, -1), (1, -1),
        (-1, 0),  (0, 0),  (1, 0),
        (-1, 1),  (0, 1),  (1, 1)
    ],
    cost=300,
    sound_file="assets/sounds/chainsaw.wav"
)

AEROSOL = Tool(
    name="Aerosol Spray",
    sprite_name="aerosol",
    description="Fast-acting weed killer with very short cooldown but limited uses.",
    efficiency=1.0,
    cooldown=200,
    longevity=50,
    reach=[(0, 0)],
    cost=25,
    sound_file="assets/sounds/aerosol.wav"
)

SHEARS = Tool(
    name="Garden Shears",
    sprite_name="shears",
    description="Reliable and fast shears for quick, single-target trimming.",
    efficiency=1.2,
    cooldown=400,
    longevity=300,
    reach=[(0, 0)],
    cost=150,
    sound_file="assets/sounds/shears.wav"
)

TOOLS = {
    'hand_hoe': HAND_HOE,
    'scythe': SCYTHE,
    'chainsaw': CHAINSAW,
    'aerosol': AEROSOL,
    'shears': SHEARS
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
