import magic, os

def identify_artifact(file_path: str):
    try:
        # Optimized for Windows python-magic-bin
        m = magic.Magic(mime=True)
        file_type = m.from_file(file_path)
    except:
        file_type = "text/plain"
    
    ext = os.path.splitext(file_path)[1].lower()
    mapping = {".py": "Python", ".java": "Java", ".js": "JavaScript"}
    
    return {
        "language": mapping.get(ext, "Unknown"),
        "mime": file_type
    }