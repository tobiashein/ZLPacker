# ZLPacker
 
A python script to create Zipped Loop Files for FL Studio.

# Usage

    main.py -f <flp directory> -s [<sample directory> [<sample directory> ...]] --output <directory> 

### Example
    main.py -f c:\myProjects -s c:\samples c:\library c:\myProjects --output c:\myZippedProjects

### Breakdown
    -f c:\myProjects  
This is the directory that contains all the flp files.

    -s c:\samples c:\library c:\myProjects 
These are the directories that contain all the samples. Make sure to add the directory with the flp files to include samples that are already stored inside the project directories aswell.

    --output c:\myZippedProjects
This is the directory where the zippe loop packages are saved.

# Notes

The script was implemented back in 2009 when FL Studio 8 was the most current version. It has been successfully tested with FL Studio 11. Keep this in mind when you're running the script at your own risk.