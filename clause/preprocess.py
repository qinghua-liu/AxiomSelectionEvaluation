import re
import sys

sys.path.append("../code")
from utils import read_lines


def extract_clause(input_file, output_file):
    lines = read_lines(input_file)
    clauses = [line for line in lines if "cnf" in line and "plain" in line]
    with open(output_file, "w+") as f:
        f.writelines("\n".join(clauses))


def extract_atom(line):
    pattern = re.compile(r"\||\~")
    raw_split = line.split(", plain,")
    name = raw_split[0].replace("cnf(", "")
    clause = raw_split[1].strip()[1: -3]
    raw_atoms = re.split(pattern, clause)
    atoms = []
    for atom in raw_atoms:
        if atom:
            if "=" in atom:
                args = atom.split("=")
                new_atom = "e(" + args[0] + "," + args[1] + ")"
                atoms.append(new_atom)
            elif "!=" in atom:
                args. atom.split("!=")
                new_atom = "e(" + args[0] + "," + args[1] + ")"
                atoms.append(new_atom)
            else:
                atoms.append(atom)
    print(atoms)


def extract_symbol(line):
    pattern = re.compile(r"\w+")
    raw_split = line.split(", plain,")
    name = raw_split[0].replace("cnf(", "")
    clause = raw_split[1].strip()[1: -3]
    symbols = re.findall(pattern, clause)
    functional_symbols = [
        sym for sym in symbols if re.match(r"[A-Z]", sym) is None]
    print(functional_symbols)


extract_symbol("cnf(i_0_855, plain, (12=k1_xboole_0|r2_hidden(X3,X2)|r2_hidden(X3,k3_subset_1(X1,X2))|~m1_subset_1(X3,X1)|~m1_subset_1(X2,k1_zfmisc_1(X1)))).")
