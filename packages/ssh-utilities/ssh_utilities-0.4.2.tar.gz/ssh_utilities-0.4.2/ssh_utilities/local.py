"""Module implementing local connection functionality.

Has the same API as remote version.
"""

import logging
import os
import shutil
import subprocess
from pathlib import Path
from socket import gethostname
from typing import IO, TYPE_CHECKING, List, Optional, Union

from typing_extensions import Literal

from .base import ConnectionABC
from .constants import C, G, R, Y
from .utils import context_timeit, file_filter, lprint

if TYPE_CHECKING:
    from .typeshed import _GLOBPAT, _SPATH, _CMD, _FILE, _ENV

__all__ = ["LocalConnection"]

logging.getLogger(__name__)


class LocalConnection(ConnectionABC):
    """Emulates SSHConnection class on local PC."""

    _osname: Literal["nt", "posix", "java", ""] = ""

    def __init__(self, address: Optional[str], username: str,
                 password: Optional[str] = None,
                 rsa_key_file: Optional[Union[str, Path]] = None,
                 line_rewrite: bool = True, server_name: Optional[str] = None,
                 quiet: bool = False, share_connection: int = 10) -> None:

        # set login credentials
        self.password = password
        self.address = address
        self.username = username
        self.rsa_key_file = rsa_key_file

        self.server_name = server_name if server_name else gethostname()
        self.server_name = self.server_name.upper()

        self.local = True

    def __str__(self) -> str:
        return self.to_str("LocalConnection", self.server_name, None,
                           self.username, None)

    @staticmethod
    def close(*, quiet: bool):
        """Close emulated local connection."""
        lprint(quiet)(f"{G}Closing local connection")

    @staticmethod
    def ssh_log(log_file="paramiko.log", level="WARN"):
        lprint()(f"{Y}Local sessions are not logged!")

    @staticmethod
    def run(args: "_CMD", *, suppress_out: bool, quiet: bool = True,
            bufsize: int = -1, executable: "_SPATH" = None,
            input: Optional[str] = None, stdin: "_FILE" = None,
            stdout: "_FILE" = None, stderr: "_FILE" = None,
            capture_output: bool = False, shell: bool = False,
            cwd: "_SPATH" = None, timeout: Optional[float] = None,
            check: bool = False, encoding: Optional[str] = None,
            errors: Optional[str] = None, text: Optional[bool] = None,
            env: Optional["_ENV"] = None,
            universal_newlines: Optional[bool] = None
            ) -> subprocess.CompletedProcess:

        if capture_output:
            stdout = subprocess.PIPE
            stderr = subprocess.PIPE

        out = subprocess.run(args, bufsize=bufsize, executable=executable,
                             input=input, stdin=stdin, stdout=stdout,
                             stderr=stderr, shell=shell, cwd=cwd,
                             timeout=timeout, check=check, encoding=encoding,
                             errors=errors, text=text,
                             universal_newlines=universal_newlines)

        if capture_output and not suppress_out:
            lprint(quiet)(f"{C}Printing local output\n{'-' * 111}{R}")
            lprint(quiet)(out.stdout)
            lprint(quiet)(f"{C}{'-' * 111}{R}\n")

        return out

    @staticmethod
    def copy_files(files: List[str], remote_path: "_SPATH",
                   local_path: "_SPATH", direction: str, quiet: bool = False):

        with context_timeit(quiet):
            for f in files:
                file_remote = Path(remote_path) / f
                file_local = Path(local_path) / f

                if direction == "get":
                    shutil.copy2(file_remote, file_local)
                elif direction == "put":
                    shutil.copy2(file_local, file_remote)
                else:
                    raise ValueError(f"{direction} is not valid direction. "
                                     f"Choose 'put' or 'get'")

    def download_tree(self, remote_path: "_SPATH", local_path: "_SPATH",
                      include: "_GLOBPAT" = None, exclude: "_GLOBPAT" = None,
                      remove_after: bool = True, quiet: bool = False):

        def _cpy(src: str, dst: str):
            if allow_file(src):
                shutil.copy2(src, dst)

        allow_file = file_filter(include, exclude)

        remote_path = self._path2str(remote_path)
        local_path = self._path2str(local_path)

        if remove_after:
            shutil.move(remote_path, local_path, copy_function=_cpy)
        else:
            shutil.copytree(remote_path, local_path, copy_function=_cpy)

    def upload_tree(self, local_path: "_SPATH", remote_path: "_SPATH",
                    include: "_GLOBPAT" = None, exclude: "_GLOBPAT" = None,
                    remove_after: bool = True, quiet: bool = False):

        self.download_tree(local_path, remote_path, include=include,
                           exclude=exclude, remove_after=remove_after,
                           quiet=quiet)

    @staticmethod
    def isfile(path: "_SPATH") -> bool:
        return os.path.isfile(path)

    @staticmethod
    def isdir(path: "_SPATH") -> bool:
        return os.path.isdir(path)

    def Path(self, path: "_SPATH") -> Path:
        return Path(self._path2str(path))

    @staticmethod
    def mkdir(path: "_SPATH", mode: int = 511, exist_ok: bool = True,
              parents: bool = True, quiet: bool = True):
        Path(path).mkdir(mode=mode, parents=parents, exist_ok=exist_ok)

    @staticmethod
    def rmtree(path: "_SPATH", ignore_errors: bool = False,
               quiet: bool = True):
        shutil.rmtree(path, ignore_errors=ignore_errors)

    @staticmethod
    def listdir(path: "_SPATH") -> List[str]:
        return os.listdir(path)

    @staticmethod
    def open(filename: "_SPATH", mode: str = "r",
             encoding: Optional[str] = None,
             bufsize: int = -1, errors: Optional[str] = None
             ) -> IO:
        encoding = encoding if encoding else "utf-8"
        errors = errors if errors else "strict"

        return open(filename, mode, encoding=encoding, errors=errors)

    @property
    def osname(self) -> Literal["nt", "posix", "java"]:
        if not self._osname:
            self._osname = os.name

        return self._osname

    # ! DEPRECATED
    @staticmethod
    def sendCommand(command: str, suppress_out: bool, quiet: bool = True):
        return subprocess.run([command], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE).stdout

    # for backawards compatibility
    sendFiles = copy_files  # type: ignore
    send_files = copy_files  # type: ignore
    downloadTree = download_tree
    uploadTree = upload_tree
