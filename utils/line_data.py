from dataclasses import dataclass
from typing import Dict

@dataclass
class LineData:
    """Data structure for line-specific information"""
    part: Dict[str, str]
    production: Dict[str, int]
    scrap: Dict[str, float]

    @classmethod
    def create_default(cls) -> 'LineData':
        """Create a default LineData instance"""
        return cls(
            part={'program': 'No Part', 'number': 'No Part', 'description': 'No Part'},
            production={'quantity': 0, 'delta': 0},
            scrap={'total': 0, 'rate': 0.0}
        )

    def update_part_info(self, part_info: Dict[str, str]) -> None:
        """Update part information"""
        self.part.update({
            'program': part_info['program'],
            'number': part_info['part_number'],
            'description': part_info['description']
        })

    def update_production(self, new_quantity: int) -> int:
        """Update production quantity and return delta"""
        old_quantity = self.production['quantity']
        delta = new_quantity - old_quantity
        self.production.update({
            'quantity': new_quantity,
            'delta': delta
        })
        return delta

    def update_scrap_rate(self) -> None:
        """Update scrap rate based on current quantities"""
        if self.production['quantity'] > 0:
            self.scrap['rate'] = round((self.scrap['total'] / self.production['quantity']) * 100, 1)
        else:
            self.scrap['rate'] = 0.0