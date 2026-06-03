COURSES_TABLE = '''
CREATE TABLE IF NOT EXISTS courses (
    course_id TEXT PRIMARY KEY,
    title TEXT,
    url TEXT
)
'''

CONTENT_TABLE = '''
CREATE TABLE IF NOT EXISTS learning_content (
    content_id TEXT PRIMARY KEY,
    course_id TEXT,
    title TEXT,
    content_type TEXT,
    url TEXT
)
'''

PROGRESS_TABLE = '''
CREATE TABLE IF NOT EXISTS progress (
    content_id TEXT PRIMARY KEY,
    status TEXT,
    percent REAL,
    updated_at DATETIME
)
'''
