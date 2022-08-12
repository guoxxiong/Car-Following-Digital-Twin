def pkgSize(pkgID, flag, ElementNum = 1, ExSize = 0):
    if pkgID == 1 or pkgID == 2:
        return 0
    elif pkgID == 9:
        if flag == 0:
            return 112 * ElementNum
        elif flag == 1:
            return 200 * ElementNum
    elif pkgID == 25:
        return 12
    elif pkgID == 27:
        if flag == 0:
            return 12 * ElementNum
        elif flag == 1:
            return 50 * ElementNum
    elif pkgID == 28:
        return 16 * ElementNum
    elif pkgID == 33:
        return 136 + ExSize
    else:
        return 0