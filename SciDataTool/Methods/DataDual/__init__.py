def is_freq(*args):
    """Determine if input args require FreqPart"""
    is_freq = False
    for arg in args:
        if "freqs" in arg or "wavenumber" in arg:
            is_freq = True
            break
    return is_freq
