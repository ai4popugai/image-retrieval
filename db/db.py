import glob
import os
import sqlite3

VIDEO_ID_KEY = 'video_id'
KEYFRAME_ID_KEY = 'keyframe_id'
OBJECTS_KEY = 'objects'
CONCEPT_KEY = 'concept'


class SQLiteDb:
    def __init__(self, db_name):
        self.db_dir = os.environ["SQLITE_DB_DIR"]

        self.version = len(glob.glob(os.path.join(self.db_dir, f"{db_name}*")))
        self.db_name = f"{db_name}_{self.version}"
        self.db_path = os.path.join(self.db_dir, self.db_name)
        self._create_db()

    def _create_db(self):
        with sqlite3.connect(self.db_path) as connect:
            cursor = connect.cursor()
            cursor.execute(f"CREATE TABLE {self.db_name}({VIDEO_ID_KEY},{KEYFRAME_ID_KEY},"
                           f"{OBJECTS_KEY},{CONCEPT_KEY})")
            connect.commit()

    def add_new_key(self, video_id, keyframe_id):
        with sqlite3.connect(self.db_path) as connect:
            cursor = connect.cursor()
            cursor.execute(f"INSERT INTO {self.db_name}({VIDEO_ID_KEY},{KEYFRAME_ID_KEY}) "
                           f"VALUES ('{video_id}', '{keyframe_id}')")
            connect.commit()
