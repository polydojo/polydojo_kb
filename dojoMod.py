# std:
# n/a

# pip-ext:
# n/a

# pip-int:
import dotsi;
import vf;

# loc:
from constants import K;
import mongo;
import utils;
import bu;

############################################################
# Assertions & prelims:                                    #
############################################################

assert K.CURRENT_DOJO_V == 0;
db = dotsi.fy({"dojoBox": mongo.db.dojoBox});   # Isolate
    
############################################################
# Dojo building and validation:                            #
############################################################

validateDojo = vf.dictOf({
    "_id": utils.isObjectId,
    "_v": lambda x: x == K.CURRENT_DOJO_V,
    #
    # Intro'd in _v0:
    "title": vf.typeIs(str),
    "scratchpad": vf.typeIs(str),
    "creatorId": utils.isObjectId,
    "createdAt": utils.isInty,
});

def buildDojo (title, creatorId):
    assert K.CURRENT_DOJO_V == 0;
    return dotsi.fy({
        "_id": utils.objectId(),
        "_v": K.CURRENT_DOJO_V,
        #
        # Intro'd in _v0:
        "title": title,
        "scratchpad": "",
        "creatorId": creatorId,
        "createdAt": utils.now(),
    });

############################################################
# Adapting: <-- TODO
############################################################

dojoAdp = dotsi.fy({"adapt": lambda x, y=0: dotsi.fy(x)});

############################################################
# Getting:
############################################################

def getDojo (q, shouldUpdateDb=True):
    "Query traditionally for a single dojo.";
    assert type(q) in [str, dict];
    dojo = db.dojoBox.find_one(q);
    if dojo is None:
        return None;
    return dojoAdp.adapt(dojo, shouldUpdateDb);


def getDojoList (q=None, shouldUpdateDb=True):
    "Query traditionally for multiple dojos.";
    q = q or {};
    assert type(q) is dict;
    adaptWrapper = lambda dojo: (                                       # A wrapper around `adapt`, aware of `shouldUpdateDb`.
        dojoAdp.adapt(dojo, shouldUpdateDb)#, # NO COMMA
    );
    return utils.map(adaptWrapper, db.dojoBox.find(q));

def getDojoCount (q=None):
    return db.dojoBox.count_documents(q or {});

############################################################
# Inserting, Updating & Deleting:
############################################################

def insertDojo (dojo):
    "More or less blindly INSERTS dojo to db.";             # Used primarily for inviting dojos.
    assert validateDojo(dojo);
    #print("inserting dojo: ", dojo);
    dbOut = db.dojoBox.insert_one(dojo);
    assert dbOut.inserted_id == dojo._id;
    return dbOut;

def replaceDojo (dojo):
    "More or less blindly REPLACES dojo in db.";            # Used primarily for updating fname/lname/password etc of logged-in dojos.
    assert validateDojo(dojo);
    dbOut = db.dojoBox.replace_one({"_id": dojo._id}, dojo);
    assert dbOut.matched_count == 1 == dbOut.modified_count;
    return dbOut;

def deleteDojo (dojo):
    "Deletes an unverified, invited.";
    assert validateDojo(dojo);
    dbOut = db.dojoBox.delete_one({"_id": dojo._id});
    assert dbOut.deleted_count == 1;
    return True;

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
