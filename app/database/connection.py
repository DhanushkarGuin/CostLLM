import sqlite3
import os

# 1. Define where the database file will live securely
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "router.sqlite")

def init_db():
    """Creates the 'data' folder, the database file, and the request_logs table."""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS request_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        prompt TEXT NOT NULL,
        routed_tier TEXT NOT NULL,
        model_used TEXT NOT NULL,
        simulated_savings REAL NOT NULL
    );
    """
    cursor.execute(create_table_sql)
    conn.commit()
    conn.close()

def log_request(prompt: str, routed_tier: str, model_used: str):
    """Calculates savings and inserts a new routing event into the database."""
    
    # 1. The Cost Savings Math
    baseline_cost = 0.010 
    
    if routed_tier == "tier_3_basic":
        actual_cost = 0.001
    else:
        actual_cost = 0.010
        
    simulated_savings = baseline_cost - actual_cost
    
    # 2. Database Insertion
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    insert_sql = """
    INSERT INTO request_logs (prompt, routed_tier, model_used, simulated_savings)
    VALUES (?, ?, ?, ?)
    """
    
    cursor.execute(insert_sql, (prompt, routed_tier, model_used, simulated_savings))
    conn.commit()
    conn.close()
    
    print(f"Ledger Updated | Tier: {routed_tier} | Saved: ${simulated_savings:.3f}")

if __name__ == "__main__":
    init_db()