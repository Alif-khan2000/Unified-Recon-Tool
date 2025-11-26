import json
import os
from typing import Any

def save_json_report(data: Any, target: str, out_path: str = None) -> str:
    """Write JSON report to reports/<target>/recon.json (or provided path)."""
    path = out_path or os.path.join('reports', target, 'recon.json')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    return path
