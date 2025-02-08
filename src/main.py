from tree import Tree
from chart import Chart
from slate import Slate, Line, Point

def main():
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

    print(t.find_person(1))

    sl = Slate(400, 400)

    sl.draw_text("HeirView", Point(200, 25), "dodgerblue")

    for i in range(len(c.badge_col)):
        col = c.badge_col[i]
        for k in range(len(col)):
            p = col[k]
            pos = Point(*p.get_center())
            pos.x += (i * 200) + 50
            pos.y += (k * 50) + 50
            number = p.person_ID
            person = t.find_person(number)
            name = person.given_name + " " + person.surname

            sl.draw_text(name, pos, size=12)

    sl.wait_for_close()

main()