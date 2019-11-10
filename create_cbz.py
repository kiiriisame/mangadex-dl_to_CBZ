import os, sys
from shutil import copyfile, make_archive, move, rmtree


def get_sorted_subdirs(dir):
    # dir: directory with chapters as subdirectory
    
    subdirs = [f.path for f in os.scandir(dir) if f.is_dir()]
    subdirs = [d.split('/')[1] for d in subdirs]
    sortfloats = [float(d.split()[0][1:]) for d in subdirs]
    sorted_subdirs = [y for (x,y) in sorted(zip(sortfloats,subdirs))]
     
    return [dir + "/" + d for d in sorted_subdirs]

def get_sorted_files(dir):
    # dir: directory with image files on the mangadex-dl format
    
    files = [f.path for f in os.scandir(dir)]
    files = [f.split('/')[-1] for f in files]
    sortfloats = [float(f.split('.')[0][1:]) for f in files]
    sorted_files = [y for (x,y) in sorted(zip(sortfloats,files))]
     
    return [dir + "/" + d for d in sorted_files]

def walk_subdirs(sorted_subdirs,newdir = "output"):
    n = 6 # number of digits in filename
    i = 0
    os.mkdir(newdir)
    for subdir in sorted_subdirs:
        files = get_sorted_files(subdir)
        for f in files:
            extention = f.split('.')[-1]
            copyfile(f,newdir + "/" + str(i).zfill(n) + "." + extention)
            i = i+1

def create_cbz(dir):
    sorted_subdirs = get_sorted_subdirs(dir)
    walk_subdirs(sorted_subdirs)
    make_archive('output', 'zip','output')
    move('output.zip',dir.strip('/').strip('.') + '.cbz')
    print("Created output: " + dir.strip('/').strip('.') + '.cbz')
    rmtree('output')
            
if __name__ == "__main__":
    argv = sys.argv
    if len(argv) <= 1:
        print("Usage: python3 create_cbz.py <dirname>")
    dir = argv[1]
    create_cbz(dir)
