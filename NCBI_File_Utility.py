import os

def main():
    dict1 = {}

    print("This program includes several tools in organizing and maniputating files downloaded from NCBI.\n"+
          "All input files from NCBI should be downloaded as the COMPLETE RECORD in GENBANK (FULL) format.\n"+
          "NCBI files should be placed in the same folder that the NCBI_File_Consolidator program reside in.\n"+
          "Output files will be placed in this same directory.\n\n")

    print("3 sample files have been included with this app.\n"+
          "- seq1.gb\n- seq2.gb\n- seq3_dups.gb\n"+
          "All 3 files have samples in common but only seq3_dups.gb contains duplicates.\n\n")

    option = input("Chose an option:\n1 = Combine two files & remove duplicate samples\n"+
        "2 = Provide a count of sample in a file\n"+
        "3 = Generate a list of accession numbers in a file\n"+
        "4 = Eliminate duplicated samples from a file\n"+
        "x = quit\n\nOption:  ")
    
    if option == "1":
        option1(dict1)

    elif option == "2":
        option2(dict1)

    elif option == "3":
        option3(dict1)

    elif option == "4":
        option4(dict1)
        
    elif option == "x" or option == "X":
        print("quitting")
    else:
        print("command not recognized -quitting")



def option1(dict1):
    masterCounter = 0
    file1 = input("\nEnter the name of the first file: ")
    file2read = file1
    masterCounter = readFile(file2read,dict1,masterCounter)
    file2 = input("\nEnter the name of the second file: ")
    file2read = file2
    masterCounter = readFile(file2read,dict1,masterCounter)
    writeFile(file1,dict1,masterCounter)


def readFile(file2read,dict1,masterCounter):
    try:
        infile = open(file2read)
        counter = 0
        sample = ""
        sampInfo = ""
        workingThroughSampleData = "no"

        for line in infile:
            if workingThroughSampleData == "yes":
                if line == "\n":
                    workingThroughSampleData = "no"
                    dict1[sample] = sampInfo
                else:
                    sampInfo = sampInfo+line
            else:
                if line[0:5] == "LOCUS":
                    sampInfo = line
                    workingThroughSampleData = "yes"
                    sample = line[12:20]
                    counter = counter+1
        infile.close()
        print("File {0:s} contains {1:d} samples".format(file2read,counter))
        masterCounter = masterCounter+counter
        return masterCounter
        
    except FileNotFoundError:
        print("No file found with the name provided")
        quit()


def writeFile(file1,dict1,masterCounter):
    checker = "no"
    while checker == "no":                          #changing output file name & check 
        file1,checker = changeName(file1,checker)   #that not overwriting any files
        if os.path.isfile(file1) == False:
            checker = "its good" 
    
    outfile = open(file1, 'w')

    counter = 0
    for key in dict1:
        sample = dict1[key]
        outfile.writelines(sample)
        outfile.write("\n")
        counter=counter+1

    outfile.close()
    print("\nThe combined output file is called:  {0:s}\nIt contains {1:d} samples.".format(file1,counter))
    counter = masterCounter-counter
    print("{0:d} duplicate samples were excluded.".format(counter))

def changeName(file1,checker):
    nameLength = (len(file1)-3)
    file1 = file1[0:nameLength]       #removing the extention
    file1 = file1+"_combined.gb"    #change file name & putting extention back on
    return file1,checker


def option2(dict1):  #counts the number of samples in the file
    masterCounter = 0
    file1 = input("\nEnter the name of the file: ")
    file2read = file1
    masterCounter = readFile(file2read,dict1,masterCounter)
    

def option3(dict1):  #list sample accession numbers
    masterCounter = 0
    file1 = input("\nEnter the name of the file: ")
    file2read = file1
    masterCounter = readFile(file2read,dict1,masterCounter)
    readFile_opt3(file2read)
    

def readFile_opt3(file2read):
    try:
        infile = open(file2read)
        workingThroughSampleData = "no"

        for line in infile:
            if workingThroughSampleData == "yes":
                if line == "\n":
                    workingThroughSampleData = "no"
            else:
                if line[0:5] == "LOCUS":
                    print(line[12:20])
                    workingThroughSampleData = "yes"
        infile.close()

    except FileNotFoundError:
        print("No file found with the name provided")
        quit()


def option4(dict1):
    masterCounter = 0
    file1 = input("\nEnter the name of the file: ")
    file2read = file1
    masterCounter = readFile(file2read,dict1,masterCounter)
    writeFile_opt3(file1,dict1,masterCounter)


def writeFile_opt3(file1,dict1,masterCounter):
    checker = "no"
    while checker == "no":                          #changing output file name & check 
        file1,checker = changeName_alt(file1,checker)   #that not overwriting any files
        if os.path.isfile(file1) == False:
            checker = "its good" 
    
    outfile = open(file1, 'w')

    counter = 0
    for key in dict1:
        sample = dict1[key]
        outfile.writelines(sample)
        outfile.write("\n")
        counter=counter+1

    outfile.close()
    print("\nThe output file is called:  {0:s}\nIt contains {1:d} samples.".format(file1,counter))
    counter = masterCounter-counter
    print("{0:d} duplicate samples were excluded.".format(counter))


def changeName_alt(file1,checker):
    nameLength = (len(file1)-3)
    file1 = file1[0:nameLength]       #removing the extention
    file1 = file1+"_no_duplicates.gb"    #change file name & putting extention back on
    return file1,checker

main()
