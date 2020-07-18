import os
import subprocess
from atp import run_E_prover, run_Vampire_prover
from utils import write_problem
from data_structure import Statements, Chronology, Problem_Order
from joblib import Parallel, delayed
from tqdm import tqdm


PATH_TO_E = "/exp/home/tptp/Systems/E---2.5/eprover"
PATH_TO_Vampire = "/exp/home/tptp/Systems/Vampire---4.5/vampire"

def run_E_prover_with_selection(input_file, output_file, cpu_time):

    output = open(output_file, 'w+')
    subprocess.call([
        PATH_TO_E,
        '--delete-bad-limit=2000000000',
        '--definitional-cnf=24',
        '-s',
        '--print-statistics',
        '-R',
        '--print-version',
        '--free-numbers',
        '--proof-object',
        '--satauto-schedule',
        '--sine',
        '--cpu-limit=' + str(cpu_time),
        input_file],
        stdout=output, stderr=open(os.devnull, 'w'))
    output.close()


def run_Vampire_prover_with_selection(input_file, output_file, cpu_time):
    output = open(output_file, 'w+')
    subprocess.call([
        PATH_TO_Vampire,
        '--mode',
        'casc',
        '--forced_options',
        'ss=axioms:sd=1',
        '-t',
        str(cpu_time),
        input_file],
        stdout=output, stderr=open(os.devnull, 'w'))
    output.close()


def run_Vampire_prover_with_only_selection(input_file, output_file):
    output = open(output_file, "w+")
    subprocess.call([
        PATH_TO_Vampire,
        "--mode",
        "axiom_selection",
        "--output_axiom_names",
        "on",
        input_file],
        stdout=output, stderr=open(os.devnull, "w"))


def run_E_prover_with_only_selection(input_file, output_file):
    output = open(output_file, "w+")
    subprocess([
        PATH_TO_E,
        "--sine=Auto",
        "--tstp-format",
        "—prune",
        input_file],
        stdout=output, stderr=open(os.devnull, "w"))


def process(thm, problem_dir,
            selected_problem_dir, output_dir):
    input_file = os.path.join(problem_dir, thm)
    selected_file = os.path.join(selected_problem_dir, thm)
    run_Vampire_prover_with_only_selection(input_file, selected_file)
    output_file = os.path.join(output_dir, thm)
    run_E_prover(selected_file, output_file, 60)


if __name__ == "__main__":
    problem_order = Problem_Order("../data/ProblemsInMMLOrder")
    problem_dir = "../problem/no_selection"
    selected_problem_dir = "../problem/Vampire_selection"
    output_dir = "../E_output/Vampire_selection"

    if not os.path.exists(selected_problem_dir):
        os.mkdir(selected_problem_dir)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    Parallel(n_jobs=10)(delayed(process)(thm, problem_dir,
                                         selected_problem_dir,
                                         output_dir)
                        for thm in tqdm(problem_order))
