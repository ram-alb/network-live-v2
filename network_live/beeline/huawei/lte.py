import os
from datetime import date

from lxml import etree
from network_live.atoll.atoll import update_network_live
from network_live.beeline.huawei.huawei_utils import (
    get_cell_physical_params,
    get_tag,
    parse_descendant_text,
)
from network_live.ftp import download_ftp_cm

max_moran_cell_id = 131

cell_id_ranges = {
    'moran': range(100, max_moran_cell_id),
    'mocn': range(100),
}


class Tag(object):
    """Container for XML tag names used in LTE configuration management parsing."""

    # eNodeB ID tags
    enodeb_function = 'eNodeBFunction'
    enodeb_id = 'eNodeBId'
    # RBS name tags
    ne = 'NE'
    ne_name = 'NENAME'
    # S1 IP tags
    dev_ip = 'DEVIP'
    user_label = 'USERLABEL'
    ip = 'IP'
    # TAC tags
    cn_operator_ta = 'CnOperatorTa'
    tracking_area_id = 'TrackingAreaId'
    tac = 'Tac'
    # qRxLevMin tags
    cell_sel = 'CellSel'
    local_cell_id = 'LocalCellId'
    qrx_lev_min = 'QRxLevMin'
    # cell level tags
    cell = 'Cell'
    cell_active_state = 'CellActiveState'


def parse_cell_params(root, sharing_type):
    """
    Parse LTE cell parameters from an XML tree based on a specified sharing type.

    Args:
        root (etree.Element): The root element of the XML tree.
        sharing_type (str): The type of sharing to consider during parsing.

    Returns:
        list: A list of dictionaries representing parsed LTE cell parameters.
    """
    admin_states = {
        '0': 'LOCKED',
        '1': 'UNLOCKED',
    }
    cell_params = [
        ('cellId', 'LocalCellId'),
        ('cell_name', 'CellName'),
        ('earfcndl', 'DlEarfcn'),
        ('rachRootSequence', 'RootSequenceIdx'),
        ('physicalLayerCellId', 'PhyCellId'),
    ]

    cells = []
    for elem in root.iter(get_tag(root, Tag.cell)):
        cell = {
            param_key: parse_descendant_text(elem, cell_parameter)
            for param_key, cell_parameter in cell_params
        }
        cell['administrativeState'] = admin_states[
            parse_descendant_text(elem, Tag.cell_active_state)
        ]
        cell['oss'] = 'Beeline Huawei'
        cell['subnetwork'] = 'Beeline'
        cell['vendor'] = 'Huawei'
        cell['cellRange'] = None
        cell['primaryPlmnReserved'] = None
        cells.append(cell)

    return list(
        filter(
            lambda cell: int(cell['cellId']) in cell_id_ranges[sharing_type],
            cells,
        ),
    )


def parse_qrxlevmin(root, sharing_type):
    """
    Parse QRxLevMin values for LTE cells from an XML tree based on a specified sharing type.

    Args:
        root (etree.Element): The root element of the XML tree.
        sharing_type (str): The type of sharing to consider during parsing.

    Returns:
        dict: A dictionary mapping cell IDs to their respective QRxLevMin values.
    """
    qrxlevmins = {}

    for elem in root.iter(get_tag(root, Tag.cell_sel)):
        cell_id = parse_descendant_text(elem, Tag.local_cell_id)
        qrxlevmin = parse_descendant_text(elem, Tag.qrx_lev_min)
        if int(cell_id) in cell_id_ranges[sharing_type]:
            qrxlevmins[cell_id] = qrxlevmin

    return qrxlevmins


def parse_tac(root, sharing_type):
    """
    Parse Tracking Area Codes (TACs) from an XML tree based on a specified sharing type.

    Args:
        root (etree.Element): The root element of the XML tree.
        sharing_type (str): The type of sharing to consider during parsing.

    Returns:
        str or None: The Tracking Area Code (TAC) based on the specified sharing type,
            or None if the TAC is not found or sharing_type is not recognized.
    """
    tacs = {}
    for elem in root.iter(get_tag(root, Tag.cn_operator_ta)):
        tracking_area_id = parse_descendant_text(elem, Tag.tracking_area_id)
        tac = parse_descendant_text(elem, Tag.tac)
        tacs[tracking_area_id] = tac

    if sharing_type == 'moran':
        return tacs['1']
    elif sharing_type == 'mocn':
        return tacs['0']


