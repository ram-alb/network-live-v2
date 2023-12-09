from network_live.beeline.huawei.lte import lte_main


def main(technology, physical_params):
    """
    Update Network Live with Beeline Huawei cells.

    Args:
        technology (str): A RAN technology (LTE, WCDMA, GSM and etc).
        physical_params (dict): A dictionary containing physical parameters.

    Returns:
        str: A Network Live update result.
    """
    main_funcs = {
        'LTE': lte_main,
    }

    main_func = main_funcs[technology]
    return main_func(physical_params)
