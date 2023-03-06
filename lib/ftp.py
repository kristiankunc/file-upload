from io import BytesIO
from ftplib import FTP

from lib.file import File


class UploadFtp():
    @staticmethod
    def _login(ftp_config: dict) -> FTP:
        ftp = FTP(
            host=ftp_config["host"],
            user=ftp_config["user"],
            passwd=ftp_config["password"],
        )
        ftp.cwd(ftp_config["directory"])

        return ftp

    @staticmethod
    def _logout(ftp) -> None:
        ftp.quit()

    @staticmethod
    async def upload(ftp_config: dict, file: File, filename: str) -> None:
        ftp = UploadFtp._login(ftp_config)

        f = BytesIO(await file.read())

        ftp.storbinary(f"STOR {filename}", f)

        ftp.quit()

    @staticmethod
    def download(ftp_config: dict, filename: str) -> BytesIO:
        ftp = UploadFtp._login(ftp_config)

        f = BytesIO()

        ftp.retrbinary(f"RETR {filename}", f.write)

        ftp.quit()

        return f
