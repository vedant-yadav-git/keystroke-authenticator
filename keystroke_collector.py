"""
Simple Keystroke Data Collector
Captures key press/release times and saves to CSV.
Press ESC to stop recording.
"""

import csv
import time
from datetime import datetime
from pynput import keyboard
import os

class KeystrokeCollector:
    def __init__(self):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_file = f"data/keystrokes_{self.session_id}.csv"
        self.press_times = {}
        self.keystroke_count = 0
        
        # Create data directory
        os.makedirs("data", exist_ok=True)
        
        # Create CSV with headers
        with open(self.output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['session_id', 'key', 'press_time', 'release_time'])
    
    def on_press(self, key):
        """Record when key is pressed"""
        try:
            key_name = key.char if hasattr(key, 'char') and key.char else str(key)
            self.press_times[key_name] = time.time()
        except:
            pass
    
    def on_release(self, key):
        """Record when key is released and save to CSV"""
        # ESC to stop
        if key == keyboard.Key.esc:
            print("\nStopping...")
            return False
        
        try:
            key_name = key.char if hasattr(key, 'char') and key.char else str(key)
            release_time = time.time()
            
            # Only save if we have a press time
            if key_name in self.press_times:
                press_time = self.press_times[key_name]
                
                # Write to CSV
                with open(self.output_file, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([self.session_id, key_name, press_time, release_time])
                
                del self.press_times[key_name]
                self.keystroke_count += 1
                
                # Progress update
                if self.keystroke_count % 50 == 0:
                    print(f"Captured {self.keystroke_count} keystrokes...")
        except:
            pass
    
    def start(self):
        """Start recording"""
        print(f"\n{'='*50}")
        print(f"RECORDING - Session: {self.session_id}")
        print(f"{'='*50}")
        print("Start typing... (Press ESC to stop)")
        print(f"{'='*50}\n")
        
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()
        
        print(f"\n{'='*50}")
        print(f"Keystrokes saved: {self.keystroke_count}")
        print(f"File: {self.output_file}")
        print(f"{'='*50}\n")


if __name__ == "__main__":
    print("\nKeystroke Collector")
    print("WARNING: Don't type passwords!\n")
    
    input("Press ENTER to start recording...")
    
    collector = KeystrokeCollector()
    collector.start()
