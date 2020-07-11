import os
import subprocess
from utils import read_lines, write_problem


PATH_TO_E = '/Users/liuqinghua/Downloads/E/PROVER/eprover'

def run_E_prover(input_file, output_file, cpu_time):

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


def proofs_from_ranking(thm, prem2score, statements,
                        problem_dir, output_dir, recorder):

    slice_list = [32, 64, 128, 256, 512, 1024]
    ranking = [pair[0] for pair in prem2score]
    stop = False
    for s in slice_list:
        if len(ranking) <= s:
            s_index = slice_list.index(s)
            cpu_time = 10 * len(slice_list[s_index:])
            stop = E_proof(thm, ranking, statements, s,
                           cpu_time, problem_dir, output_dir)
            if stop:
                message = '{} :Proof is FOUND with {} premises.'.format(
                    thm, s)
            else:
                message = \
                    '{}: Proof is NOT found with {} premises.'.format(
                        thm, s)
            recorder.info(message)
            break
        else:
            cpu_time = 10
            stop = E_proof(thm, ranking, statements, s,
                           cpu_time, problem_dir, output_dir)
            if stop:
                message = '{}: Proof is FOUND with {} premises.'.format(
                    thm, s)
                recorder.info(message)
                break
    else:
        message = '{}: Proof is NOT found with {} premises.'.format(
            thm, s)
        recorder.info(message)
