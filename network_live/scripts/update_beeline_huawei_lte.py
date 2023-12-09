from dotenv import load_dotenv
from network_live.atoll.atoll import get_physical_params
from network_live.beeline.huawei.main import main as huawei_main

load_dotenv()


def main():
    """Update Network Live db with LTE Beeline Huawei data."""
    technology = 'LTE'
    physical_params = get_physical_params(technology)
    update_result = huawei_main(technology, physical_params)
    print(update_result)
