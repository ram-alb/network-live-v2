from dotenv import load_dotenv
from network_live.beeline.huawei.main import main as huawei_main

load_dotenv()


def main():
    """Update Network Live db with LTE Beeline Huawei data."""
    huawei_main('moran')
