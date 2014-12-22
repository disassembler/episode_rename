#!/usr/bin/python2
# Episode Name - File Renamer
# Renames files without accurate episode order using the Episode Name only
# Originally Coded by: Tim (http://forum.kodi.tv/showthread.php?tid=109546&pid=1430683).
# Alterations by Sam Leathers (https://github.com/disassembler/episode_rename)

# Import modules
import os
import glob
import csv

# Assign inital values
repeat = "true"
edit = "true"

#Define custom functions
def invalid_char(s):
    """
    Strip the invalid filename characters from the string selected.
    Feel free to add/remove additional .replace(X,X) as needed if you
    want to remove other characters even if they are valid.
    For example: , or [ or !
    """
    return s.replace("?","").replace(":","").replace("*","").replace("<","").replace(">","").replace("|","").replace("/","").replace("\\","").replace('"',"")

def season(l):
    """
    Takes the first cell of the CSV copied from the TVDB website
    and strips out only the season.
    """
    if l == "Special":
        season = "00"
    else:
        season = l.split(" ")[0].zfill(2)
    return season

def episode(l):
    """
    Takes the first cell of the CSV copied from the TVDB website
    and strips out only the episode. Pads a 0 before single digits.
    """
    if l == "Special":
        episode = "00"
    else:
        episode = l.split(" ")[-1].zfill(2)
    return episode

# Overall loop, allows user to re-run the entire script
while repeat == "true":

    # Checks if the user defined variables need to be edited
    if edit == "true":

        # Prompt user to define static variables
        series_name = raw_input("Please enter your series name: ")
        #series_name = "Looney Tunes"
        print "\n"
        data = raw_input("Path to CSV: ")
        #data = "input.csv"
        print "\n"
        dir1 = raw_input("Path to episodes (format C:\*): ")
        #dir1 = '/data/rtorrent/downloads/Looney?Tunes?Golden?Collection/*/*/*/Bonus?Cartoons/*'
        print "\n"
        move = raw_input("Would you like to move renamed files? (Yes/No): ").lower()
        move = "yes"
        if move in ("y", "ye", "yes"):
            print "\n"
            print "Enter path to root folder where files should be moved"
            move_path = raw_input("and season folders will be created (format C:\Show\): ")
            #move_path = "/data/pvr/tvshows/Looney Tunes/"
        edit = "false"
    file_list = glob.glob(dir1)
    print ("\n\n")

    # Loop through file_list and look for matches in the CSV to the filename after the prefix assigned
    for file in file_list:
        fname = file
        ext = fname[-4:]
        with open(data, 'r') as file:
            reader = csv.reader(file)
            season_episode_name = ["S" + season(line[0]) + "E" + episode(line[0]) + " " + invalid_char(line[1]) for line in reader if invalid_char(line[1].lower()) in fname.lower() and line[1].lower() != ""]
            season_dir = (''.join(season_episode_name)).split("E")[0][1:]
        if not season_episode_name:
            episode_number = raw_input("\nPlease input season episode number for " + fname + ":")
            with open(data, 'r') as file:
                reader = csv.reader(file)
                for line in reader:
                    if line[0] == episode_number:
                        season_episode_name = ["S" + season(line[0]) + "E" + episode(line[0]) + " " + line[1]]
                        season_dir = (''.join(season_episode_name)).split("E")[0][1:]
        if season_episode_name:
            season_episode_name = ''.join(season_episode_name)
            fname2 = dir1[:-1] + series_name + " " + season_episode_name + ext

            # If user chose to move files to another directory, then fname2 has the path replaced
            if move in ("y", "ye", "yes"):
                fname2 = move_path + "Season " + season_dir + "/" + fname2[len(dir1[:-1]):]

                # Generates the season directory if does not already exist
                if not os.path.exists(move_path + "Season " + season_dir):
                    os.makedirs(move_path + "Season " + season_dir)

            # Rename file and move if user requested
            print fname + "\n    >>> " + fname2 + "\n"
            if not os.path.isfile(fname2):
                os.symlink(fname, fname2)

        else:
            print fname + "\n    >>> " "Unable to locate match, please rename manually.\n"

    # Check if user wants to repeat, edit or exit
    repeat = raw_input ("\n\nType R to run again, Type E to edit the parameters, or Q to quit: ")
    if repeat.lower() in ("r", "retry"):
        repeat = "true"
        print "\nRunning again with the same parameters.."
    elif repeat.lower() in ("e", "edit"):
        edit = "true"
        repeat = "true"
        print "\nEditing paramaters before running again.."
    elif repeat.lower() in ("q", "quit"):
        repeat = "false"
        print "\nQuitting..."
    else:
        repeat = "false"
        print "\nInvalid command."

# When repeat no longer is "true" the script exiits with the below message
else:
    raw_input("\n\nPress enter to exit...")
