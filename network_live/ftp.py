import os
from datetime import datetime, timedelta
from zipfile import ZipFile

import paramiko


def download_ftp_data(remote_path, local_path, ftp_type):
    """
    Download data from a remote server via FTP and saves it locally.

    Args:
        remote_path (str): The path to the file on the remote server.
        local_path (str): The local path where the downloaded file will be saved.
        ftp_type (str): The type of FTP server ('ftp_server' or 'oss').
    """
    if ftp_type == 'ftp_server':
        host = os.getenv('FTP_HOST')
        login = os.getenv('FTP_LOGIN')
        password = os.getenv('FTP_PASSWORD')
    elif ftp_type == 'oss':
        host = os.getenv('ASTOSS_HOST')
        login = os.getenv('ASTOSS_USER')
        password = os.getenv('ASTOSS_PASSWORD')

    with paramiko.Transport((host)) as transport:
        transport.connect(username=login, password=password)
        with paramiko.SFTPClient.from_transport(transport) as sftp:
            sftp.get(remote_path, local_path)


def get_cm_path_date(operator):
    """
    Retrieve the Configuration Management (CM) file path and date for the specified operator.

    Args:
        operator (str): The operator for which to retrieve CM information ('tele2' or 'beeline').

    Returns:
        tuple: A tuple containing the CM file path and formatted date.
    """
    cms_path = {
        'tele2': 'cm_files/tele2',
        'beeline': 'cm_files/beeline',
    }

    date_formats = {
        'tele2': '%Y%m%{d}'.format(d='d'),
        'beeline': '%{d}.%m.%Y'.format(d='d'),
    }

    now = datetime.now()
    date_format = date_formats[operator]
    date = (now - timedelta(days=2)).strftime(date_format)

    return cms_path[operator], date


def delete_old_files(files_path):
    """
    Delete files from a given directory.

    Args:
        files_path (str): A directory path from where need to delete files
    """
    files = os.listdir(files_path)

    if files:
        for file_item in files:
            os.remove(os.path.join(files_path, file_item))


def unzip_cm_file(zipfile_path):
    """
    Unzip a cm file from the specified ZIP archive.

    Args:
        zipfile_path (str): The path to the ZIP archive containing the log file.
    """
    zipfile_name = os.path.splitext(os.path.basename(zipfile_path))[0]
    zipfile_dir = os.path.dirname(zipfile_path)

    with ZipFile(zipfile_path, 'r') as zip_obj:
        if 'result_data' in zipfile_name:
            date = zipfile_name.split('_')[-1]
            filename = f'result_data_{date}.csv'
            zip_obj.extract(
                filename,
                zipfile_dir,
            )
            os.rename(
                os.path.join(zipfile_dir, filename),
                os.path.join(zipfile_dir, 'tele2_lte_log.csv'),
            )
        else:
            zip_obj.extractall(zipfile_dir)


def download_ftp_cm(cm_label, is_unzip=True):
    """
    Download the Configuration Management (CM) files from an FTP server for a specified operator.

    Args:
        cm_label (str): The label which spicify which cm files should be downloaded.
        is_unzip (bool, optional): Flag indicating whether to unzip the downloaded file.

    Returns:
        str: The local path where the CM files are downloaded.
    """
    if 'tele2' in cm_label:
        local_cm_path, date = get_cm_path_date('tele2')
    elif 'beeline' in cm_label:
        local_cm_path, date = get_cm_path_date('beeline')

    delete_old_files(local_cm_path)

    ftp_cm_paths = {
        'beeline_huawei_moran': f'/reporter/beeline/cm/LTE/{date}.zip',
        'beeline_huawei_mocn': f'/reporter/beeline/mocn/cm/LTE/{date}.zip',
    }

    remote_path = ftp_cm_paths[cm_label]
    local_path = os.path.join(local_cm_path, os.path.basename(remote_path))

    download_ftp_data(remote_path, local_path, 'ftp_server')

    if is_unzip:
        unzip_cm_file(local_path)
        os.remove(local_path)

    return local_cm_path
