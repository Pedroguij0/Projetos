import os
import subprocess

script_dir = os.path.dirname(os.path.abspath(__file__))
chatbot_script = os.path.join(script_dir, "chatbot.py")
subprocess.run(f'start cmd /k python "{chatbot_script}" & pause', shell=True)