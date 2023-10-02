# SUB PROGRAM: used by DatasetGenerator.py
# Program used to create the "train.txt" and "valid.txt", identifying the files from the given directories

####################
###### IMPORT ######
####################
from os import mkdir, walk
from os.path import abspath, basename, join, splitext
from pathlib import Path
from shutil import copyfile
import random


#######################
###### FUNCTIONS ######
#######################
### Check if the paths given are valid ###
def isPathValid(path):
    if (Path(path).exists()):
        return True
    else:
        print("*** The path given is not valid ***")
        print("*** Please, provide another one ***")
        return False


### Ask the user to enter a path an return it ###
def askUserPath(instruction):
    print(instruction)
    path = Path(input().strip("\"\'"))
    while (not (isPathValid(path))):
        path = Path(input().strip("\"\'"))

    return path


### Ask the user to enter successive paths, append them to a list and return it ###
def askUserSuccessivePaths(instruction):
    list_path = []
    path = None

    print(instruction)
    print("(type 'DONE' when you are done)")

    while (path != "DONE"):
        path = input().strip("\"\'")
        while ((path != "DONE") and (isPathValid(path) == False)):
            path = input().strip("\"\'")
        if (path != "DONE"):
            list_path.append(Path(path))

    return list_path


### Check the files contained at "dir_path" and append their paths to a list when their extensions are in "list_ext", return this list of paths ###
def listFileWithExt(dir_path, list_ext):
    list_path = []
    for file in next(walk(dir_path))[2]:
        if (splitext(file)[1] in list_ext):
            list_path.append(join(dir_path, file))

    return list_path


### Check for a file named "filename" within several directories whose paths are listed in "list_dir" ###
def findFileWithinListDir(filename, list_dir):
    for dir in list_dir:
        for file in next(walk(dir))[2]:
            if( basename(file) == filename ):
                return join(dir, file)

    return None


### Compare the names of the images and the labels, if they have the same names (without their extensions) they are eligible as training/validation samples ###
def listImageLabelSameRootname(list_path_dir_im, list_path_dir_lab):
    # Empty processing lists
    list_im = []
    list_lab = []
    # Empty lists that will contain the paths of the couples [images, labels] that can be used to create the training/validation datasets
    list_eli = []

    # Populate the list of images
    for path_dir_im in list_path_dir_im:
        list_im += listFileWithExt(path_dir_im, [".jpg", ".png"])
    # Populating the list of labels
    for path_dir_lab in list_path_dir_lab:
        list_lab += listFileWithExt(path_dir_lab, [".txt"])

    # Populating the list of eligible couples of files [images, labels]
    for image in list_im:
        for label in list_lab:
            if (basename(image).split(".")[0] == basename(label).split(".")[0]):
                list_eli.append([image, label])
                break

    return list_eli


### Generate a list of elements for the phase dataset and return it ###
def generatePhaseDataset(instruction, list_eli):
    tot_eli = len(list_eli)
    counter = 0
    list_phase = []

    print(instruction)
    print("Up to", tot_eli, "file(s) can be kept:")

    input_num = int(input())
    while ((input_num < 0) or (input_num > tot_eli)):
        print("*** The value given is not valid ***")
        print("*** Please, provide another one ***")
        input_num = int(input())

    while (counter < input_num):
        rand_ind = random.randint(0, (tot_eli-1))
        list_phase.append(list_eli.pop(rand_ind))
        tot_eli -= 1
        counter += 1

    return list_phase


### Creation of the directory/file needed for a specific phase ###
### Return the file containing the paths of the data that will be used during this phase ###
def createPhaseDatasetDirFile(phase_name, list_file, out_dir, out_dir_str):
    out_phase = join(out_dir, phase_name)
    out_phase_str = join(out_dir_str, phase_name)
    mkdir(out_phase)
    # Creation of　a file containing the path of the data that will be used during "phase_name"
    phase_path_file = open(join(out_dir, f"{phase_name}.txt"), "w+")
    # Copy every images / labels from "list_file" to the "phase_name" directory
    for file in list_file:
        # Temporary files
        temp_im_str = join(out_phase_str, basename(file[0]))
        temp_im = join(out_phase, basename(file[0]))
        temp_lab = join(out_phase, basename(file[1]))
        # Copy
        copyfile(file[0], temp_im)
        copyfile(file[1], temp_lab)
        # Add the name of the images to the path file
        phase_path_file.write(temp_im_str + "\n")
    phase_path_file.close()
    
    return phase_path_file


