import json
from pathlib import Path
for p in (Path(__file__).resolve().parent.parent/'data'/'pakistan').glob('*.json'): print(p.name,len(json.loads(p.read_text(encoding='utf-8'))),'records')
