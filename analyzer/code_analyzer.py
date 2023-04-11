from vendor.static_code_analyzer.evaluator import evaluator_yield
import argparse
import os
parser = argparse.ArgumentParser(
    prog='Static code analyzer',
    description='Static code analyzer')

parser.add_argument('dir')

args = parser.parse_args()
os.chdir('/home/majcher/PycharmProjects/Static Code Analyzer/Static Code Analyzer/task')
directory = args.dir
# directory = '/home/majcher/PycharmProjects/Static Code Analyzer/Static Code Analyzer/task/test/this_stage/test_3.py'

for msg in evaluator_yield(directory):
    if len(msg):
        print(*msg, sep='\n')
