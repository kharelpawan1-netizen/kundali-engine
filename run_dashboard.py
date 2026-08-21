"""
run_dashboard.py

Convenient launcher for the Vedic Kundali Dashboard application.
Starts Uvicorn server and serves the full interactive dashboard.
Automatically finds an available port if port 8000 is occupied.
"""

import socket
import sys
import webbrowser
from pathlib import Path

# Set UTF-8 output if supported
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

import uvicorn


def find_available_port(start_port: int = 8000, max_attempts: int = 10) -> int:
    """Find the first available port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            res = s.connect_ex(("127.0.0.1", port))
            if res != 0:
                return port
    return start_port


def main():
    host = "127.0.0.1"
    port = find_available_port(8000)
    url = f"http://{host}:{port}"

    print("=" * 70)
    print("✨ STARTING VEDIC KUNDALI DASHBOARD")
    print(f"🚀 Dashboard URL: {url}")
    print("=" * 70)

    # Automatically open default browser after 1.2s
    try:
        import threading
        import time

        def open_browser():
            time.sleep(1.2)
            webbrowser.open(url)

        threading.Thread(target=open_browser, daemon=True).start()
    except Exception:
        pass

    uvicorn.run("api.app:app", host=host, port=port, log_level="info", reload=False)


if __name__ == "__main__":
    main()
