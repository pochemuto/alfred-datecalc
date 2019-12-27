import re

def decimal(fmt, value):
    match = re.match(r'[#0]\.((#+|0+))$', fmt)
    if match:
        zeros = match.group(1)
        precision = len(zeros)
        decimal_format = '%.' + str(precision) + 'f'
        result = decimal_format % value
        if zeros[0] == '#':
            result = result.rstrip('0').rstrip('.')
        return result
    else:
        return None
