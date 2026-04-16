import psutil
import time
import sys

LAUNCHER_NAME = "ArmouryCrateSE.exe"
XBOX_PROCESSES = ["XboxPcApp.exe", "XboxPcAppFT.exe", "Xbox.exe"]
MAX_WAIT_TIME = 300       # How long to watch for both processes (seconds)
KILL_DELAY = 1           # How long to wait after detection before killing (seconds)


def check_if_process_exists(name: str) -> bool:
    """Check if a process with the given name is currently running."""
    for proc in psutil.process_iter(["name"]):
        try:
            if proc.info["name"] and proc.info["name"].lower() == name.lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False


def kill_process(name: str) -> None:
    """Force kill all processes matching the given name."""
    for proc in psutil.process_iter(["name"]):
        try:
            if proc.info["name"] and proc.info["name"].lower() == name.lower():
                proc.kill()
                print(f"Killed process: {name} (PID {proc.pid})")
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            print(f"Could not kill {name}: {e}")


def main():
    print(f"Watching for {LAUNCHER_NAME} and Xbox apps...")

    for elapsed in range(MAX_WAIT_TIME):
        launcher_running = check_if_process_exists(LAUNCHER_NAME)
        
        # Check if ANY of the Xbox processes are running
        xbox_running = any(check_if_process_exists(p) for p in XBOX_PROCESSES)

        if launcher_running and xbox_running:
            print(f"Both processes detected at {elapsed}s.")
            print(f"Waiting {KILL_DELAY}s before closing Xbox...")

            # Wait, but keep checking if Xbox was manually closed during delay
            for i in range(KILL_DELAY):
                time.sleep(1)
                # If ALL Xbox processes are gone, exit gracefully
                if not any(check_if_process_exists(p) for p in XBOX_PROCESSES):
                    print("Xbox was already closed manually. Exiting.")
                    sys.exit(0)
                print(f"  Closing in {KILL_DELAY - i - 1}s...")

            print("Closing Xbox now...")
            
            # Loop through and kill all of them
            for p in XBOX_PROCESSES:
                kill_process(p)
                
            print("Done.")
            sys.exit(0)

        time.sleep(1)

    print(f"Timeout reached ({MAX_WAIT_TIME}s). Xbox was not closed.")
    sys.exit(1)


if __name__ == "__main__":
    main()