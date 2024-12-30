from pathlib import Path

def get_db_path():
    try:
        db_path = Path.cwd().parent / "logged_entries"
        assert db_path.exists()
    except: 
        db_path = Path.cwd() / "logged_entries"
        assert db_path.exists()
    
    return db_path


# DB_PATH = Path.cwd().parent / "logged_entries"
MAX_ENTRIES = 10
