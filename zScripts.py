# std:
import os;
import sys;

# pip-ext:
# n/a

# pip-int:
import dotsi;

# loc:
import utils;

def rmBundles ():
    for filename in os.listdir("./front"):
        if "-bundle.js" in filename:
            os.remove("./front/" + filename);

def help ():
    print("\nRun as: $ python zScripts.py {funcName}");
    print("Available funcNames are listed below.\n");
    for (k, v) in globals().items():
        if callable(v):
            print(k);
    print("");

if __name__ == "__main__":
    assert len(sys.argv) == 2;
    funcName = sys.argv[1];
    globals()[funcName]();
    
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
