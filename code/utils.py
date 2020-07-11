import csv
import logging


def read_lines(file_path):
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()
    return lines


def write_problem(thm, ranking, statements, problem_file):
    with open(problem_file, "w+") as f:
        f.write(statements[thm].replace("axiom", "conjecture") + "\n")
        f.writelines("\n".join([statements[prem] for prem in ranking]))


def write_ranking_to_csv(prem2score, csv_file):
    with open(csv_file, "w+") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(prem2score)


def set_recorder(name, logfile):
    recorder = logging.getLogger(name)
    recorder.setLevel(logging.INFO)
    rf_handler = logging.StreamHandler()
    rf_handler.setLevel(logging.INFO)
    rf_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(message)s"))

    f_handler = logging.FileHandler(logfile)
    f_handler.setLevel(logging.INFO)
    f_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(message)s"))
    recorder.addHandler(rf_handler)
    recorder.addHandler(f_handler)
    return recorder
