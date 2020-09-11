import os
import sys
import re
import fnmatch
import argparse
import time
import zipfile


def extract_samples(path):
    ## generate list of ascii characters
    ascii = ["\0"]*256
    for ii in xrange(32, 127):
        ascii[ii] = chr(ii)
    ascii[ord("\t")] = "\t"        
    ascii = "".join(ascii)

    ## extract ascii strings
    data = []
    for s in open(path, "rb").read().translate(ascii).split("\0"):
        if len(s) >= 6:
            data.append(s)
    
    ## extract filenames
    samples = []
    for item in data:
        match = re.findall(r".:\\.*\..*$", item)
        if match:
            samples.append(os.path.normcase(os.path.normpath(match[0])))
    return samples


def get_files(root, patterns=["*"]):
    for path, _, files in os.walk(root):
        for file in files:
            for pattern in patterns:
                if fnmatch.fnmatch(file, "*.%s" % pattern):
                    yield os.path.normcase(os.path.join(path, file))

    
def main():
    ## init parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", metavar="<path>", type=str, dest="flp_path", help="flp directory", required=True)
    parser.add_argument("-s", metavar="<path>", type=str, dest="sample_path", help="samples directory", nargs="*", required=True)
    parser.add_argument("--output", metavar="<path>", type=str, dest="output", help="output directory", required=True)
    args = parser.parse_args()
    
    ## get list of samples 
    if os.path.isdir(args.flp_path):
        args.sample_path.append(args.flp_path)
    lib_list = []
    for item in args.sample_path:
        lib_list.extend(list(get_files(item, ["*"])))
    library = {}
    for item in lib_list:
        library[item] = item
        tmp = item
        for ii in xrange(len(tmp.split("\\")) - 1):
            tmp = os.path.normcase(tmp.split("\\", 1)[1])
            library[tmp] = item

    ## get list of flp files
    flp_files = []
    if os.path.isdir(args.flp_path):
        flp_files.extend(list(get_files(args.flp_path, ["flp"])))
    else:
        flp_files.append(args.flp_path) 

    ## create log file
    log = open("log.txt", "w")    
    
    ## iterate over flp files
    for flp in flp_files:
        zip_path = os.path.join(args.output, os.path.dirname(flp[3:]))
        zip_name = "%s.zip" % os.path.splitext(os.path.basename(flp))[0]
        
        if os.path.exists(os.path.join(zip_path, zip_name)):
            continue
        
        if not os.path.exists(zip_path):
            os.makedirs(zip_path)
            
        zip = zipfile.ZipFile(os.path.join(zip_path, zip_name), "w", zipfile.ZIP_DEFLATED)
        zip.write(flp, arcname=os.path.basename(flp))

        samples = extract_samples(flp)

        missing_samples = []
            
        print "%s" % flp
        
        for smp in samples:
            found = False
            path_levels = [smp]

            for ii in xrange(len(smp.split("\\")) - 1):
                path_levels.append(os.path.normcase(path_levels[-1].split("\\", 1)[1]))
            
            for path in path_levels:
                if path in library:
                    found = True
                    zip.write(library[path], arcname=os.path.basename(library[path]))
                    break
                
            if not found:
                missing_samples.append(path_levels[0])
                print "    not found: %s" % path_levels[0]
        
        print
        zip.close()
            
        if missing_samples:
            log.write("%s\n" % flp)
            for item in missing_samples:
                log.write("    not found: %s\n" % item)
            log.write("\n\n")
    
    log.close()


if __name__ == "__main__":
    start_time = time.time()
    main()
    print "\ntotal time: %.2f seconds" % (time.time() - start_time)
