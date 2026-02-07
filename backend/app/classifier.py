import magic
import yaml
import os

MANIFEST_PATH = "../engines_manifest.yaml"

def discover_capabilities(file_path):
    mime = magic.Magic(mime=True).from_file(file_path)
    ext = os.path.splitext(file_path)[1]
    
    if not os.path.exists(MANIFEST_PATH):
        return {"error": "Manifest file not found"}

    with open(MANIFEST_PATH, "r") as f:
        manifest = yaml.safe_load(f)

    for engine in manifest.get('engines', []):
        if engine['extension'] == ext or engine['mime_type'] == mime:
            return {
                "language": engine.get('name'),
                "supported_tests": list(engine['test_types'].keys()),
                "mime": mime
            }
            
    return {"error": "Unsupported format", "mime": mime}