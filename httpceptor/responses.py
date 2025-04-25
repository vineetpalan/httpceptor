import json
import os
from pathlib import Path

mocked_responses = {}

if not mocked_responses:
    for file in Path(os.getenv("RESPONSE_DIR", "responses")).glob("*.json"):
        with open(file, "r") as f:
            data = json.load(f)
            mocked_responses.update(data)
