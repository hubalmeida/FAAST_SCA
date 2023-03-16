"""Mock file"""

def raw_data() -> dict:
    """
    Function to mock data.
    :return: Dict  data
    """
    data = {
        'unit': ['YR'] * 3,
        'sex': ['F'] * 3,
        'age': ['Y1'] * 3,
        'geo\time': ['AM', 'AL', 'PT'],
        '2021': [79.4, 80.4, 80.2],
        '2020': [79.1, 79.2, 78.5],
        '2019': [82.9, 83.5, 83.3]
    }
    return data


def expect_data() -> dict:
    """
    Function to mock data.
    :return: Dict  data
    """
    data = {
        'unit': ['YR'] * 3,
        'sex': ['F'] * 3,
        'age': ['Y1'] * 3,
        'region': ['PT'] * 3,
        'year': [2021, 2020, 2019],
        'value': [80.2, 78.5, 83.3]
    }
    return data