import requests
import os
import json
import yaml
from pathlib import Path

NIST_CPRT_URL = os.getenv("NIST_CPRT_URL", "https://cprt-beta.nist.gov/api/cprt/export/json")
PROMPTS_DIR = Path("/app/prompts") if os.path.exists("/app/prompts") else Path("prompts")
SPECS_DIR = Path("specs/personas")
OPENCLAW_SKILLS_DIR = Path("/root/.openclaw/workspace/skills") if os.path.exists("/root/.openclaw") else Path("openclaw_config/workspace/skills")

def fetch_nist_data():
    try:
        # Attempt to fetch real NIST data if URL is provided and accessible
        if NIST_CPRT_URL and not NIST_CPRT_URL.startswith("http://placeholder"):
            try:
                response = requests.get(NIST_CPRT_URL, timeout=10)
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                print(f"Live NIST fetch failed, falling back to prototype data: {e}")

        # Mocking NIST data for the prototype
        return {
            "tasks": [
                {"id": "T0001", "description": "Conduct vulnerability scans."},
                {"id": "T0002", "description": "Analyze network traffic to identify anomalies."},
                {"id": "T0161", "description": "Coordinate incident response activities."}
            ],
            "work_roles": [
                {
                    "id": "PD-WRL-002",
                    "name": "Incident Response",
                    "task_ids": ["T0161", "T0002"]
                }
            ]
        }
    except Exception as e:
        print(f"Error fetching NIST data: {e}")
        return None

def generate_tks_json(persona_id, nice_role_id, nist_data):
    work_role = next((r for r in nist_data["work_roles"] if r["id"] == nice_role_id), None)
    if not work_role:
        print(f"Work role {nice_role_id} not found in NIST data.")
        return

    tks = {
        "persona_id": persona_id,
        "nice_role_id": nice_role_id,
        "tasks": [t for t in nist_data["tasks"] if t["id"] in work_role["task_ids"]],
        # Add Knowledge and Skills similarly if available in nist_data
    }

    output_path = PROMPTS_DIR / persona_id / "tks.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(tks, f, indent=2)
    print(f"Generated TKS JSON for {persona_id}")

def update_openclaw_skills(nist_data):
    for task in nist_data["tasks"]:
        skill_dir = OPENCLAW_SKILLS_DIR / task["id"]
        skill_dir.mkdir(parents=True, exist_ok=True)

        skill_md = f"""# Skill: {task['id']}
## Description
{task['description']}

## NICE Mapping
- Task ID: {task['id']}
"""
        with open(skill_dir / "SKILL.md", "w") as f:
            f.write(skill_md)
    print("Updated OpenClaw Skill Registry")

def sync():
    print("NIST-Sync Worker starting...")
    nist_data = fetch_nist_data()
    if not nist_data:
        return

    # Process all personas in specs
    for spec_file in SPECS_DIR.glob("*.yaml"):
        with open(spec_file, "r") as f:
            spec = yaml.safe_load(f)
            persona_id = spec["id"]
            # For simplicity, we assume we can map persona_id to NICE ID.
            # In pd-ir.yaml it says NICE Work Role: Incident Response (PD-WRL-002)
            # Let's extract it or assume a mapping.
            nice_role_id = "PD-WRL-002" if persona_id == "pd-ir" else None
            if nice_role_id:
                generate_tks_json(persona_id, nice_role_id, nist_data)

    update_openclaw_skills(nist_data)

if __name__ == "__main__":
    sync()
