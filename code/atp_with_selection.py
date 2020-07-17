import os
import subprocess
from atp import run_E_prover, run_Vampire_prover
from utils import write_problem
from data_structure import Statements, Chronology, Problem_Order
from joblib import Parallel, delayed


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


def process(thm, statements, chronology, problem_dir,
            E_no_selection, E_selection,
            Vampire_no_selection, Vampire_selection):
    available_prems = chronology.available_premises(thm)
    problem_file = os.path.join(problem_dir, thm)
    write_problem(thm, available_prems, statements, problem_file)
    E_no_selection_file = os.path.join(E_no_selection, thm)
    run_E_prover(problem_file, E_no_selection_file, 60)
    Vampire_no_selection_file = os.path.join(Vampire_no_selection, thm)
    run_Vampire_prover(problem_file, Vampire_no_selection_file, 60)
    E_selection_file = os.path.join(E_selection, thm)
    run_E_prover_with_selection(problem_file, E_selection_file, 60)
    Vampire_selection_file = os.path.join(Vampire_selection, thm)
    run_Vampire_prover_with_selection(
        problem_file, Vampire_selection_file, 60)


if __name__ == "__main__":
    chronology = Chronology("../data/chronology")
    problem_order = Problem_Order("../data/ProblemsInMMLOrder")
    statements = Statements("../data/statements")
    problem_dir = "../problem/no_selection"
    E_no_selection = "../E_output/no_selection"
    Vampire_no_selection = "../Vampire_output/no_selection"
    E_selection = "../E_output/E_selection"
    Vampire_selection = "../Vampire_output/Vampire_selection"
    if not os.path.exists(problem_dir):
        os.mkdir(problem_dir)
    if not os.path.exists(E_no_selection):
        os.mkdir(E_no_selection)
    if not os.path.exists(Vampire_no_selection):
        os.mkdir(Vampire_no_selection)
    if not os.path.exists(E_selection):
        os.mkdir(E_selection)
    if not os.path.exists(Vampire_selection):
        os.mkdir(Vampire_selection)
    Parallel(n_jobs=4)(delayed(process)(thm, statements, chronology,
                                        problem_dir,
                                        E_no_selection, E_selection,
                                        Vampire_no_selection,
                                        Vampire_selection)
                       for thm in problem_order)
