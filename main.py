def readFile(filename):  # returns an error message
    try:
        input = open(filename)
        content = input.readlines()
        input.close()
        return content
    except IOError:
        return IOError("file not found")


def seqs_dict(
    content,
):  # returns a dictionary from the fasta file and number of records in the file
    seqs = {}
    for line in content:
        line = line.rstrip()
        if line[0] == ">":
            words = line.split()
            name = words[0][1:]
            seqs[name] = ""
        else:
            seqs[name] = seqs[name] + line
    print("records number in file:", len(seqs.keys()))
    return seqs


def getMinMaxSequences(
    seqs,
):  # returns lengths of the sequences in the file, longest sequence, shortest sequence and their identifiers
    sequence_length = []
    for name in seqs:
        length = len(seqs[name])
        sequence_length.append(length)
    max_length = max(sequence_length)
    min_length = min(sequence_length)
    max_length_identifier = []
    min_length_identifier = []
    for name in seqs:
        if len(seqs[name]) == max_length:
            max_length_identifier.append(name)
        if len(seqs[name]) == min_length:
            min_length_identifier.append(name)
    return max_length_identifier, max_length, min_length_identifier, min_length


def orf_count(
    start_position, seqs
):  # returns orf with maximum length, its index and identifier.
    orfs_dict = {}
    for name in seqs:
        seq = seqs[name]
        i = start_position
        while i <= len(seq) - 3:
            codon = seq[i : i + 3]
            if codon == "ATG":
                j = i
                while j <= len(seq) - 3:
                    stop_codon = seq[j : j + 3]
                    if stop_codon in ["TAA", "TAG", "TGA"]:
                        orf = seq[i : j + 3]
                        orfs_dict[f"{name}_{i}"] = orf
                        break
                    j = j + 3
            i = i + 3
    max_length = 0
    for key, value in orfs_dict.items():
        length = len(value)
        if length > max_length:
            max_length = length
    for key, val in orfs_dict.items():
        if len(val) == max_length:
            return key, val, max_length


def repeat_pattern(n, seqs):  # returns pattern of length n that has max frequency
    pattern_dict = {}
    for key in seqs:
        seq = seqs[key]
        i = 0
        while i <= len(seq) - n:
            pattern = seq[i : i + n]
            pattern_dict[pattern] = pattern_dict.get(pattern, 0) + 1
            i = i + 1
    max_frequency = 0
    key = ""
    for pattern_key in pattern_dict:
        frequency_pattern = pattern_dict[pattern_key]
        if frequency_pattern > max_frequency:
            max_frequency = frequency_pattern
            key = pattern_key
    for pattern in pattern_dict:
        if pattern_dict[pattern] == max_frequency:
            return pattern, max_frequency


def main():
    content = ""
    try:
        content = readFile("input_file.fa")
    except IOError:
        print("Error in reading file: ")

    if len(content) == 0:
        print("Terminating program: no content in the file")
        return

    dict = seqs_dict(content)
    min_max_seq = getMinMaxSequences(dict)
    print(
        "max_length_identifier, max_length, min_length_identifier, min_length:",
        min_max_seq,
    )
    orf = orf_count(0, dict)
    print("seq identifier with max orf length_index, orf, length:", orf)
    frequent_pattern = repeat_pattern(7, dict)
    print("frequent occuring pattern of length n and its frequency:", frequent_pattern)


main()
