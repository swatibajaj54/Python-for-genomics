import math


def readFile(filename):
    try:
        input = open(filename)
        content = input.readlines()
        input.close()
        return content
    except IOError:
        return IOError("file not found")


def getMinMaxSequences(content):
    seqs = {}
    for line in content:
        line = line.rstrip()
        if line[0] == ">":
            words = line.split()
            name = words[0][1:]
            seqs[name] = ""
        else:
            seqs[name] = seqs[name] + line

    # print("Number of sequences in input file is", len(seqs.keys()))
    sequence_length = []
    # max_length = 0
    # min_length = math.inf
    for name in seqs:
        length = len(seqs[name])
        sequence_length.append(length)
    #     if length > max_length:
    #         max_length = length
    #     if length < min_length:
    #         min_length = length
    # print(name, max_length)
    # print(name, min_length)
    max_length = max(sequence_length)
    min_length = min(sequence_length)
    max_length_identifier = []
    min_length_identifier = []
    for name in seqs:
        if len(seqs[name]) == max_length:
            max_length_identifier.append(name)
        if len(seqs[name]) == min_length:
            min_length_identifier.append(name)
    # print("sequence lengths is:", sequence_length)
    # print(
    #     "max length:",
    #     max_length,
    #     max_length_identifier,
    #     "min length:",
    #     min_length,
    #     min_length_identifier,
    # )
    return seqs


def orf_count(start_position, seqs):
    orfs_dict = {}
    for name in seqs:
        seq = seqs[name]
        i = start_position
        while i <= len(seq) - 3:
            codon = seq[i : i + 3]
            if codon == "ATG":
                text = seq[i : len(seq) - 3]
                indexOfTAA = text.find("TAA")
                indexOfTAG = text.find("TAG")
                indexOfTGA = text.find("TGA")
                endIndex = -1
                if indexOfTAA != -1:
                    endIndex = indexOfTAA
                elif indexOfTAG != -1:
                    endIndex = indexOfTAG
                elif indexOfTGA != -1:
                    endIndex = indexOfTGA

                if endIndex != -1:
                    orf = text[0 : endIndex + 3]
                    orfs_dict[f"{name}_{i}"] = orf
            i = i + 3
    print(orfs_dict)
    for name_index in orfs_dict:
        length = len(orfs_dict[name_index])
        max_length = 0
        if length > max_length:
            max_length = length
    for key, val in orfs_dict.items():
        if len(val) == max_length:
            print(key, val, max_length)


def main():
    content = ""
    try:
        content = readFile("input_file.fa")
    except IOError:
        print("Error in reading file: ")

    if len(content) == 0:
        print("Terminating program: no content in the file")
        return

    dict = getMinMaxSequences(content)
    orf_count(0, dict)


main()
