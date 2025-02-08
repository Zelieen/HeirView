from tree import Tree
from chart import Chart

print("starting HeirView")

t = Tree()
t.import_from_file("./HeirView_test_export.ged")
print(t)
persons = t.get_ancestors_for_chart(1, 1)
connections = t.get_connections_for_chart(persons)

c = Chart()
c.add_persons(persons)
c.add_connections(connections)
print(c)