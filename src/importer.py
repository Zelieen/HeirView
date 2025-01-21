def read_in_file(directory):
    lines = []
    with open(directory) as f:
        lines = f.readlines()
        lines = [x.strip(" ") for x in lines] # Leading white space preceding a GEDCOM line should be ignored by the reading system
    return lines

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
    return found_lines # a tuple (line index, line content)

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

def collect_person_info(lines, start):
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

    return p_ID



    ## if [0] = 0: this is a new entry
    ## then check which type (HE, @I, @F)

    ### HE = this is the header
    #### get the version from eg "2 VERS 5.5.1"
    ##### is it compatible?

    ### @I = this is a person
    #### make a new person with names
    ##### add all information:
    ###### birth: add event
    ###### death: add event
    ###### more to be determined

    ### @F this is a family declaration
    #### add relationships to persons
    ##### partnership mother-father
    ##### child-mother
    ##### child-father
    ##### if married: add event