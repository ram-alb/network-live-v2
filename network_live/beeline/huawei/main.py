from network_live.ftp import download_ftp_cm


def main(sharing_type):
    """
    Update Network Live db with data from Beeline Huawei cm files.

    Args:
        sharing_type (str): A type of RAN sharing technology (MORAN or MOCN)
    """
    operator = f'beeline_huawei_{sharing_type}'

    download_ftp_cm(operator)
