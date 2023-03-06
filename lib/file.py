import time
import pprint
from datetime import datetime
from starlette.datastructures import FormData


class File():
    def __init__(self, type: str, data: FormData | dict):
        self.id: int = 0
        self.custom_name: str = ""
        self.file = None
        self.filename: str = ""
        self.uploaded_at: int = 0
        self.size: int = 0

        if type == "form_data":
            self.__form_init(data)

        elif type == "file_data":
            self.__dict_init(data)

    def __form_init(self, form_data: FormData) -> None:
        self.custom_name = form_data["filename"]
        self.file = form_data["file"]
        self.uploaded_at = round(
            time.mktime(datetime.now().timetuple()))
        self.filename = self._gen_filename()

    def __dict_init(self, file_data: dict) -> None:
        self.id = file_data["id"]
        self.custom_name = file_data["custom_name"]
        self.filename = file_data["filename"]
        self.uploaded_at = file_data["uploaded_at"]
        self.size = file_data["size"]

    async def _calc_size(self) -> int:
        self.size = len(await self.file.read())
        await self.file.seek(0)
        return self.size

    def _gen_filename(self) -> str:
        name, extension = self.file.filename.split(".")
        return f"{name}_{datetime.utcfromtimestamp(self.uploaded_at).strftime('%Y-%m-%d_%H-%M-%S')}.{extension}"

    async def save(self, db_config: dict, ftp_config: dict) -> None:
        from lib.ftp import UploadFtp
        from lib.db import DB

        print(self.file)
        await UploadFtp.upload(ftp_config, self.file, self.filename)
        DB.add_file(db_config, self)

    def __str__(self) -> str:
        return pprint.pformat(self.__dict__, indent=4)
