from node import Person, Family

def read_in_file(directory):
    lines = []
    with open(directory) as f:
        lines = f.readlines()
    lines = [x.strip(" ") for x in lines] # Leading white space preceding a GEDCOM line should be ignored by the reading system
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
    version = version_lines[0][1][7:-1]
    return version

def get_person_lines(lines):
    person_lines = find_lines_by_tags(lines, ["@I"])
    return person_lines

def get_family_lines(lines):
    family_lines = find_lines_by_tags(lines, ["@F"])
    return family_lines

def collect_person_info(lines, start=0, end=None):
    if not end:
        end = start + 1
        while lines[end][0] != "0": # find line with next entry
            end += 1
    
    # get ID
    parts = lines[start].split("@")
    p_ID = int(parts[1][1:])
    
    # get given name
    g_name_line = find_lines_by_tags(lines[start:end], ["NAME", "GIVN"])[0][1]
    p_g_name = g_name_line.split("GIVN ")[1]
    print(p_g_name)
     # get surname
    surname_line = find_lines_by_tags(lines[start:end], ["NAME", "SURN"])[0][1]
    p_surname = surname_line.split("SURN ")[1]
    print(p_surname)

    # get birth
    birth_date_line = find_lines_by_tags(lines[start:end], ["BIRT", "DATE"])[0][1]
    birth_date = birth_date_line.split("DATE ")[1]
    birth_place_line = find_lines_by_tags(lines[start:end], ["BIRT", "PLAC"])[0][1]
    birth_place = birth_place_line.split("PLAC ")[1].split(",")[0]
    
    # get death
    death_date_line = find_lines_by_tags(lines[start:end], ["DEAT", "DATE"])[0][1]
    death_date = death_date_line.split("DATE ")[1]
    death_place_line = find_lines_by_tags(lines[start:end], ["DEAT", "PLAC"])[0][1]
    death_place = death_place_line.split("PLAC ")[1].split(",")[0]
    
    return p_ID, p_g_name, p_surname, birth_date, birth_place, death_date, death_place

def collect_family_info(lines, start=0, end=None):
    if not end:
        end = start + 1
        while lines[end][0] != "0": # find line with next entry
            end += 1

    # get parents
    father_line = find_lines_by_tags(lines[start:end], ["HUSB"])[0][1]
    father_ID = int(father_line.split("@")[1][1:])
    mother_line = find_lines_by_tags(lines[start:end], ["WIFE"])[0][1]
    mother_ID = int(mother_line.split("@")[1][1:])

    # get children
    children_lines = find_lines_by_tags(lines[start:end], ["CHIL"])[0][1]
    child_IDs = []
    for child_line in children_lines:
        c = int(child_line.split("@")[1][1:])
        child_IDs.append(c)

    # marriage event
    marr_date_line = find_lines_by_tags(lines[start:end], ["MARR", "DATE"])[0][1]
    marr_date = marr_date_line.split("DATE ")[1]
    marr_place_line = find_lines_by_tags(lines[start:end], ["MARR", "PLAC"])[0][1]
    marr_place = marr_place_line.split("PLAC ")[1].split(",")[0]

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
            p_info = collect_person_info(file[start:end], start, end)
            persons_list.append(make_person_from_info(p_info))
        elif "@F" in file[start]:
            f_info = collect_family_info(file[start:end], start, end)
            families_list.append(Family(f_info))
        else:
            pass
    
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

    if get_version(file[blocks[1][0]:blocks[1][1]]) != "5.5.1":
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