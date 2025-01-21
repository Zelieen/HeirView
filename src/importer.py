def read_in_file(directory):
    lines = []
    with open(directory) as f:
        lines = f.readlines()
        lines = [x.strip(" ") for x in lines] # Leading white space preceding a GEDCOM line should be ignored by the reading system
    return lines

def find_lines_by_tags(lines, tag_list):
    found_lines = []
    if len(tag_list) < 1:
        return found_lines
    
    current_tag = 0
    for i in range(len(lines)):
        if int(lines[i][0]) >= current_tag: # safe guard against lower level entry beginning
            if lines[i][2:6] == tag_list[current_tag]:
                if current_tag + 1 < len(tag_list):
                    current_tag += 1
                else:
                    found_lines.append((i, lines[i]))
        else:
            current_tag -= 1
    return found_lines

def get_version(lines):
    version_lines = find_lines_by_tags(lines, ["HEAD", "GEDC", "VERS"])
    version = version_lines[0][1][7:-1]
    return version



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