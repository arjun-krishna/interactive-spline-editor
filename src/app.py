"""
filename: app.py

Application launcher
"""
from window import AppWindow

def main() -> None:
    window = AppWindow()
    window.run()

if __name__ == "__main__":
    main()