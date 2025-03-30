
import os

migrations_path = os.path.join(os.path.dirname(__file__), "../todoapp/migrations")
os.makedirs(migrations_path, exist_ok=True)

