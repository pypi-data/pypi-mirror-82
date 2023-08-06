"""Template module for all connections classes."""
import logging
from abc import ABC, abstractmethod
from os import fspath
from pathlib import Path
from typing import IO, TYPE_CHECKING, List, Optional, Union

from typing_extensions import Literal

from .path import SSHPath

if TYPE_CHECKING:
    from .utils import CompletedProcess as CP
    from subprocess import CompletedProcess as sCP
    CompletedProcess = Union[CP, sCP]
    from paramiko.sftp_file import SFTPFile
    from .typeshed import _GLOBPAT, _SPATH, _CMD, _ENV, _FILE


__all__ = ["ConnectionABC"]

logging.getLogger(__name__)


class ConnectionABC(ABC):
    """Class defining API for connection classes."""

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def close(self, *, quiet: bool):
        pass

    @abstractmethod
    def ssh_log(self, log_file: Union[Path, str] = Path("paramiko.log"),
                level: str = "WARN"):
        pass

    @abstractmethod
    def run(self, args: "_CMD", *, suppress_out: bool, quiet: bool = True,
            bufsize: int = -1, executable: "_SPATH" = None,
            input: Optional[str] = None, stdin: "_FILE" = None,
            stdout: "_FILE" = None, stderr: "_FILE" = None,
            capture_output: bool = False, shell: bool = False,
            cwd: "_SPATH" = None, timeout: Optional[float] = None,
            check: bool = False, encoding: Optional[str] = None,
            errors: Optional[str] = None, text: Optional[bool] = None,
            env: Optional["_ENV"] = None,
            universal_newlines: Optional[bool] = None
            ) -> "CompletedProcess":
        pass

    @abstractmethod
    def copy_files(self, files: List[str], remote_path: "_SPATH",
                   local_path: "_SPATH", direction: str, quiet: bool = False):
        pass

    @abstractmethod
    def download_tree(self, remote_path: "_SPATH", local_path: "_SPATH",
                      include: "_GLOBPAT" = None, exclude: "_GLOBPAT" = None,
                      remove_after: bool = True, quiet: bool = False):
        pass

    @abstractmethod
    def upload_tree(self, local_path: "_SPATH", remote_path: "_SPATH",
                    include: "_GLOBPAT" = None, exclude: "_GLOBPAT" = None,
                    remove_after: bool = True, quiet: bool = False):
        pass

    @abstractmethod
    def isfile(self, path: "_SPATH") -> bool:
        pass

    @abstractmethod
    def isdir(self, path: "_SPATH") -> bool:
        pass

    @abstractmethod
    def Path(self, path: "_SPATH") -> Union[Path, SSHPath]:
        pass

    @abstractmethod
    def mkdir(self, path: "_SPATH", mode: int = 511, exist_ok: bool = True,
              parents: bool = True, quiet: bool = True):
        pass

    @abstractmethod
    def rmtree(self, path: "_SPATH", ignore_errors: bool = False,
               quiet: bool = True):
        pass

    @abstractmethod
    def listdir(self, path: "_SPATH") -> List[str]:
        pass

    @abstractmethod
    def open(self, filename: "_SPATH", mode: str = "r",
             encoding: Optional[str] = None,
             bufsize: int = -1, errors: Optional[str] = None
             ) -> Union[IO, "SFTPFile"]:
        pass

    @property
    @abstractmethod
    def osname(self) -> Literal["nt", "posix", "java"]:
        pass

    # Normal methods
    @staticmethod
    def _path2str(path: Optional["_SPATH"]) -> str:
        """Converts pathlib.Path, SSHPath or plain str to string.

        Also remove any rtailing backslashes.

        Parameters
        ----------
        path: "_SPATH"
            path to convert to string, if string is passed,
            then just returns it

        Raises
        ------
        FileNotFoundError
            if path is not instance of str, Path or SSHPath
        """
        if isinstance(path, (Path, SSHPath)):
            p = fspath(path)
            return p if not p.endswith("/") else p[:-1]
        elif isinstance(path, str):
            return path if not path.endswith("/") else path[:-1]
        else:
            raise FileNotFoundError(f"{path} is not a valid path")

    @staticmethod
    def to_str(connection_name: str, host_name: str, address: Optional[str],
               user_name: str, ssh_key: Union[Path, str]) -> str:
        """Aims to ease persistance, returns string representation of instance.

        With this method all data needed to initialize class are saved to sting
        and connection can be reinitialized with from_str method of
        `conection.Connection` class.

        Parameters
        ----------
        connection_name : str
            SSHConnection or LocalConnection
        host_name : str
            name of remote server
        address : str
            server address in case of remote connection
        user_name : str
            server login name
        ssh_key : Union[Path, str]
            file with public key

        Returns
        -------
        str
            string representation of the class

        See Also
        --------
        :class:`ssh_utilities.conncection.Connection`
        """
        ssh_key = Path(ssh_key)
        return (f"<{connection_name}:{host_name}>("
                f"user_name:{user_name} | "
                f"rsa_key:{str(ssh_key.resolve())} | "
                f"address:{address})")

    def __del__(self):
        self.close(quiet=True)

    # ! DEPRECATED
    def openSftp(self, quiet=False):
        """DEPRECATED METHOD !!!.

        Legacy method sftp is noe opened automatically when needed.

        See also
        --------
        :attr:`ssh_utilities.remote.SSHConnection.sftp` more recent implementation
        """
        pass

    sendFiles = copy_files
    send_files = copy_files
    downloadTree = download_tree
    uploadTree = upload_tree
