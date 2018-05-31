import re

def decimal(fmt, value):
    match = re.match(r'#\.(#+)', fmt)
    if match:
        precision = len(match.group(1))
        decimal_format = '%.' + str(precision) + 'f'
        return (decimal_format % value).rstrip('0').rstrip('.')
    else:
        return None
