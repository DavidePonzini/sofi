def check_incompatibility(val1, err1, val2, err2):
    err_sqared_sum = err1**2 + err2**2
    sqrt = err_sqared_sum**0.5
    diff = abs(val1 - val2)

    # Check if the difference is greater than three times the combined standard deviation
    return diff > 3 * sqrt