def parse_s1_ip(root):
    """
    Parse the S1 IP address from an XML tree based on specific criteria.

    Args:
        root (etree.Element): The root element of the XML tree.

    Returns:
        str or None: The S1 IP address if the specified criteria are met,
            or None if the IP address is not found.
    """
    for elem in root.iter(get_tag(root, Tag.dev_ip)):
        user_label = parse_descendant_text(elem, Tag.user_label)
        if 'kcell' in user_label.lower():
            return parse_descendant_text(elem, Tag.ip)


def parse_rbs_level_parameter(root, ancestor, descendant):
    """
    Parse a parameter value within a specific XML in RBS level.

    Args:
        root (etree.Element): The root element of the XML tree.
        ancestor (str): The name of the ancestor node.
        descendant (str): The name of the descendant node containing the parameter value.

    Returns:
        str or None: The text content of the specified descendant node,
            or None if the element or its text content is not found.
    """
    tag_value = get_tag(root, ancestor)
    tag = root.find(f'.//{tag_value}')
    return parse_descendant_text(tag, descendant)


def calculate_eci(cell_id, enodeb_id):
    """
    Calculate the ECI (E-UTRAN Cell Identity) based on cell and eNodeB identifiers.

    Args:
        cell_id (str): The identifier of the LTE cell.
        enodeb_id (str): The identifier of the eNodeB (E-UTRAN NodeB).

    Returns:
        int: The calculated ECI.
    """
    eci_factor = 256
    int_cell_id = int(cell_id)
    int_enodeb_id = int(enodeb_id)
    return int_enodeb_id * eci_factor + int_cell_id


def parse_xml(xml_path, sharing_type, physical_params):
    """
    Parse an XML configuration management file for LTE (Long-Term Evolution) cells.

    Args:
        xml_path (str): The path to the XML configuration management file.
        sharing_type (str): The type of sharing to consider during parsing, e.g., 'moran', 'mocn'.
        physical_params (dict): A dictionary containing physical parameters.

    Returns:
        list: A list of dictionaries representing parsed LTE cells.
    """
    root = etree.parse(xml_path).getroot()
    try:
        cell_params = parse_cell_params(root, sharing_type)
    except AttributeError:
        return []
    qrxlevmins = parse_qrxlevmin(root, sharing_type)

    lte_cells = []
    for cell in cell_params:
        cell_id = cell['cellId']
        cell_physical_params = get_cell_physical_params(
            cell['cell_name'],
            physical_params,
        )
        lte_cell = {**cell, **cell_physical_params}
        lte_cell['qRxLevMin'] = qrxlevmins[cell_id]
        lte_cell['tac'] = parse_tac(root, sharing_type)
        lte_cell['ip_address'] = parse_s1_ip(root)
        lte_cell['enodeb_id'] = parse_rbs_level_parameter(
            root,
            Tag.enodeb_function,
            Tag.enodeb_id,
        )
        lte_cell['site_name'] = parse_rbs_level_parameter(
            root,
            Tag.ne,
            Tag.ne_name,
        )
        lte_cell['eci'] = calculate_eci(cell_id, lte_cell['enodeb_id'])
        lte_cell['insert_date'] = date.today()
        lte_cells.append(lte_cell)

    return lte_cells


def parse_lte_cms(xmls_path, sharing_type, physical_params):
    """
    Parse LTE (Long-Term Evolution) configuration management files.

    Args:
        xmls_path (str): The path to the folder containing XML configuration management files.
        sharing_type (str): The type of sharing to consider during parsing, e.g., 'moran', 'mocn'.
        physical_params (dict): A dictionary containing physical parameters.

    Returns:
        list: A list of dictionaries representing parsed LTE cells.
    """
    cells = []
    for cm_file in os.listdir(xmls_path):
        xml_path = os.path.join(xmls_path, cm_file)
        cells.extend(parse_xml(xml_path, sharing_type, physical_params))
    return cells


def lte_main(physical_params):
    """
    Update Network Live with Beeline Huawei LTE cells.

    Args:
        physical_params (dict): A dictionary containing physical parameters.

    Returns:
        str: A Network Live update result.
    """
    xmls_path = download_ftp_cm('beeline_huawei_moran')
    lte_cells = parse_lte_cms(xmls_path, 'moran', physical_params)

    xmls_path = download_ftp_cm('beeline_huawei_mocn')
    lte_cells.extend(parse_lte_cms(xmls_path, 'mocn', physical_params))

    return update_network_live(lte_cells, 'Beeline Huawei', 'LTE')
