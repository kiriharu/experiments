import argparse
import os
import posixpath

from paramiko.client import SSHClient, AutoAddPolicy
from paramiko.sftp_attr import SFTPAttributes
from paramiko.sftp_client import SFTPClient


class BackupDownloader:
    last_backup_info_file = ".last_backup_info"

    def __init__(
            self,
            sftp: SFTPClient,
            last_backup_time: int,
            remote_backup_dir: str,
            local_backup_dir: str
    ):
        self.sftp = sftp
        self.last_backup_time = last_backup_time
        self.remote_backup_dir = remote_backup_dir
        self.local_backup_dir = local_backup_dir
        self._prev_percent = 0

    @classmethod
    def init(
            cls,
            hostname: str,
            port: int,
            username: str,
            password: str,
            remote_backup_dir: str = "backups",
            local_backup_dir: str = "backups",
    ) -> "BackupDownloader":
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(
            hostname=hostname,
            port=port,
            username=username,
            password=password, 
            allow_agent=False,
            look_for_keys=False
        )

        last_backup_time = 0

        if not os.path.exists(cls.last_backup_info_file):
            print(f"WARNING: File {cls.last_backup_info_file} not found creating")
            open(cls.last_backup_info_file, "w").close()
        else:
            with open(cls.last_backup_info_file, "r") as f:
                last_time = f.readline()
                if not last_time:
                    print(f"INFO: File {cls.last_backup_info_file} found, but not have last backup time")
                else:
                    print(f"INFO: File {cls.last_backup_info_file} found, last backup time = {last_time}")
                    last_backup_time = int(last_time)

        if not os.path.exists(local_backup_dir):
            print(f"WARNING: Local backup dir {local_backup_dir} not exists, create...")
            os.makedirs(local_backup_dir)

        return cls(
            sftp=client.open_sftp(),
            last_backup_time=last_backup_time,
            remote_backup_dir=remote_backup_dir,
            local_backup_dir=local_backup_dir
        )

    @property
    def _last_backup_file(self) -> SFTPAttributes:
        return list(self.sftp.listdir_attr(self.remote_backup_dir))[-1]

    def _write_last_backup_time(self, time: int):
        with open(self.last_backup_info_file, "w") as f:
            f.write(str(time))

    def _write_status(self, fetched: int, total: int):
        one_percent = total / 100
        percent = fetched / one_percent
        if int(percent) > self._prev_percent:
            print(f"INFO: Download... {fetched}/{total} bytes, {int(percent)}%")
            self._prev_percent = percent

    def execute(self):
        backup_file = self._last_backup_file
        if backup_file.st_mtime <= self.last_backup_time:
            print(
                f"INFO: Last backup on server = {backup_file.st_mtime}, on local = {self.last_backup_time}, "
                f"no backup need"
            )
            return

        print(f"INFO: Getting file {backup_file.filename}")
        self.sftp.get(
            # SFTP use posix-like path
            posixpath.join(self.remote_backup_dir, backup_file.filename),
            os.path.join(self.local_backup_dir, backup_file.filename),
            callback=self._write_status
        )
        print(f"INFO: Writing backup time = {backup_file.st_mtime}")
        self._write_last_backup_time(backup_file.st_mtime)
        print("Done!")

    def __del__(self):
        self.sftp.close()


def main():
    parser = argparse.ArgumentParser(
        description="Download backups from sftp server"
    )
    parser.add_argument("hostname", type=str, help="SFTP Hostname")
    parser.add_argument("port", type=int, help="SFTP port")
    parser.add_argument("username", type=str, help="SFTP username")
    parser.add_argument("password", type=str, help="SFTP password")

    parser.add_argument(
        "remote_backup_dir", type=str, help="Remote backup dir where script will search for files", default="backups"
    )
    parser.add_argument(
        "local_backup_dir", type=str, help="Local dir where backups will be stored", default="backups"
    )

    args = parser.parse_args()

    backup_downloader = BackupDownloader.init(
        hostname=args.hostname,
        port=args.port,
        username=args.username,
        password=args.password,
        remote_backup_dir=args.remote_backup_dir,
        local_backup_dir=args.local_backup_dir
    )

    backup_downloader.execute()


if __name__ == "__main__":
    main()
