import os
import subprocess
from utils import read_lines, write_problem


PATH_TO_E = ""
PATH_TO_Vampire = ""


def run_E_prover(input_file, output_file, cpu_time):
    # run without selection
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
        '--cpu-limit=' + str(cpu_time),
        input_file],
        stdout=output, stderr=open(os.devnull, 'w'))
    output.close()


def run_Vampire_prover(input_file, output_file, cpu_time):
    # run without selection
    output = open(output_file, 'w+')
    subprocess.call([
        PATH_TO_Vampire,
        ' ',
        'casc',
        '--forced_options',
        'ss=off',
        '-t',
        str(cpu_time),
        input_file],
        stdout=output, stderr=open(os.devnull, 'w'))
    output.close()


def E_proof(thm, ranking, statements, s,
            cpu_time, problem_dir, output_dir):
    input_file = os.path.join(problem_dir, thm)
    output_file = os.path.join(output_dir, thm)
    write_problem(thm, ranking[:s], statements, input_file)
    run_E_prover(input_file, output_file, cpu_time)
    lines = read_lines(output_file)
    if "# Proof found!" in lines and "# SZS status Theorem" in lines:
        return True
    else:
        return False


def Vampire_proof(thm, ranking, statements, s,
                  cpu_time, problem_dir, output_dir):
    input_file = os.path.join(problem_dir, thm)
    output_file = os.path.join(output_dir, thm)
    write_problem(thm, ranking[:s], statements, input_file)
    run_Vampire_prover(input_file, output_file, cpu_time)
    lines = read_lines(output_file)
    if '% Refutation found. Thanks to Tanya!' in lines:
        return True
    else:
        return False


def E_proofs_from_ranking(thm, ranking, slice_list, statements,
                          problem_dir, output_dir):

    stop = False
    for s in slice_list:
        if len(ranking) <= s:
            s_index = slice_list.index(s)
            cpu_time = 10 * len(slice_list[s_index:])
            stop = E_proof(thm, ranking, statements, s,
                           cpu_time, problem_dir, output_dir)
            break
        else:
            cpu_time = 10
            stop = E_proof(thm, ranking, statements, s,
                           cpu_time, problem_dir, output_dir)
            if stop:
                break


def Vampire_proofs_from_ranking(thm, ranking, slice_list, statements,
                                problem_dir, output_dir):
    stop = False
    for s in slice_list:
        if len(ranking) <= s:
            s_index = slice_list.index(s)
            cpu_time = 10 * len(slice_list[s_index:])
            stop = Vampire_proof(thm, ranking, statements, s, cpu_time,
                                 problem_dir, output_dir)
            break
        else:
            cpu_time = 10
            stop = Vampire_proof(thm, ranking, statements, s, cpu_time,
                                 problem_dir, output_dir)
            if stop:
                break
