import os
from exif import Image
import shutil
import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import sys
import time
from pathlib import Path
import exifread
import time

################## Name the mains folder in the way you want ###################
main_folder = "Anys"
secundary_folder = "Anys_revisar"
revision_folder = "Sense_data"
################### Name the months in the way you want #####################
months = ["Gener","Febrer","Març","Abril","Maig","Juny","Juliol","Agost","Setembre","Octubre","Novembre","Desembre"]

## "ask for [y/n] if the answer is yes return true, if it's no return false"
def yes_no():
    answer = None
    while (answer == None):
        print("[Yes/No]:", end=' ')
        x = input()
        if (x == 'Y' or x == 'y' or x == 'Yes' or x == 'yes' or x == 'YES'): answer = True
        elif (x == 'N' or x == 'n' or x == 'No' or x == 'no' or x == 'NO'): answer = False
        else: print("We didn't understand you, please type ", end=' ')
    print("")
    return answer

## "ask for [option1/option2] returns de option1/option2 depending the choose
def choose(option1, option2):
    answer = None
    while (answer == None):
        print("[", option1, "/", option2, "]", end=' ')
        x = input()
        if (x == option1): answer = x
        elif (x == option2): answer = x
        else: print("We didn't understand you, please type ", end=' ')
    print("")
    return answer

## "returns true if a file is an image, false otherwise"
def is_image_file(filename):
    image_file_extensions = ('.rgb','.gif','.pbm','.pgm','.ppm','.tiff','.rast','.xbm','.jpeg','.jpg','.bmp','.png',
    '.webp','.exr','.JPEG','.JPG','.AAE','.PNG')

    if filename.endswith((image_file_extensions)):
        return True
    else:
        return False

## Returns the DateTimeOriginal, otherwise returns the DateTimeDigitized,
## otherwise returns the DateTime, otherwise returns None
def ImageDate(file_path):
    image = Image.open(file_path)
    exifdata = image.getexif()
    T = None
    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        # 36867(0x9003) ==> DateTimeOriginal; 36868(0x9004) ==> DateTimeDigitized; 306(0x0132) ==> DateTime
        if(tag_id == 36867 or tag_id == 36868 or tag_id == 306):
            tag = TAGS.get(tag_id, tag_id)
            data = exifdata.get(tag_id)
            # decode bytes
            if isinstance(data, bytes):
                data = data.decode()
            #print(f"{tag_id:25}: {data}")
            T = (tag_id, data)
            if(T != None): break
    return T

def get_path(message):
    print(message)
    print("Do you want to use the current directory?", end=' ')
    if (yes_no() == True): return os.getcwd()
    else: return ask_path()

def ask_path():
    print("Enter the path of the folder you wanna use:")
    folder_path = os.getcwd() + "/" + input()
    if(os.path.exists(folder_path)):
        return folder_path
    else:
        print("The path you entered doesn't exists, do you want to create it? ", end=' ')
        if(yes_no() == True):
            os.makedirs(folder_path, exist_ok = True)
            return folder_path
        else:
            return ask_path()

def count_photos(path):
    count = 0
    for dirpath, subdirs, files in os.walk(path):
        for name in files:
            if(is_image_file(name) and name[0] != '.'):
                count = count + 1
    return count

## Find the new name for a file which doesn't exists in the directory
def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1

    return path

