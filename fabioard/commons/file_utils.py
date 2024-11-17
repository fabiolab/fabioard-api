from pathlib import Path


def get_files(path: Path, extension: str = "*") -> list[Path]:
    return list(path.rglob(f'*{extension}', case_sensitive=False))
