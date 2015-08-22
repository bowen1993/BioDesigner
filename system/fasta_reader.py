def read_fastas(fp):
    name, seq = None, []
    for line in fp:
        line = line.rstrip()
        if line.startswith(">"):
            line = line[1:]
            if name: yield (name, ''.join(seq))
            name, seq = line, []
        else:
            seq.append(line)
    if name: yield (name, ''.join(seq))

def parse_fasta_str(fasta_str):
    fasta_str_list = fasta_str.split('\n')
    res_dict = dict()
    for name, seq in read_fastas(fasta_str_list):
        res_dict[name] = seq
    return res_dict

def parse_fasta_file(fasta_filename):
    res_dict = dict()
    with open(fasta_filename) as fp:
        for name, seq in read_fasta(fp):
            res_dict[name] = seq
    return res_dict