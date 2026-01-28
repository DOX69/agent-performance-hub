#!/usr/bin/env python3
"""Update README badge with latest token efficiency."""

import json
import re
from pathlib import Path

def main():
    # Lire métriques
    try:
        metrics = json.loads(
            Path('.agent/debug/token-metrics.json').read_text()
        )
        efficiency = metrics['token_efficiency']
    except FileNotFoundError:
        print("Metrics file not found, defaulting to 0")
        efficiency = 0
    
    # Déterminer couleur
    if efficiency >= 40:
        color = "brightgreen"
    elif efficiency >= 20:
        color = "yellow"
    else:
        color = "orange"
    
    # Format badge
    badge = f"![Token Efficiency](https://img.shields.io/badge/Token%20Efficiency-{efficiency}%25-{color})"
    
    # Lire README
    readme_path = Path('README.md')
    if not readme_path.exists():
        print("README.md not found")
        return

    readme = readme_path.read_text(encoding='utf-8')
    
    # Remplacer ou ajouter badge
    pattern = r"!\[Token Efficiency\]\(.*?\)"
    if re.search(pattern, readme):
        readme = re.sub(pattern, badge, readme)
    else:
        # Ajouter après le titre principal
        readme = readme.replace(
            "# AGENT-PERFORMANCE-HUB",
            f"# AGENT-PERFORMANCE-HUB\n\n{badge}"
        )
    
    readme_path.write_text(readme, encoding='utf-8')
    print(f"✅ Badge updated: Token Efficiency {efficiency}%")

if __name__ == "__main__":
    main()
