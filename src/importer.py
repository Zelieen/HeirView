def read_in_file(self, directory):
    # load file into memory

    # go line by line

    ## if [0] = 0: this is e new entry
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