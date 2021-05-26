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
import stdAdpBuilder;

############################################################
# Assertions & prelims:                                    #
############################################################

assert K.CURRENT_CATEGORY_V == 0;
db = dotsi.fy({"categoryBox": mongo.db.categoryBox});   # Isolate
    
############################################################
# Category building and validation:                        #
############################################################

validateCategory = vf.dictOf({
    "_id": utils.isObjectId,
    "_v": lambda x: x == K.CURRENT_CATEGORY_V,
    #
    # Intro'd in _v0:
    #
    "name": vf.typeIs(str),
    "rank": utils.isNonNegativeNumber,      # 0+, inty or float.
    "parentId": utils.isBlankOrObjectId,    # "" => no parent => top
    "creatorId": utils.isObjectId,
    "createdAt": utils.isInty,
});

def buildCategory (creatorId, name="", rank=0, parentId=""):
    assert K.CURRENT_CATEGORY_V == 0;
    return dotsi.fy({
        "_id": utils.objectId(),
        "_v": K.CURRENT_CATEGORY_V,
        #
        # Intro'd in _v0:
        #
        "name": name,
        "rank": rank,
        "parentId": parentId,
        "creatorId": creatorId,
        "createdAt": utils.now(),
    });

############################################################
# Adapting:
############################################################

categoryAdp = stdAdpBuilder.buildStdAdp(
    str_fooBox = "categoryBox",
    str_CURRENT_FOO_V = "CURRENT_CATEGORY_V",
    int_CURRENT_FOO_V = K.CURRENT_CATEGORY_V,
    func_validateFoo = validateCategory,
);

#@categoryAdp.addStepAdapter
#def stepAdapterCore_from_0_to_1 (categoryY):                 # Note: This _CANNOT_ be a lambda as `addStepAdapter` relies on .__name__
#    # category._v: X --> Y
#    # Added:
#    #   + foo
#    categoryY.update({
#        "foo": "foobar",
#    });

assert categoryAdp.getStepCount() == K.CURRENT_CATEGORY_V;

# Adaptation Checklist:
# Assertions will help you.
# You'll need to look at:
#   + constants.py
#   + categoryMod.py
#       + top (K) assertion
#       + define stepAdapterCore_from_X_to_Y
#       + modify builder/s as needed
#       + modify validator/s as needed
#       + modify snip/s if any, as needed
#   + categoryCon.py and others:
#       + modify funcs that call categoryMod's funcs.

############################################################
# Getting:
############################################################

def getCategory (q, shouldUpdateDb=True):
    "Query traditionally for a single category.";
    assert type(q) in [str, dict];
    category = db.categoryBox.find_one(q);
    if category is None:
        return None;
    return categoryAdp.adapt(category, shouldUpdateDb);


def getCategoryList (q=None, shouldUpdateDb=True):
    "Query traditionally for multiple categorys.";
    q = q or {};
    assert type(q) is dict;
    adaptWrapper = lambda category: (                                       # A wrapper around `adapt`, aware of `shouldUpdateDb`.
        categoryAdp.adapt(category, shouldUpdateDb)#, # NO COMMA
    );
    return utils.map(adaptWrapper, db.categoryBox.find(q));

def getCategoryCount (q=None):
    return db.categoryBox.count_documents(q or {});

############################################################
# Inserting, Updating & Deleting:
############################################################

def insertCategory (category):
    "More or less blindly INSERTS category to db.";
    assert validateCategory(category);
    #print("inserting category: ", category);
    dbOut = db.categoryBox.insert_one(category);
    assert dbOut.inserted_id == category._id;
    return dbOut;

def replaceCategory (category):
    "More or less blindly REPLACES category in db.";
    assert validateCategory(category);
    dbOut = db.categoryBox.replace_one({"_id": category._id}, category);
    assert dbOut.matched_count == 1 == dbOut.modified_count;
    return dbOut;

def deleteCategory (category):
    "Deletes an unverified, invited.";
    assert validateCategory(category);
    dbOut = db.categoryBox.delete_one({"_id": category._id});
    assert dbOut.deleted_count == 1;
    return True;

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
