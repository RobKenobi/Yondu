from modules.handtracking import HandDetector, HandProcessing

hand_detector = HandDetector()
hand_tracker = HandProcessing(hand_detector)
