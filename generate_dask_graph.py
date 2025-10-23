from graphviz import Digraph

dot = Digraph(comment='Dask Task Graph')

dot.node('a', 'load a')
dot.node('b', 'load b')
dot.node('c', 'load c')
dot.node('d', 'load d')
dot.node('sum_ab', 'sum(a, b)')
dot.node('sum_cd', 'sum(c, d)')
dot.node('mul', 'mul(sum_ab, sum_cd)')

dot.edges(['ab', 'ac', 'cd', 'bd'])
dot.edge('a', 'sum_ab')
dot.edge('b', 'sum_ab')
dot.edge('c', 'sum_cd')
dot.edge('d', 'sum_cd')
dot.edge('sum_ab', 'mul')
dot.edge('sum_cd', 'mul')

dot.render('images/high_performance_python/dask_task_graph', view=False, format='png')
