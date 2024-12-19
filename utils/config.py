class Config:
    def __init__(self):
        # Video settings
        self.frame_width = 1020
        self.frame_height = 600
        self.frame_rate = 25
        self.camera_id = "/dev/video0"
        
        # Detection settings
        self.model_path = "best.pt"
        self.confidence_threshold = 0.95
        
        # Line positions (as percentage of frame)
        self.vertical_line_position = 0.5
        self.horizontal_line_position = 0.5