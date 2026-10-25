import paramiko
import json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("207.180.255.35", username="root")

cmd = 'curl -s -H "Accept: application/json" https://zenodo.org/api/records/23642090'
stdin, stdout, stderr = ssh.exec_command(cmd)
out = stdout.read().decode()
ssh.close()

try:
    data = json.loads(out)
    print("Status: SUCCESS from pcworm-root!")
    print("DOI:", data.get("doi"))
    print("Concept DOI:", data.get("conceptdoi"))
    print("Record ID:", data.get("id"))
    print("Title:", data.get("metadata", {}).get("title"))
    print("Version:", data.get("metadata", {}).get("version"))
    print("Publication Date:", data.get("metadata", {}).get("publication_date"))
    print("Resource Type:", data.get("metadata", {}).get("resource_type"))
    print("\nCreators:")
    for c in data.get("metadata", {}).get("creators", []):
        print(f"  - {c.get('name')} | Affiliation: {c.get('affiliation')}")
    print("\nContributors:")
    for c in data.get("metadata", {}).get("contributors", []):
        print(f"  - {c.get('name')} | Role: {c.get('type')} | Affiliation: {c.get('affiliation')}")
    print(f"\nFiles ({len(data.get('files', []))}):")
    for f in data.get("files", []):
        print(f"  - {f.get('key')} ({f.get('size')} bytes)")
    print("\nRelated Identifiers:")
    for r in data.get("metadata", {}).get("related_identifiers", []):
        print(f"  - {r.get('relation')} -> {r.get('identifier')} ({r.get('scheme')})")
except Exception as e:
    print("Failed to parse response:", e)
    print("Raw output:", out[:400])
