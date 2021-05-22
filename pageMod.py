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

assert K.CURRENT_PAGE_V == 0;
db = dotsi.fy({"pageBox": mongo.db.pageBox});   # Isolate
    
############################################################
# Page building and validation:                            #
############################################################

validatePage = vf.dictOf({
    "_id": utils.isObjectId,
    "_v": lambda x: x == K.CURRENT_PAGE_V,
    #
    # Intro'd in _v0:
    "title": vf.typeIs(str),
    "scratchpad": vf.typeIs(str),
    "creatorId": utils.isObjectId,
    "createdAt": utils.isInty,
});

def buildPage (title, creatorId):
    assert K.CURRENT_PAGE_V == 0;
    return dotsi.fy({
        "_id": utils.objectId(),
        "_v": K.CURRENT_PAGE_V,
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

pageAdp = dotsi.fy({"adapt": lambda x, y=0: dotsi.fy(x)});

############################################################
# Getting:
############################################################

def getPage (q, shouldUpdateDb=True):
    "Query traditionally for a single page.";
    assert type(q) in [str, dict];
    page = db.pageBox.find_one(q);
    if page is None:
        return None;
    return pageAdp.adapt(page, shouldUpdateDb);


def getPageList (q=None, shouldUpdateDb=True):
    "Query traditionally for multiple pages.";
    q = q or {};
    assert type(q) is dict;
    adaptWrapper = lambda page: (                                       # A wrapper around `adapt`, aware of `shouldUpdateDb`.
        pageAdp.adapt(page, shouldUpdateDb)#, # NO COMMA
    );
    return utils.map(adaptWrapper, db.pageBox.find(q));

def getPageCount (q=None):
    return db.pageBox.count_documents(q or {});

############################################################
# Inserting, Updating & Deleting:
############################################################

def insertPage (page):
    "More or less blindly INSERTS page to db.";             # Used primarily for inviting pages.
    assert validatePage(page);
    #print("inserting page: ", page);
    dbOut = db.pageBox.insert_one(page);
    assert dbOut.inserted_id == page._id;
    return dbOut;

def replacePage (page):
    "More or less blindly REPLACES page in db.";            # Used primarily for updating fname/lname/password etc of logged-in pages.
    assert validatePage(page);
    dbOut = db.pageBox.replace_one({"_id": page._id}, page);
    assert dbOut.matched_count == 1 == dbOut.modified_count;
    return dbOut;

def deletePage (page):
    "Deletes an unverified, invited.";
    assert validatePage(page);
    dbOut = db.pageBox.delete_one({"_id": page._id});
    assert dbOut.deleted_count == 1;
    return True;

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
