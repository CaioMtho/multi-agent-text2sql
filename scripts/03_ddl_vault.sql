
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    kdf_salt TEXT NOT NULL,
    wrapped_master_key TEXT NOT NULL, 
    
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE vaults (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE secrets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vault_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    ciphertext TEXT NOT NULL,     
    
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (vault_id) REFERENCES vaults(id) ON DELETE CASCADE
);