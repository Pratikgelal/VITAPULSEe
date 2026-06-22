from app import create_app
import os
import sys

# Point Python explicitly to the root task directory where Vercel unzips your code
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# Vercel looks for an object named 'app' at the module level
app = create_app()
