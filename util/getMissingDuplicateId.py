def list_decrement(arr):
    idx = len(arr) - 1
    missing_ids = []
    duplicate_ids = []
    for i in range(idx, 0, -1):
        eval = int(arr[i]) - int(arr[i - 1])
        if eval > 1:
            for j in range(1, eval):
                missing_ids.append(int(arr[i]) - j)
        elif eval == 0:
            duplicate_ids.append(int(arr[i]))

    return missing_ids, duplicate_ids