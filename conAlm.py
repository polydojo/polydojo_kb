# std:
# n/a

# pip-int:
import dotsi;

# pip-ext:
# n/a

# loc:
# n/a

checkTruthyStr = lambda s: bool(s and type(s) is str);

def buildConcentricAlm (accessLevelList):
    """
    Builds a concentric ALM, based on `accessLevelList`,
    which should be a list of strings, from lowest to highest.
    Eg.
        alm = conAlm.build(['low', 'mid', 'high'])
        alm.contains("mid", "low")  # True
        alm.contains("mid", "high") # False
        alm.contains("mid", "mid")  # True
        alm.exceeds("mid", "mid")   # False
    """;
    assert len(accessLevelList) >= 2;
    assert len(accessLevelList) == len(set(accessLevelList));
    assert all(map(checkTruthyStr, accessLevelList));

    lim = {};   # Level to Index Map, internal helper.
    for (i, level) in enumerate(accessLevelList):
        lim[level] = i;
    
    def expand (level):
        """
        Expands`level`, returning the list of contained
        access levels, including `level` itself.
        Eg:
            alm = conAlm.build("low", "mid", "high"])
            alm.expand("low")   # -> ["low"]
            alm.expand("mid")   # -> ["low", "mid"]
            alm.expand("high")  # -> ["low", "mid", "high"]
        """;
        assert level in lim;
        return accessLevelList[0 : lim[level] + 1];
        # ^Slice from lowest to given `level`, both incl.
    
    def contains (perimeterLevel, testLevel):
        """
        Checks if `perimeterLevel` includes `testLevel`.
        Note: Each level is considered to contain itself.
        Eg:
            alm = conAlm.build("low", "mid", "high"])
            alm.contains("mid", "low")  # True
            alm.contains("mid", "mid")  # True
            alm.contains("mid", "high") # False
        """;
        assert perimeterLevel in lim and testLevel in lim;
        return lim[perimeterLevel] >= lim[testLevel];
    
    def exceeds (higherLevel, testLevel):
        """
        Checks if `higherLevel` strictly exceeds `testLevel`.
        Note: No level is considered to exceed itself.
        Eg:
            alm = conAlm.build("low", "mid", "high"])
            alm.exceeds("mid", "low")  # True
            alm.exceeds("mid", "mid")  # False
            alm.exceeds("mid", "high") # False

        """;        
        assert higherLevel in lim and testLevel in lim;
        return lim[higherLevel] > lim[testLevel];
    
    return dotsi.fy({
        "expand": expand,
        "contains": contains,
        "exceeds": exceeds,
        "getMinLevel": lambda : accessLevelList[0],
        "getMaxLevel": lambda : accessLevelList[-1],
        "_accessLevelList": accessLevelList,
        "_levelIndexMap": lim,
    });
build = buildConcentricAlm; # Alias, short.
# Exo-use: `import conAlm; conAlm.build(["min", "mid", "max"]);`

def test_concentricAlm ():
    alm = buildConcentricAlm(["low", "mid", "high"]);
    
    # alm.expand:
    assert alm.expand("low") == ["low"];
    assert alm.expand("mid") == ["low", "mid"];
    assert alm.expand("high") == ["low", "mid", "high"];
    
    # alm.contains:
    assert alm.contains("low", "low") == True;
    assert alm.contains("low", "mid") == False;
    assert alm.contains("low", "high") == False;
    # cont.
    assert alm.contains("mid", "low") == True;
    assert alm.contains("mid", "mid") == True;
    assert alm.contains("mid", "high") == False;
    # cont.
    assert alm.contains("high", "low") == True;
    assert alm.contains("high", "mid") == True;
    assert alm.contains("high", "high") == True;
    
    # alm.exceeds:
    assert alm.exceeds("low", "low") == False;
    assert alm.exceeds("low", "mid") == False;
    assert alm.exceeds("low", "high") == False;
    # cont.
    assert alm.exceeds("mid", "low") == True;
    assert alm.exceeds("mid", "mid") == False;
    assert alm.exceeds("mid", "high") == False;
    # cont.
    assert alm.exceeds("high", "low") == True;
    assert alm.exceeds("high", "mid") == True;
    assert alm.exceeds("high", "high") == False;

    return True;

# Run tests if __main__: :::::::::::::::::::::::::::::::::::

if __name__ == "__main__":
    test_concentricAlm();
    print("Tests passed.");

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
