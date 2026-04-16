import psutil
import time
import sys

LAUNCHER_NAME = "ArmouryCrateSE.exe"
XBOX_NAME = "XboxPcApp.exe"
MAX_TIME = 100


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
    print(f"Watching for {LAUNCHER_NAME} and {XBOX_NAME}...")

    for elapsed in range(MAX_TIME):
        launcher_running = check_if_process_exists(LAUNCHER_NAME)
        xbox_running = check_if_process_exists(XBOX_NAME)

        if launcher_running and xbox_running:
            print(f"Both processes detected at {elapsed}s. Closing Xbox...")
            kill_process(XBOX_NAME)
            print("Done.")
            sys.exit(0)

        time.sleep(1)

    print(f"Timeout reached ({MAX_TIME}s). Xbox was not closed.")
    sys.exit(1)


if __name__ == "__main__":
    main()