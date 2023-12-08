from lxml import etree


def get_tag(root, tag_name):
    """
    Find the first occurrence of a specific XML tag within the given XML tree.

    Args:
        root (etree.Element): The root element of the XML tree.
        tag_name (str): The name of the XML tag to search for.

    Returns:
        str or None: The tag of the first occurrence of the specified tag_name,
            or None if the tag is not found.
    """
    for elem in root.iter():
        if not isinstance(elem, (etree._Comment, etree._ProcessingInstruction)):
            local_name = etree.QName(elem).localname
        if local_name == tag_name:
            return elem.tag


def parse_descendant_text(ancestor, descendant):
    """
    Parse the text content of a specific descendant element within an XML tree.

    Args:
        ancestor (etree.Element): The ancestor element from which to start searching.
        descendant (str): The name of the descendant element whose text content is to be retrieved.

    Returns:
        str or None: The text content of the specified descendant element,
            or None if the element or its text content is not found.
    """
    namespace = etree.QName(ancestor).namespace
    if namespace is not None:
        return ancestor.find(f'.//{{{namespace}}}{descendant}').text
    return ancestor.find(f'.//{descendant}').text


def get_cell_physical_params(cell_name, physical_params):
    """
    Retrieve physical parameters for an LTE cell based on its name.

    Args:
        cell_name (str): The name of the LTE cell.
        physical_params (dict): A dictionary containing physical parameters for various LTE cells.

    Returns:
        dict: A dictionary containing physical parameters (azimuth, height, longitude, latitude).
            If the cell_name is not found in physical_params, default values are returned.
    """
    try:
        cell_physical_params = physical_params[cell_name]
    except KeyError:
        cell_physical_params = {
            'azimut': None,
            'height': None,
            'longitude': None,
            'latitude': None,
        }
    return cell_physical_params
