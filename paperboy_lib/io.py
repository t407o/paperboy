import os


def read_lines(file_path: str) -> list[str]:
    if not os.path.exists(os.path.join(os.environ.get("PAPERBOY_CONFIG_DIR"), file_path)):
        raise FileNotFoundError(f"{file_path} not found in config dir... Check your files and create if not exists!!!")
    
    arr = []
    with open(os.path.join(os.environ.get("PAPERBOY_CONFIG_DIR"), file_path), "r", encoding="utf-8") as f:
        for line in f:
            arr.append(line.strip()) if line.strip() else None
    return arr

def read_str(file_path: str) -> str:
    with open(os.path.join(os.environ.get("PAPERBOY_CONFIG_DIR"), file_path), "r", encoding="utf-8") as f:
        return f.read().strip()