def percent_change(previous, current):
    if previous in (None, 0):
        return 0.0
    return ((current - previous) / previous) * 100
