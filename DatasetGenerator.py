# MAIN PROGRAM: uses either CommonFoldersTrainValid.py or DifferentFoldersTrainValid.py
# Program used to create the "train.txt" and "valid.txt", identifying the files from the given folders

####################
###### IMPORT ######
####################
from CommonFoldersTrainValid import commonDirTrainValid
from DifferentFoldersTrainValid import differentDirTrainValid


#######################
###### FUNCTIONS ######
#######################
### Ask the user the way training/validation data are stored ones to another ###
def originRelativity():
    print("\nSelect the way your original training/validation data are stored:")
    print("\tCOMMON: if your training/validation data are stored in common folders")
    print("\tDIFFERENT: if your training/validation data are stored in different folders")
    print("Please, type your choice (COMMON / DIFFERENT):")
    
    origin_relativity = input()

    while( (origin_relativity != "COMMON") and (origin_relativity != "DIFFERENT") ):
        print("*** Watch out, your choice should either be COMMON or DIFFERENT ***")
        print("*** Please, enter a valid choice ***")
        origin_relativity = input()
        
    return origin_relativity


### Ask the user the "relativity" of the paths generated ###
def destinationRelativity():
    print("\nSelect the relativity according to which you would like the paths to be generated:")
    print("\tABSOLUTE: if you want the paths to be absolute")
    print("\tRELATIVE: if you want the paths to be relative to the folder that will contain your dataset")
    print("Please, type your choice (ABSOLUTE / RELATIVE):")
    
    destination_relativity = input()

    while( (destination_relativity != "ABSOLUTE") and (destination_relativity != "RELATIVE") ):
        print("*** Watch out, your choice should either be ABSOLUTE or RELATIVE ***")
        print("*** Please, enter a valid choice ***")
        destination_relativity = input()
        
    return destination_relativity


##################
###### MAIN ######
##################
if(__name__ == "__main__"):
    origin_relativity = originRelativity()
    destination_relativity = destinationRelativity()

    if( origin_relativity == "COMMON" ):
        path_dataset = commonDirTrainValid(destination_relativity)
    else:
        path_dataset = differentDirTrainValid(destination_relativity)

    print(f"\nYour dataset has been created at the following location:\n\t{path_dataset}")
    
    input("\n*** Press ENTER to exit the program ***")
