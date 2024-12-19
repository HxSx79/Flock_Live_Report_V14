from typing import Dict
from datetime import datetime

class DataDisplay:
    @staticmethod
    def format_production_data(data: Dict) -> Dict:
        """Format production data for display"""
        return {
            'line1_part': {
                'program': str(data['line1_part']['program']),
                'number': str(data['line1_part']['number']),
                'description': str(data['line1_part']['description'])
            },
            'line1_production': {
                'quantity': int(data['line1_production']['quantity']),
                'delta': int(data['line1_production']['delta'])
            },
            'line1_scrap': {
                'total': int(data['line1_scrap']['total']),
                'rate': float(data['line1_scrap']['rate'])
            },
            'line2_part': {
                'program': str(data['line2_part']['program']),
                'number': str(data['line2_part']['number']),
                'description': str(data['line2_part']['description'])
            },
            'line2_production': {
                'quantity': int(data['line2_production']['quantity']),
                'delta': int(data['line2_production']['delta'])
            },
            'line2_scrap': {
                'total': int(data['line2_scrap']['total']),
                'rate': float(data['line2_scrap']['rate'])
            },
            'total_quantity': int(data['total_quantity']),
            'total_delta': int(data['total_delta']),
            'total_scrap': int(data['total_scrap']),
            'average_scrap_rate': float(data['average_scrap_rate']),
            'current_time': datetime.now().strftime("%H:%M:%S"),
            'success': True
        }