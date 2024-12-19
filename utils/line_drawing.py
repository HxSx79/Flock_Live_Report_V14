import cv2
from .config import Config

class LineDrawer:
    def __init__(self):
        self.config = Config()

    def draw_lines(self, frame: cv2.Mat) -> cv2.Mat:
        """Draw counting lines and labels on the frame"""
        height, width = frame.shape[:2]
        
        # Draw vertical counting line (yellow)
        line_x = int(width * self.config.vertical_line_position)
        cv2.line(frame, (line_x, 0), (line_x, height), (0, 255, 255), 2)
        
        # Draw horizontal zone separator line (white)
        line_y = int(height * self.config.horizontal_line_position)
        cv2.line(frame, (0, line_y), (width, line_y), (255, 255, 255), 2)
        
        # Add zone labels
        cv2.putText(frame, "Line 1", (10, int(height * 0.25)), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, "Line 2", (10, int(height * 0.75)), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        return frame