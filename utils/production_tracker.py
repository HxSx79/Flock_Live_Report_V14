from typing import Dict, Optional
from .bom_reader import BOMReader
from .excel_logger import ExcelLogger
from .line_data import LineData
from .data_display import DataDisplay

class ProductionTracker:
    def __init__(self):
        self.bom_reader = BOMReader()
        self.excel_logger = ExcelLogger()
        self.line1 = LineData.create_default()
        self.line2 = LineData.create_default()
        self.processed_timestamps = set()
        self.total_quantity = 0
        self.total_scrap = 0

    def _process_line_crossing(self, line_data: LineData, line_number: int, 
                             class_name: str, timestamp: int) -> None:
        """Process a line crossing event"""
        if timestamp not in self.processed_timestamps:
            print(f"Processing crossing for line {line_number}: {class_name}")
            
            # Get part info from BOM
            part_info = self.bom_reader.get_part_info(class_name)
            
            # Update line data
            line_data.update_part_info(part_info)
            
            # Log to Excel
            self.excel_logger.log_crossing(line_number, class_name, part_info)
            
            # Mark timestamp as processed
            self.processed_timestamps.add(timestamp)
            print(f"Updated line {line_number} part info: {part_info}")

    def update_production(self, counts: Dict[str, int], 
                         latest_crossings: Dict[str, Optional[Dict]]) -> None:
        """Update production data based on line crossings"""
        # Update Line 1
        delta1 = self.line1.update_production(counts['line1'])
        if delta1 > 0:
            self.total_quantity += delta1
            
        if latest_crossings['line1']:
            self._process_line_crossing(
                self.line1,
                1,
                latest_crossings['line1']['class_name'],
                latest_crossings['line1']['timestamp']
            )
        
        # Update Line 2
        delta2 = self.line2.update_production(counts['line2'])
        if delta2 > 0:
            self.total_quantity += delta2
            
        if latest_crossings['line2']:
            self._process_line_crossing(
                self.line2,
                2,
                latest_crossings['line2']['class_name'],
                latest_crossings['line2']['timestamp']
            )

        # Update scrap rates
        self.line1.update_scrap_rate()
        self.line2.update_scrap_rate()

    def get_all_data(self) -> Dict:
        """Get all production data for display"""
        # Calculate total scrap and average scrap rate
        total_scrap = self.line1.scrap['total'] + self.line2.scrap['total']
        avg_scrap_rate = 0.0
        
        if self.total_quantity > 0:
            avg_scrap_rate = round((total_scrap / self.total_quantity) * 100, 1)

        data = {
            'line1_part': self.line1.part,
            'line1_production': self.line1.production,
            'line1_scrap': self.line1.scrap,
            'line2_part': self.line2.part,
            'line2_production': self.line2.production,
            'line2_scrap': self.line2.scrap,
            'total_quantity': self.total_quantity,
            'total_delta': self.line1.production['delta'] + self.line2.production['delta'],
            'total_scrap': total_scrap,
            'average_scrap_rate': avg_scrap_rate
        }
        
        return DataDisplay.format_production_data(data)