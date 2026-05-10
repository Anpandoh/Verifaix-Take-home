PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS prompts;

CREATE TABLE IF NOT EXISTS description_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT NOT NULL DEFAULT 'default',
    version TEXT NOT NULL UNIQUE,
    pdf_path TEXT NOT NULL,
    text_hash TEXT NOT NULL,
    extracted_text TEXT NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE(project_name, version)
);

CREATE TABLE IF NOT EXISTS test_plans (
    version TEXT PRIMARY KEY,
    description_version TEXT NOT NULL,
    summary TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(description_version) REFERENCES description_versions(version)
);

CREATE TABLE IF NOT EXISTS test_plan_items (
    version TEXT NOT NULL,
    item_id TEXT NOT NULL,
    description TEXT NOT NULL,
    source_sections TEXT NOT NULL,
    test_type TEXT NOT NULL,
    expected_behavior TEXT NOT NULL,
    edge_case INTEGER NOT NULL,
    PRIMARY KEY(version, item_id),
    FOREIGN KEY(version) REFERENCES test_plans(version)
);

CREATE TABLE IF NOT EXISTS test_plan_deltas (
    delta_id TEXT NOT NULL,
    old_version TEXT NOT NULL,
    new_version TEXT NOT NULL,
    change_type TEXT NOT NULL,
    item_id TEXT NOT NULL,
    before_text TEXT,
    after_text TEXT,
    PRIMARY KEY(new_version, delta_id)
);

CREATE TABLE IF NOT EXISTS generated_code (
    version TEXT NOT NULL,
    module_name TEXT NOT NULL,
    code_path TEXT NOT NULL,
    created_at TEXT NOT NULL,
    PRIMARY KEY(version, module_name)
);

CREATE TABLE IF NOT EXISTS generated_tests (
    version TEXT NOT NULL,
    test_name TEXT NOT NULL,
    test_plan_item_id TEXT NOT NULL,
    code_path TEXT NOT NULL,
    created_at TEXT NOT NULL,
    PRIMARY KEY(version, test_name, test_plan_item_id)
);

CREATE TABLE IF NOT EXISTS artifacts (
    version TEXT NOT NULL,
    artifact_type TEXT NOT NULL,
    name TEXT NOT NULL,
    path TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    created_at TEXT NOT NULL,
    PRIMARY KEY(version, artifact_type, name)
);

CREATE TABLE IF NOT EXISTS execution_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version TEXT NOT NULL,
    test_name TEXT NOT NULL,
    test_plan_item_ids TEXT NOT NULL,
    status TEXT NOT NULL,
    failure_message TEXT,
    duration_seconds REAL NOT NULL,
    created_at TEXT NOT NULL
);
