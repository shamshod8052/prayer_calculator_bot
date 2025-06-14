def insert_values_every_n(lst, n, value):
    result = []
    for i in range(0, len(lst), n):
        result.append(value)
        result.extend(lst[i:i + n])

    return result