### Create the "obj.data" file ###
def objdataCreation(out_dir, out_valid_str, classes_names, train_txt, valid_txt, backup_dir):
    data_file_name = basename(out_dir) + ".data"
    obj_data_path = join(out_dir, data_file_name)
    obj_data_content = open(obj_data_path, "w+")

    num_classes = 0
    with open(classes_names) as file:
        for (num_class, name_class) in enumerate(file):
            num_classes += 1

    obj_data_content.write("classes = " + str(num_classes) + "\r\n")
    obj_data_content.write("train = " + join(out_valid_str, basename(train_txt.name)) + "\r\n")
    obj_data_content.write("valid = " + join(out_valid_str, basename(valid_txt.name)) + "\r\n")
    obj_data_content.write("names = " + join(out_valid_str, basename(classes_names)) + "\r\n")
    obj_data_content.write("backup = " + join(out_valid_str, basename(backup_dir), ""))

    return


##################
###### MAIN ######
##################
def differentDirTrainValid(destination_relativity):
    # CREATION VARIABLES
    list_train = []
    list_valid = []

    ### SELECTION ELIGIBLE FILES ###
    # Populating the list containing the paths to the TRAIN IMAGES
    list_dir_im_train_instruction = "\nEnter the path(s) to the directories containing the IMAGES you want in your TRAIN dataset:"
    list_dir_im_train = askUserSuccessivePaths(list_dir_im_train_instruction)
    # Populating the list containing the paths to the VALID IMAGES
    list_dir_im_valid_instruction = "\nEnter the path(s) to the directories containing the IMAGES you want in your VALID dataset:"
    list_dir_im_valid = askUserSuccessivePaths(list_dir_im_valid_instruction)
    # Populating the list containing the paths to the TRAIN LABELS
    list_dir_lab_train_instruction = "\nEnter the path(s) to the directories containing the LABELS you want in your TRAIN dataset:"
    list_dir_lab_train = askUserSuccessivePaths(list_dir_lab_train_instruction)
    # Populating the list containing the paths to the VALID LABELS
    list_dir_lab_valid_instruction = "\nEnter the path(s) to the directories containing the LABELS you want in your VALID dataset:"
    list_dir_lab_valid = askUserSuccessivePaths(list_dir_lab_valid_instruction)
    # Populating the lists containing the paths for the couples ([images, labels]) of ELIGIBLE files
    list_eli_train = listImageLabelSameRootname(list_dir_im_train, list_dir_lab_train)
    list_eli_valid = listImageLabelSameRootname(list_dir_im_valid, list_dir_lab_valid)

    ### PREPARATION OF THE DATASETS ###
    random.seed()
    # Selection of the data for the TRAIN dataset
    list_train_instruction = "\nChoose the number of files to keep for the training dataset"
    list_train = generatePhaseDataset(list_train_instruction, list_eli_train)
    # Selection of the data for the VALID dataset
    list_valid_instruction = "\nChoose the number of files to keep for the validation dataset"
    list_valid = generatePhaseDataset(list_valid_instruction, list_eli_valid)

    ### CREATION OF THE DATASETS ###
    # Selection of the path, in which the directory will be saved
    out_path_instruction = "\nEnter the path to the directory that will contain your dataset:"
    out_path = askUserPath(out_path_instruction)

    # Creation of the directory
    print("\nEnter the name of your dataset:")
    dataset_name = input()
    out_dir = abspath(join(out_path, dataset_name))
    mkdir(out_dir)
    ### Absolute paths ###
    if (destination_relativity == "ABSOLUTE"):
        out_dir_str = out_dir
    ### Relative paths ###
    else:
        out_dir_str = join(".", basename(out_path), dataset_name)
    
    path_file_train = createPhaseDatasetDirFile("train", list_train, out_dir, out_dir_str)
    path_file_valid = createPhaseDatasetDirFile("valid", list_valid, out_dir, out_dir_str)

    ### CREATION OF THE OTHER FILES NECESSARY ###
    # Creation of the file: "classes.names"
    classes_file_ori = findFileWithinListDir("classes.txt", (list_dir_lab_train + list_dir_lab_valid))
    if (classes_file_ori == None):
        classes_file_ori_instruction = "\nEnter the path of your \"classes.txt\":"
        classes_file_ori = askUserPath(classes_file_ori_instruction)
    classes_file_gen = join(out_dir, "classes.names")
    # Copy of the file "classes.txt" and rename it as "classes.name"
    copyfile(classes_file_ori, classes_file_gen)

    # Creation of the directory: "backup"
    backup_dir = join(out_dir, "backup")
    mkdir(backup_dir)

    # Creation of the file: "obj.data"
    objdataCreation(out_dir, out_dir_str, classes_file_gen, path_file_train, path_file_valid, backup_dir)

    return out_dir