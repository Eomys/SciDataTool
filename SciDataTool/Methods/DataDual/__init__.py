def is_freq(*args):
    """Determine if input args require FreqPart"""
    is_freq = False
    if len(args) == 1 and type(args[0]) == tuple:
        args = args[0]  # if called from another script with *args
    for arg in args:
        if "freqs" in arg or "wavenumber" in arg:
            is_freq = True
            break
    return is_freq
