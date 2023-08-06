# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utility methods for downloading files."""
from requests import ConnectionError, Timeout, TooManyRedirects, RequestException
from typing import List, Optional
from urllib.parse import urljoin
import hashlib
import logging
import os
import requests
import shutil
import time
import zipfile

from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.shared.exceptions import ClientException

logger = logging.getLogger(__name__)


class Downloader:
    """Helper class for assisting with generic file downloads."""

    @staticmethod
    def _is_download_needed(file_path: str, md5hash: Optional[str]) -> bool:
        """
        Delete as needed stuff at the file_path.

        :param file_path: File path to check and remove if needed.
        :param md5hash: md5hash of the expected file. Do not remove if the hash matches.
        :return: True if download is needed. False, otherwise.
        """
        if os.path.exists(file_path):
            if os.path.isdir(file_path):
                logger.info("Deleting a directory")
                shutil.rmtree(file_path)
            elif md5hash is not None and md5hash == Downloader.md5(file_path):
                logger.info("md5hash matched. No download necessary.")
                return False

        return True

    @classmethod
    def get_download_path(cls, file_name: str, target_dir: str, prefix: Optional[str] = None) -> str:
        """
        Build the path to which the specified file will be downloaded.

        :param file_name: File name requested.
        :param target_dir: Directory in which the file will be saved.
        :param prefix: Prefix corresponding to the class that has requested this download,
        to be prepended to the file_name.
        :return: Path to which we will try to download the file.
        """
        return os.path.join(target_dir, "{prefix}_{file_name}".format(prefix=prefix or '',
                                                                      file_name=file_name))

    @classmethod
    def download(cls, download_prefix: str, file_name: str, target_dir: str,
                 md5hash: Optional[str] = None, prefix: Optional[str] = None) -> Optional[str]:
        """
        Download the given url.

        :param download_prefix: Url to download from.
        :param file_name: File name requested in case of an archive.
        :param target_dir: Target directory in which we should download and store.
        :param md5hash: md5hash of the file being downloaded to prevent random files from getting downloaded.
        :param prefix: Prefix corresponding the class that has requested this download.
        :return: Path to the downloaded file name or None if the file doesn't exist or any failure.
        """
        download_path = Downloader.get_download_path(file_name=file_name,
                                                     target_dir=target_dir,
                                                     prefix=prefix)
        download_url = urljoin(download_prefix, file_name)

        # Clean up and check hash.
        if Downloader._is_download_needed(download_path, md5hash):
            try:
                hash_md5 = hashlib.md5()
                chunk_size = 10 * 1024 * 1024
                download_start_time = time.clock()
                with requests.get(download_url, stream=True) as r, open(download_path, 'wb') as fd:
                    if r.status_code != 404:
                        for chunk in r.iter_content(chunk_size):  # 10M
                            if chunk:
                                fd.write(chunk)
                                hash_md5.update(chunk)
                                fd.flush()
                        download_end_time = time.clock()

                        logger.info("Embeddings download time: {time_taken}".format(
                            time_taken=download_end_time - download_start_time))

                if md5hash and hash_md5.hexdigest() != md5hash:
                    error_message = "md5hash validation failed. This downloaded file will not be used " \
                                    "and will be removed."
                    logging_utilities.log_traceback(
                        ClientException(error_message),
                        logger,
                        is_critical=False
                    )
                    os.remove(download_path)
                    return None
            except (ConnectionError, Timeout, TooManyRedirects, RequestException):
                # Failed to download model
                exception_error_msg = "Download failed with error"
                logging_utilities.log_traceback(
                    ClientException(exception_error_msg),
                    logger,
                    override_error_msg=exception_error_msg,
                    is_critical=False
                )
                return None

        return download_path

    @classmethod
    def md5(cls, file_path: str) -> Optional[str]:
        """
        Calculate md5hash of the given file name if the path exists. Else, return None.

        :param file_path: Path to the file.
        :return: md5digest or None
        """
        if file_path is not None and os.path.exists(file_path):
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(65536), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        return None

    @classmethod
    def unzip_file(cls, zip_fname, extract_path):
        """
        Unzip the contents of the file, whose name is passed in

        :param zip_fname: name of the file to be un-zipped
        :param extract_path: path for the zipped folder to extracted to
        :return: Unzip the contents of the file, whose name is passed in
        """
        with zipfile.ZipFile(os.path.join(os.getcwd(), zip_fname), 'r') as zf:
            try:
                # Try around extracting.
                # The extractall() throws in a multinode context when using a shared filesystem
                zf.extractall(extract_path)
            except (IOError, OSError):
                msg = """Problem in extracting zip file in automl sdk file downloader.
                             In a distributed training context, this is expected to occur
                             for up to n_nodes - 1 times."""
                logger.warning(msg)
                pass
        return zf.filelist

    @staticmethod
    def get_zip_filelist(zip_fname: str) -> List[zipfile.ZipInfo]:
        """
        Get the list of files inside a zip archive without extracting them.

        :param zip_fname: The name of the file to be un-zipped.
        :return: The zipfile filelist.
        """
        with zipfile.ZipFile(os.path.join(os.getcwd(), zip_fname), 'r') as zf:
            return zf.filelist