## Function to sort photos
def sortphotos(source_path, destination_path, n_photos, copy_move, test_mode, silence_mode, keep_duplicates, non_original_apart, revision):
    actual_photo = 1

    print("\nThe settings selected are:", "\nSource: "+source_path, "\nDestination: "+destination_path, "\nCopy/Move: "+copy_move, "\nTest mode: ", test_mode,
            "\nSilence mode: ", silence_mode, "\nKeep duplicates: ", keep_duplicates, "\nNon original: ", non_original_apart, "\nRevision: ", revision)
    print("\nRevise the setting and press enter to procede")
    input()

    for dirpath, subdirs, files in os.walk (source_path):
        for name in files:
            file_path = dirpath + "/" + name
            try:
                if (is_image_file(name) and name[0] != '.'):
                    img_date = ImageDate(file_path)
                    if (not silence_mode):
                        print("Analyzing: " + name + " [" + str(actual_photo) + "/" + str(n_photos) +"]")
                        print("Location: " + file_path)
                    actual_photo += 1

                    if (img_date != None):

                        year = img_date[1][0:4]
                        month = img_date[1][5:7]
                        if (img_date[0] != 306): destination = destination_path + "/" + main_folder + "/"+ str(year) + "/" + str(month) + " - " + months[int(month)-1]
                        else: destination = destination_path + "/" + secundary_folder + "/"+ str(year) + "/" + str(month) + " - " + months[int(month)-1]
                        if (not os.path.exists(destination) and not test_mode): os.makedirs(destination, exist_ok=True)

                        destination += "/" + name
                        if (not silence_mode): print("Destination:" + destination)
                        if (not silence_mode): print(img_date)
                        if (os.path.isfile(destination) and keep_duplicates):
                            destination = uniquify(destination)
                            if(not silence_mode): print("File renamed from " + name + " to " + os.path.basename(destination))


                        if (copy_move == "copy"):
                            if(not test_mode): shutil.copyfile(file_path, destination)
                            if(not silence_mode): print("File has been copied succesfully!")
                        elif (copy_move == "move"):
                            if(not test_mode): shutil.move(file_path, destination)
                            if(not silence_mode): print("File has been moved succesfully!")
                    else:
                        if (not silence_mode): print("The image does't have a DateTime", "Please check it manually later.")
                        if (revision):
                            destination = destination_path + "/" + revision_folder
                            if (copy_move == "copy"):
                                if(not test_mode): shutil.copyfile(file_path, destination)
                                if(not silence_mode): print("File has been copied succesfully!")
                            elif (copy_move == "move"):
                                if(not test_mode): shutil.move(file_path, destination)
                                if(not silence_mode): print("File has been moved succesfully!")
            except:
                if (not silence_mode): print("ERROR: The file hasn't been copied/moved...")
            if (not silence_mode): print("")
def main():
    # Starting the script
    print("Script started !\nI've you wanna restart the program at any point, please press CTRL + C to kill the process")
    time.sleep(0.5)
    print("___________________________________________________________________________________")
    print("Please remember that this script was written to sort the photos of a folder \nUnless you modify the code, the photos will be sorted by years and then by months")
    time.sleep(0.5)
    print("____________________________________________________________________________________")
    print("Now you'll have to set the configuration of the program by answering some questions:\n")
    time.sleep(0.5)

    # Source path and destination path
    source_path = get_path("Now you'll be asked to write the source path (you can use the current directory or select another)")
    print("_"*(len(source_path)+8))
    print("Source: " + source_path)
    print("_"*(len(source_path)+8), "\n")
    destination_path = get_path("Now you'll be asked to write the destination path (you can use the current directory or select another)")
    print("_"*(len(destination_path)+13))
    print("Destination: " + destination_path)
    print("_"*(len(destination_path)+13), "\n")
    time.sleep(0.5)

    # Settings: copy_move, test_mode, silence_mode, keep_duplicates, non_original_apart, revision
    print("Do you wish to 'copy' or 'move' the files?", end=' ')
    copy_move = choose("copy", "move")
    print("Do you want to KEEP DUPLICATES? (Photos with the same name will be renamed adding 1, 2, 3 at the end)")
    keep_duplicates = yes_no()
    print("Do you want to run the script in TEST MODE? (it will only display the process and not copy/move anything)", end=' ')
    test_mode = yes_no()
    print("Some photos may not have a DateTimeOriginal Tag and might not be taken from the date indicated, do you wish to copy/move them into a secundary folder?", end=' ')
    non_original_apart = yes_no()
    print("Do you want to copy/move the photos without DateTime into a revision folder?", end =' ')
    revision = yes_no()
    if (not test_mode):
        print("Do you want to run the run the script in silence mode? (it won't display the info from each photo)", end =' ')
        silence_mode = yes_no()
    else:
        silence_mode = False
    time.sleep(0.5)

    n_photos = count_photos(source_path)

    print("There are "+ str(n_photos) + " ready to be sorted, do you wish to continue? (WARNING: This is a one way process)", end=' ')
    execute = yes_no()
    time.sleep(0.5)

    if (execute == True):
        sortphotos(source_path, destination_path, n_photos, copy_move, test_mode, silence_mode, keep_duplicates, non_original_apart, revision)
        print("\nSorting have been completed!!\n")
    else:
        print("\nHave a nice day anyway!\n")

if __name__ == "__main__":
	main()
