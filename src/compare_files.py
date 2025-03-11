def read_file(file_path):
    data = {}
    with open(file_path, 'r') as file:
        for line in file:
            if ',' in line:
                key, value = line.strip().split(',', 1)
                data[key] = value
    return data

def compare_files(file1, file2):
    data1 = read_file(file1)
    data2 = read_file(file2)

    all_keys = set(data1.keys()).union(set(data2.keys()))

    for key in all_keys:
        value1 = data1.get(key, None)
        value2 = data2.get(key, None)
        excluded_terms = ["SIM", "OSD"]

        if value1 != value2:
            if value1 is None:
                # print(f"{key} only in {file2}: {value2}")
                pass
            elif value2 is None:
                if any(term in key for term in excluded_terms):
                    # print(f"{key} only in {file1}: {value1}")
                    print(f"{key},{value1}")
                pass
            else:
                # print(f"{key} differs: {file1}={value1}, {file2}={value2}")
                pass

if __name__ == "__main__":
    file1 = "default.param"
    file2 = "full_params_heavy_shot.param"
    compare_files(file1, file2)
