import os
import subprocess
import sys

script_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
chatbot_script = os.path.join(script_dir, "chatbot.py")
subprocess.run(f'start cmd /k python "{chatbot_script}" & pause', shell=True)