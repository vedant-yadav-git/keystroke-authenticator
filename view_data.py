"""
Simple data viewer for keystroke data
Shows basic stats and preview of collected data
"""

import pandas as pd
import os
import glob

def view_latest_session():
    """View the most recent keystroke session"""
    
    # Find all CSV files in data directory
    csv_files = glob.glob("data/keystrokes_*.csv")
    
    if not csv_files:
        print("No data files found. Run keystroke_collector.py first!")
        return
    
    # Get most recent file
    latest_file = max(csv_files, key=os.path.getctime)
    
    # Load data
    df = pd.read_csv(latest_file)
    
    print(f"\n{'='*60}")
    print(f"Session: {latest_file}")
    print(f"{'='*60}\n")
    
    # Basic stats
    print(f"Total keystrokes: {len(df)}")
    
    if len(df) > 0:
        # Calculate dwell times (how long key was held)
        df['dwell_time'] = df['release_time'] - df['press_time']
        
        # Calculate flight times (time between key presses)
        df['flight_time'] = df['press_time'].diff()
        
        print(f"\nDwell Time Stats (milliseconds):")
        print(f"  Average: {df['dwell_time'].mean() * 1000:.2f} ms")
        print(f"  Min: {df['dwell_time'].min() * 1000:.2f} ms")
        print(f"  Max: {df['dwell_time'].max() * 1000:.2f} ms")
        
        print(f"\nFlight Time Stats (milliseconds):")
        print(f"  Average: {df['flight_time'].mean() * 1000:.2f} ms")
        
        # Session duration
        duration = df['release_time'].max() - df['press_time'].min()
        print(f"\nSession Duration: {duration:.2f} seconds")
        print(f"Typing Speed: {len(df) / duration:.2f} keys/second")
        
        # Key frequency (top 10)
        print(f"\nMost Pressed Keys:")
        print(df['key'].value_counts().head(10))
        
        print(f"\n{'='*60}")
        print(f"First 10 keystrokes:")
        print(f"{'='*60}")
        print(df[['key', 'dwell_time', 'flight_time']].head(10).to_string(index=False))
        print()

if __name__ == "__main__":
    view_latest_session()
