"""Selected evaluator functions on fixed offline fixtures; no benchmark or model execution.

Functions are extracted from pinned upstream inputs using AST. Package initialization,
providers, filesystem access and external services are not executed. Service and file
reads for the selected CSV check are replaced with an in-memory fixed input.
"""
import ast
import copy
import csv
import io
import json
from pathlib import Path
from types import SimpleNamespace

BASE = Path(__file__).resolve().parents[1]

def function(path, name, class_name=None, namespace=None):
    tree = ast.parse(path.read_text())
    body = tree.body
    if class_name:
        body = next(x for x in body if isinstance(x, ast.ClassDef) and x.name == class_name).body
    node = copy.deepcopy(next(x for x in body if isinstance(x, ast.FunctionDef) and x.name == name))
    node.decorator_list = []
    for arg in node.args.args:
        arg.annotation = None
    node.returns = None
    unit = ast.fix_missing_locations(ast.Module(body=[node], type_ignores=[]))
    ns = {} if namespace is None else namespace.copy()
    exec(compile(unit, str(path), 'exec'), ns)
    return ns[name]

class EdgeGraph:
    nodes = [0, 1]
    edges = [(0, 1)]
    def order(self):
        return 2
    def number_of_edges(self):
        return 1

source = BASE / 'inputs/agentsnet--LiteralMessagePassing.py'
graph = EdgeGraph()
consensus = function(source, 'get_score', 'Consensus')
cover = function(source, 'score_vertex_cover')
report = {
    'scope': 'SCRIPTED FIXTURES — NOT MODEL EVIDENCE. Extracted scorer functions only; not end-to-end runs.',
    'agentsnet_consensus_constant_zero': consensus(SimpleNamespace(graph=graph), ['0', '0']),
    'agentsnet_consensus_disagreement': consensus(SimpleNamespace(graph=graph), ['0', '1']),
    'agentsnet_valid_vertex_cover': cover(['Yes', 'No'], graph),
}
try:
    report['agentsnet_empty_vertex_cover'] = cover(['No', 'No'], graph)
except Exception as exc:
    report['agentsnet_empty_vertex_cover'] = {'exception': type(exc).__name__, 'message': str(exc)}

rows = ['NetSys Corporation,12199.99', 'DataCore Enterprise,11999.99']
vendor = BASE / 'inputs/agentcompany--evaluator.py'
for label, fixture_rows in [('listed_order', rows), ('reversed_same_rows', rows[::-1])]:
    fixture = 'name,price\n' + '\n'.join(fixture_rows) + '\n'
    checker = function(vendor, 'checkpoint6', namespace={
        'csv': csv,
        'logging': SimpleNamespace(warning=lambda *_: None),
        'download_owncloud_content': lambda *_: None,
        'open': lambda *_: io.StringIO(fixture),
    })
    report['agentcompany_vendor_' + label] = checker('fixture://local')

assert report['agentsnet_consensus_constant_zero'] == 1.0
assert report['agentsnet_consensus_disagreement'] == 0.0
assert report['agentsnet_valid_vertex_cover'] == 1.0
assert report['agentsnet_empty_vertex_cover']['exception'] == 'ZeroDivisionError'
assert report['agentcompany_vendor_listed_order'] is True
assert report['agentcompany_vendor_reversed_same_rows'] is False
utility = function(BASE / 'inputs/agentdojo--slack-user_tasks.py', 'utility', 'UserTask1')
def environment(messages):
    return SimpleNamespace(slack=SimpleNamespace(user_inbox={'Alice': messages}))
before = environment([])
task = SimpleNamespace(USER_SEND='Alice')
report['agentdojo_one_irrelevant_message'] = utility(task, '', before, environment(['unrelated']))
report['agentdojo_two_messages_one_summary'] = utility(task, '', before, environment(['article summary', 'follow-up']))
assert report['agentdojo_one_irrelevant_message'] is True
assert report['agentdojo_two_messages_one_summary'] is False
citation = function(BASE / 'inputs/browsecomp-plus--evaluate_run.py', 'compute_citation_metrics')
report['browsecomp_citation_ids_matching'] = citation(['1'], ['1'])
report['browsecomp_citation_ids_missing'] = citation([], ['1'])
report['browsecomp_citation_scope'] = 'Only document IDs are inputs. These scores cannot establish whether a claim is supported by the document.'
assert report['browsecomp_citation_ids_matching']['precision'] == 1.0
assert report['browsecomp_citation_ids_missing']['recall'] == 0.0
silo = BASE / 'inputs/silo--metrics.py'
namespace = {'json': json}
namespace['_normalize_value'] = function(silo, '_normalize_value', namespace=namespace)
namespace['_longest_increasing_subsequence_length'] = function(silo, '_longest_increasing_subsequence_length')
success = function(silo, 'compute_success_rate', namespace=namespace)
partial = function(silo, 'compute_partial_correctness', namespace=namespace)
def submissions(values):
    return [{'agent_id': i, 'answer': value} for i, value in enumerate(values)]
for case in ('III-21_n100', 'III-30_n2'):
    task = json.loads((BASE / ('inputs/silo--' + case + '.json')).read_text())
    expected = task['expected_output']
    answers = submissions(expected['per_agent_values'])
    result = {'exact': success(answers, expected)}
    try:
        result['partial'] = partial(answers, expected, 'III')
    except Exception as exc:
        result['partial'] = {'exception': type(exc).__name__, 'message': str(exc)}
    report['silo_gold_' + case] = result
task = json.loads((BASE / 'inputs/silo--III-21_n2.json').read_text())
expected = task['expected_output']
complete = sum(expected['per_agent_values'], [])
alternative = [complete[:19], complete[19:]]
report['silo_alternative_sorted_partition'] = {
    'lengths': list(map(len, alternative)),
    'same_sorted_concatenation': sum(alternative, []) == complete == sorted(complete),
    'exact': success(submissions(alternative), expected),
}
assert report['silo_gold_III-21_n100']['exact'] == 1.0
assert abs(report['silo_gold_III-21_n100']['partial'] - 0.4615) < 1e-9
assert report['silo_gold_III-30_n2']['partial']['exception'] == 'TypeError'
assert report['silo_alternative_sorted_partition']['same_sorted_concatenation']
assert report['silo_alternative_sorted_partition']['exact'] == 0.0
(BASE / 'fixture-audit.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
