#!/usr/bin/env python3
"""
Weed Whacker - Game Launcher
Run this script to start the game.
Use --dev for live reloading during development.
"""

import sys
import os
import time
import subprocess

def get_latest_mtime(watch_dir):
    """Get the most recent modification time of any Python file in the directory."""
    latest = 0
    for root, _, files in os.walk(watch_dir):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                try:
                    mtime = os.path.getmtime(path)
                    if mtime > latest:
                        latest = mtime
                except OSError:
                    pass
    return latest

def run_with_live_reload():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    watch_dir = os.path.join(base_dir, 'weed_whacker')
    
    last_mtime = get_latest_mtime(watch_dir)
    
    print(f"[*] Starting live reload server...")
    print(f"[*] Watching for changes in: {watch_dir}")
    print(f"[*] Press Ctrl+C to stop.")
    
    # Start the initial game process without the --dev flag
    cmd = [sys.executable, __file__]
    args_without_dev = [arg for arg in sys.argv[1:] if arg != '--dev']
    cmd.extend(args_without_dev)
    
    process = subprocess.Popen(cmd)
    
    try:
        while True:
            time.sleep(0.5)  # Poll every half second
            current_mtime = get_latest_mtime(watch_dir)
            
            # If a file was modified, restart the process
            if current_mtime > last_mtime:
                print("\n[*] File change detected! Restarting game...")
                process.terminate()
                process.wait()  # Wait for it to close
                
                # Start a new process
                process = subprocess.Popen(cmd)
                last_mtime = current_mtime
                
    except KeyboardInterrupt:
        print("\n[*] Stopping live reload server...")
        if process.poll() is None:
            process.terminate()
            process.wait()

if __name__ == "__main__":
    if "--dev" in sys.argv:
        run_with_live_reload()
    else:
        from weed_whacker.main import main
        main()
