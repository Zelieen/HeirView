from node import Person, Family

def read_in_file(directory):
    lines = []
    with open(directory) as f:
        lines = f.readlines()
    lines = [x.strip(" ") for x in lines] # Leading white space preceding a GEDCOM line should be ignored by the reading system
    lines = [x.rstrip("\n") for x in lines]
    return lines

def find_blocks(lines):
    blocks = []

    for i in range(len(lines)):
        if lines[i][0] == "0":
            blocks.append((i, i))
            if len(blocks) > 1:
                blocks[-2] = (blocks[-2][0], i) # add end line to previous block
    blocks[-1] = (blocks[-1][0], i) # add last line as end of last block
    return blocks

def find_lines_by_tags(lines, tag_list, start=0): # finds the lines that are nested in the order of the tags
    found_lines = []
    if len(tag_list) < 1:
        return found_lines
    
    current_tag = 0
    for i in range(start, len(lines)):
        if int(lines[i][0]) >= current_tag: # safe guard against lower level entry beginning
            if tag_list[current_tag] in lines[i]:
                if current_tag + 1 < len(tag_list): # more tags to consider?
                    current_tag += 1
                else:
                    found_lines.append((i, lines[i]))
        else:
            current_tag -= 1
    return found_lines # a tuple (line index, line content) # change to tuple: (start, end of block)

def get_version(lines):
    version_lines = find_lines_by_tags(lines, ["HEAD", "GEDC", "VERS"])
    version = version_lines[0][1][7:]
    return version

def get_person_lines(lines):
    person_lines = find_lines_by_tags(lines, ["@I"])
    return person_lines

def get_family_lines(lines):
    family_lines = find_lines_by_tags(lines, ["@F"])
    return family_lines

def collect_person_info(lines, start=0, end=None):
    if end == None:
        end = len(lines) - 1
    
    # get ID
    parts = lines[start].split("@")
    p_ID = int(parts[1][1:])
    
    # get given name
    p_g_name = None
    g_name_line = find_lines_by_tags(lines[start:end], ["NAME", "GIVN"])
    if g_name_line != []:
        p_g_name = g_name_line[0][1].split("GIVN ")[1]
     # get surname
    p_surname = None
    surname_line = find_lines_by_tags(lines[start:end], ["NAME", "SURN"])
    if surname_line != []:
        p_surname = surname_line[0][1].split("SURN ")[1]

    # get birth
    birth_date = None
    birth_date_line = find_lines_by_tags(lines[start:end], ["BIRT", "DATE"])
    if birth_date_line != []:
        birth_date = birth_date_line[0][1].split("DATE ")[1]
    birth_place = None
    birth_place_line = find_lines_by_tags(lines[start:end], ["BIRT", "PLAC"])
    if birth_place_line != []:
        birth_place = birth_place_line[0][1].split("PLAC ")[1].split(",")[0]
    
    # get death
    death_date = None
    death_date_line = find_lines_by_tags(lines[start:end], ["DEAT", "DATE"])
    if death_date_line != []:
        death_date = death_date_line[0][1].split("DATE ")[1]
    death_place = None
    death_place_line = find_lines_by_tags(lines[start:end], ["DEAT", "PLAC"])
    if death_place_line != []:
        death_place = death_place_line[0][1].split("PLAC ")[1].split(",")[0]
    
    return p_ID, p_g_name, p_surname, birth_date, birth_place, death_date, death_place

def collect_family_info(lines, start=0, end=None):
    if end == None:
        end = len(lines) - 1

    # get parents
    father_ID = None
    father_line = find_lines_by_tags(lines[start:end], ["HUSB"])
    if father_line != []:
        father_ID = int(father_line[0][1].split("@")[1][1:])
    mother_ID = None
    mother_line = find_lines_by_tags(lines[start:end], ["WIFE"])
    if mother_line != []:
        mother_ID = int(mother_line[0][1].split("@")[1][1:])

    # get children
    children_lines = find_lines_by_tags(lines[start:end], ["CHIL"])
    child_IDs = []
    for child_line in children_lines:
        c = int(child_line[1].split("@")[1][1:])
        child_IDs.append(c)

    # marriage event
    marr_date = None
    marr_date_line = find_lines_by_tags(lines[start:end], ["MARR", "DATE"])
    if marr_date_line != []:
        marr_date = marr_date_line[0][1].split("DATE ")[1]
    marr_place = None
    marr_place_line = find_lines_by_tags(lines[start:end], ["MARR", "PLAC"])
    if marr_place_line != []:
        marr_place = marr_place_line[0][1].split("PLAC ")[1].split(",")[0]

    return mother_ID, father_ID, child_IDs, marr_date, marr_place

def make_person_from_info(p_ID, p_g_name, p_surname, birth_date, birth_place, death_date, death_place):
    p = Person(p_ID, p_g_name, p_surname)
    if birth_date or birth_place:
        p.add_event("birth", p_ID, birth_date, birth_place)
    if death_date or death_place:
        p.add_event("death", p_ID, death_date, death_place)
    return p

def extract_info(file, blocks):    
    persons_list = []
    families_list = []

    for start, end in blocks:
        if "@I" in file[start]:
            #print(file[start:end])
            p_info = collect_person_info(file[start:end])
            persons_list.append(make_person_from_info(*p_info))
        elif "@F" in file[start]:
            f_info = collect_family_info(file[start:end])
            families_list.append(Family(*f_info))
        else:
            pass
    print(f"extracted {len(persons_list)} persons and {len(families_list)} families")
    return persons_list, families_list #Tuple (list of Person(), list of Family())

def import_file(directory):
    file = read_in_file(directory)
    if file == []:
        print("there is nothing in the file!")
        return
    if "HEAD" not in file[0]:
        print("Found no HEAD section at start of file")
        return
    
    blocks = find_blocks(file)
    version = get_version(file[blocks[1][0]:blocks[1][1]])

    if  version != "5.5.1":
        print(f"file does not contain a compatible gedcom version")
        return
    
    return extract_info(file, blocks)

    # pseudocode:
    # gather person data
    # make Person() for each
    # add events to the Person()
    # add the Person() to the tree
    # gather families information
    # integrate relationships into the tree