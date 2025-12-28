import dav_tools

def check_incompatibility(val1, err1, val2, err2):
    err_sqared_sum = err1**2 + err2**2
    sqrt = err_sqared_sum**0.5
    diff = abs(val1 - val2)

    # Check if the difference is greater than three times the combined standard deviation
    return diff > 3 * sqrt

if __name__ == '__main__':
    val1 = dav_tools.messages.ask('Value 1: ')
    err1 = dav_tools.messages.ask('Error 1: ')
    val2 = dav_tools.messages.ask('Value 2: ')
    err2 = dav_tools.messages.ask('Error 2: ')

    incompatible = check_incompatibility(float(val1), float(err1), float(val2), float(err2))
    if incompatible:
        dav_tools.messages.error('Incompatible.')
    else:
        dav_tools.messages.success('Compatible.')