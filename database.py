"""
Database Layer for Aerial Infrastructure Classification & Intelligence System
=============================================================================
Manages SQLite database storage for users and prediction inspection records.
"""

import os
import sqlite3
import json
from werkzeug.security import generate_password_hash, check_password_hash

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
INSTANCE_DIR = os.path.join(PROJECT_DIR, "instance")
os.makedirs(INSTANCE_DIR, exist_ok=True)
DB_PATH = os.path.join(INSTANCE_DIR, "infrastructure_intelligence.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'Analyst',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Predictions Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            filename TEXT NOT NULL,
            filepath TEXT NOT NULL,
            predicted_class TEXT NOT NULL,
            confidence REAL NOT NULL,
            confidence_label TEXT NOT NULL,
            top_predictions_json TEXT NOT NULL,
            image_quality TEXT NOT NULL,
            quality_details_json TEXT NOT NULL,
            risk_score INTEGER NOT NULL,
            priority TEXT NOT NULL,
            visual_indicators_json TEXT NOT NULL,
            importance TEXT NOT NULL,
            risks_json TEXT NOT NULL,
            recommended_action TEXT NOT NULL,
            location TEXT DEFAULT 'Location not provided',
            latitude TEXT DEFAULT '',
            longitude TEXT DEFAULT '',
            heatmap_path TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()

    # Seed Default Users if empty
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        default_users = [
            ('admin', generate_password_hash('admin123'), 'Administrator'),
            ('analyst', generate_password_hash('analyst123'), 'Analyst'),
            ('officer', generate_password_hash('officer123'), 'Defense Officer'),
            ('user', generate_password_hash('user123'), 'Analyst')
        ]
        cursor.executemany(
            'INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
            default_users
        )
        conn.commit()

    conn.close()
    print("[SUCCESS] SQLite Database initialized at:", DB_PATH)

def verify_user_login(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user['password_hash'], password):
        return True, user['role']
    # Fallback check for legacy unhashed or demo matching
    if username in ['admin', 'analyst', 'user', 'officer'] and password in ['admin123', 'analyst123', 'user123', 'officer123']:
        return True, 'Analyst'
    return False, None

def save_prediction_record(record_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO predictions (
            username, filename, filepath, predicted_class, confidence,
            confidence_label, top_predictions_json, image_quality, quality_details_json,
            risk_score, priority, visual_indicators_json, importance, risks_json,
            recommended_action, location, latitude, longitude, heatmap_path
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        record_data.get('username', 'Guest Analyst'),
        record_data.get('filename', ''),
        record_data.get('filepath', ''),
        record_data.get('predicted_class', ''),
        record_data.get('confidence', 0.0),
        record_data.get('confidence_label', ''),
        json.dumps(record_data.get('top_predictions', [])),
        record_data.get('image_quality', 'Good'),
        json.dumps(record_data.get('quality_details', {})),
        record_data.get('risk_score', 50),
        record_data.get('priority', 'Medium'),
        json.dumps(record_data.get('visual_indicators', [])),
        record_data.get('importance', ''),
        json.dumps(record_data.get('risks', [])),
        record_data.get('recommended_action', ''),
        record_data.get('location', 'Location not provided'),
        record_data.get('latitude', ''),
        record_data.get('longitude', ''),
        record_data.get('heatmap_path', '')
    ))

    conn.commit()
    inserted_id = cursor.lastrowid
    conn.close()
    return inserted_id

def get_all_prediction_records():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM predictions ORDER BY timestamp DESC')
    rows = cursor.fetchall()
    conn.close()

    records = []
    for r in rows:
        item = dict(r)
        item['top_predictions'] = json.loads(item['top_predictions_json']) if item.get('top_predictions_json') else []
        item['quality_details'] = json.loads(item['quality_details_json']) if item.get('quality_details_json') else {}
        item['visual_indicators'] = json.loads(item['visual_indicators_json']) if item.get('visual_indicators_json') else []
        item['risks'] = json.loads(item['risks_json']) if item.get('risks_json') else []
        records.append(item)

    return records

def get_prediction_record_by_id(pred_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM predictions WHERE id = ?', (pred_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    item = dict(row)
    item['top_predictions'] = json.loads(item['top_predictions_json']) if item.get('top_predictions_json') else []
    item['quality_details'] = json.loads(item['quality_details_json']) if item.get('quality_details_json') else {}
    item['visual_indicators'] = json.loads(item['visual_indicators_json']) if item.get('visual_indicators_json') else []
    item['risks'] = json.loads(item['risks_json']) if item.get('risks_json') else []
    return item

def delete_prediction_record(pred_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM predictions WHERE id = ?', (pred_id,))
    conn.commit()
    conn.close()

def get_analytics_kpis():
    records = get_all_prediction_records()
    total_inspections = len(records)

    if total_inspections == 0:
        return {
            "total_inspections": 0,
            "high_priority_count": 0,
            "avg_confidence": 0.0,
            "most_detected": "None",
            "class_distribution": {},
            "priority_distribution": {"Low": 0, "Medium": 0, "High": 0, "Critical": 0}
        }

    high_priority_count = sum(1 for r in records if r.get('priority') in ['High', 'Critical'])
    avg_confidence = round(sum(r.get('confidence', 0) for r in records) / total_inspections, 2)

    class_counts = {}
    priority_counts = {"Low": 0, "Medium": 0, "High": 0, "Critical": 0}

    for r in records:
        cls = r.get('predicted_class', 'Unknown')
        class_counts[cls] = class_counts.get(cls, 0) + 1
        
        prio = r.get('priority', 'Medium')
        if prio in priority_counts:
            priority_counts[prio] += 1
        else:
            priority_counts[prio] = 1

    most_detected = max(class_counts, key=class_counts.get) if class_counts else "None"

    return {
        "total_inspections": total_inspections,
        "high_priority_count": high_priority_count,
        "avg_confidence": avg_confidence,
        "most_detected": most_detected,
        "class_distribution": class_counts,
        "priority_distribution": priority_counts
    }

if __name__ == '__main__':
    init_db()
