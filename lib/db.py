from datetime import datetime
import time
from mysql.connector import MySQLConnection

from lib.file import File


class DB():
    @staticmethod
    def _login(db_config: dict) -> MySQLConnection:
        return MySQLConnection(
            host=db_config["host"],
            port=db_config["port"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"]
        )

    @staticmethod
    def _logout(conn: MySQLConnection) -> None:
        conn.close()

    @staticmethod
    def _execute(conn: MySQLConnection, query: str, values: tuple = None) -> None:
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        cursor.close()

    @staticmethod
    def _make_file_dict(file_data: tuple) -> dict:
        return {
            "id": file_data[0],
            "filename": file_data[1],
            "size": file_data[2],
            "custom_name": file_data[3],
            "uploaded_at": round(file_data[4].timestamp())
        }

    @staticmethod
    def _fetch(conn: MySQLConnection, query: str, values: tuple = None) -> list:
        cursor = conn.cursor()
        cursor.execute(query, values)
        result = cursor.fetchall()
        cursor.close()

        return result

    @staticmethod
    def _fetchone(conn: MySQLConnection, query: str, values: tuple = None) -> tuple:
        cursor = conn.cursor()
        cursor.execute(query, values)
        result = cursor.fetchone()
        cursor.close()

        return result

    @staticmethod
    def convert_time(files: list[dict] | dict) -> list[dict] | dict:
        converted_files = []

        if isinstance(files, dict):
            files["uploaded_at"] = round(
                time.mktime(files["uploaded_at"].timetuple()))
            return files

        elif isinstance(files, list):
            for file in files:
                file["uploaded_at"] = round(
                    time.mktime(file["uploaded_at"].timetuple()))
                converted_files.append(file)

            return converted_files

    @staticmethod
    def add_file(db_config: dict, file: File) -> None:
        conn = DB._login(db_config)

        query = "INSERT INTO files (filename, size, custom_name, uploaded_at) VALUES (%s, %s, %s, %s)"
        values = (file.filename, file.size, file.custom_name,
                  datetime.utcfromtimestamp(file.uploaded_at))

        DB._execute(conn, query, values)

        DB._logout(conn)

    @staticmethod
    def get_files(db_config: dict) -> dict:
        conn = DB._login(db_config)

        query = "SELECT * FROM files ORDER BY uploaded_at DESC"

        result = DB._fetch(conn, query)

        DB._logout(conn)
        files = []
        for file in result:
            files.append(File("file_data", DB._make_file_dict(file)))

        return files

    @staticmethod
    def get_file(db_config: dict, file_id: int) -> dict | None:
        conn = DB._login(db_config)

        query = "SELECT * FROM files WHERE id = %s"
        values = (file_id,)

        result = DB._fetchone(conn, query, values)

        DB._logout(conn)

        if result is None:
            return None

        return File("file_data", DB._make_file_dict(result))
