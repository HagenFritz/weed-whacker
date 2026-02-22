"""
Weed Whacker - Events and Weather System
Handles random events and weather conditions that affect gameplay.
"""

from dataclasses import dataclass

@dataclass
class Event:
    """Represents a game event or weather condition"""
    id: str
    name: str
    description: str
    icon_name: str
    duration: int  # in milliseconds. -1 means infinite/default
    
    # Buffs and Nerfs (multipliers to base values)
    weed_spawn_rate_mult: float = 1.0
    weed_growth_rate_mult: float = 1.0
    player_speed_mult: float = 1.0
    income_mult: float = 1.0
    tool_cooldown_mult: float = 1.0

# Define default weather
SUNNY = Event(
    id="sunny",
    name="Sunny",
    description="Perfect weather for gardening. Normal conditions.",
    icon_name="sunny",
    duration=-1,
)

# Other potential events for the future:
RAINY = Event(
    id="rainy",
    name="Rainy",
    description="Weeds grow faster, but your tools cool down quicker.",
    icon_name="rainy",
    duration=30000,
    weed_growth_rate_mult=1.5,
    tool_cooldown_mult=0.8
)

DROUGHT = Event(
    id="drought",
    name="Drought",
    description="Weeds grow slower, but income is reduced.",
    icon_name="drought",
    duration=45000,
    weed_growth_rate_mult=0.5,
    income_mult=0.8
)

OVERGROWN = Event(
    id="overgrown",
    name="Overgrown",
    description="Weeds are spawning rapidly!",
    icon_name="overgrown",
    duration=20000,
    weed_spawn_rate_mult=2.5
)

# Registry of all events
EVENTS = {
    "sunny": SUNNY,
    "rainy": RAINY,
    "drought": DROUGHT,
    "overgrown": OVERGROWN
}

class EventManager:
    """Manages active events and provides current multipliers"""
    
    def __init__(self):
        self.current_event = SUNNY
        self.time_remaining = -1
        
    def start_event(self, event_id: str):
        """Start a new event by ID"""
        if event_id in EVENTS:
            self.current_event = EVENTS[event_id]
            self.time_remaining = self.current_event.duration
            
    def update(self, dt: int):
        """Update event timer
        
        Args:
            dt: Delta time in milliseconds
        """
        if self.time_remaining > 0:
            self.time_remaining -= dt
            if self.time_remaining <= 0:
                # Revert to default weather
                self.current_event = SUNNY
                self.time_remaining = -1
                
    def get_progress_percent(self) -> float:
        """Get the progress of the current event as a percentage (0.0 to 1.0)
        Returns 0.0 if the event is infinite.
        """
        if self.current_event.duration <= 0:
            return 0.0
            
        # 1.0 = just started, 0.0 = ending soon
        return max(0.0, self.time_remaining / self.current_event.duration)

    # Multiplier getters
    def get_weed_spawn_rate_mult(self) -> float:
        return self.current_event.weed_spawn_rate_mult

    def get_weed_growth_rate_mult(self) -> float:
        return self.current_event.weed_growth_rate_mult

    def get_player_speed_mult(self) -> float:
        return self.current_event.player_speed_mult

    def get_income_mult(self) -> float:
        return self.current_event.income_mult

    def get_tool_cooldown_mult(self) -> float:
        return self.current_event.tool_cooldown_mult
