# std:
import hashlib;
import hmac;
import re;
import secrets;

# pip-ext:
import pymongo;

# pip-int:
import dotsi;
import vf;

# loc:
from constants import K;
import mongo;
import utils;
import bu;
import hashUp;
import stdAdpBuilder;

############################################################
# Assertions & indexing:                                   #
############################################################

assert K.CURRENT_USER_V == 1;
db = dotsi.fy({"userBox": mongo.db.userBox});   # Isolate
db.userBox.create_index([
    ("email", pymongo.ASCENDING),
], unique=True, name=K.USER_EMAIL_INDEX_NAME);  # Unique
    
############################################################
# User building and validation:                            #
############################################################

def genVeriCode ():
    return secrets.token_urlsafe();

_validateUserFormat = vf.dictOf({
    "_id": utils.isObjectId,
    "_v": lambda x: x == K.CURRENT_USER_V,
    #
    # Intro'd in _v0:
    "fname": vf.typeIs(str),
    "lname": vf.typeIs(str),
    "email": vf.allOf(
        vf.patternIs(K.EMAIL_RE),
        lambda x: x == x.lower(),
    ),
    "hpw": vf.typeIs(str),  # Hashed PW
    "createdAt": utils.isInty,
    "isVerified": vf.typeIs(bool),
    "hVeriCode": vf.typeIs(str),
    "inviterId": lambda x: x == "" or utils.isObjectId(x),
    "isDeactivated": vf.typeIs(bool),
    "hResetPw": vf.typeIs(str), # Hashed Reset-PW
    "resetPwExpiresAt": utils.isInty,
    "isRootAdmin": vf.typeIs(bool),
    #
    # Intro'd in _v1:
    #
    "accessLevel": lambda x: x in K.USER_ACCESS_LEVEL_LIST,
});

def validateUser (user):
    assert _validateUserFormat(user);
    if user.isRootAdmin:
        assert user.accessLevel == "admin";
    return True;

def buildUser (
        email, fname, lname="", pw="", isRootAdmin=False,
        isVerified=False, inviterId="", veriCode=None,
        accessLevel = K.USER_ACCESS_LEVEL_LIST[0],
    ):
    assert K.CURRENT_USER_V == 1;
    assert fname and email;
    assert type(fname) == type(email) == str and "@" in email;
    userId = utils.objectId();
    hpw = utils.hashPw(pw) if pw else "";
    veriCode = veriCode or genVeriCode();
    return dotsi.fy({
        "_id": userId,
        "_v": K.CURRENT_USER_V,
        #
        # Intro'd in _v0:
        #
        "fname": fname,
        "lname": lname,
        "email": email,
        "hpw": hpw,
        "createdAt": utils.now(),
        "isVerified": isVerified,
        "hVeriCode": utils.hashPw(veriCode),
        "inviterId": inviterId,
        "isDeactivated": False,
        "hResetPw": "",
        "resetPwExpiresAt": 0,
        "isRootAdmin": isRootAdmin,
        #
        # Intro'd in _v1:
        #
        "accessLevel": accessLevel,
    });

def snipUser (user):
    sensitiveKeyList = utils.readKeyz("""
        hpw, hVeriCode, hResetPw, resetPwExpiresAt,
    """);
    return utils.pick(user, lambda k: k not in sensitiveKeyList);

############################################################
# Adapting:
############################################################

userAdp = stdAdpBuilder.buildStdAdp(
    str_fooBox = "userBox",
    str_CURRENT_FOO_V = "CURRENT_USER_V",
    int_CURRENT_FOO_V = K.CURRENT_USER_V,
    func_validateFoo = validateUser,
);

@userAdp.addStepAdapter
def stepAdapterCore_from_0_to_1 (userY):                    # Note: This _CANNOT_ be a lambda as `addStepAdapter` relies on .__name__
    # user._v: 0 --> 1
    # Added:
    #   + accessLevel
    i = -1 if userY.isRootAdmin else 0;                     # Highest (last index) access level for root admin, else lowest.
    userY.update({
        "accessLevel": K.USER_ACCESS_LEVEL_LIST[i],
    });

#@userAdp.addStepAdapter
#def stepAdapterCore_from_X_to_Y (userY):                   # Note: This _CANNOT_ be a lambda as `addStepAdapter` relies on .__name__
#    # user._v: X --> Y
#    # Added:
#    #   + foo
#    userY.update({
#        "foo": "foobar",
#    });

assert userAdp.getStepCount() == K.CURRENT_USER_V;

# Adaptation Checklist:
# Assertions will help you.
# You'll need to look at:
#   + constants.py
#   + userMod.py
#       + top (K) assertion
#       + define stepAdapterCore_from_X_to_Y
#       + modify builder/s as needed
#       + modify validator/s as needed
#       + modify snip/s if any, as needed
#   + userCon.py and others:
#       + modify funcs that call userMod's funcs.

############################################################
# Getting:
############################################################

def getUser (q, shouldUpdateDb=True):
    "Query traditionally for a single user.";
    assert type(q) in [str, dict];
    user = db.userBox.find_one(q);
    if user is None:
        return None;
    return userAdp.adapt(user, shouldUpdateDb);

def getUserByEmail(email, shouldUpdateDb=True):
    "Get a user by email.";
    return getUser({"email": email}, shouldUpdateDb);

def getUserList (q=None, shouldUpdateDb=True):
    "Query traditionally. No special treatment for emails.";
    q = q or {};
    assert type(q) is dict;
    adaptWrapper = lambda user: (                                       # A wrapper around `adapt`, aware of `shouldUpdateDb`.
        userAdp.adapt(user, shouldUpdateDb)#, # NO COMMA
    );
    return utils.map(adaptWrapper, db.userBox.find(q));

def getUserCount (q=None):
    return db.userBox.count_documents(q or {});


############################################################
# Inserting, Updating & Deleting:
############################################################

def insertUser (user):
    "More or less blindly INSERTS user to db.";             # Used primarily for inviting users.
    assert validateUser(user);
    #print("inserting user: ", user);
    dbOut = db.userBox.insert_one(user);
    assert dbOut.inserted_id == user._id;
    return dbOut;

def replaceUser (user):
    "More or less blindly REPLACES user in db.";            # Used primarily for updating fname/lname/password etc of logged-in users.
    assert validateUser(user);
    dbOut = db.userBox.replace_one({"_id": user._id}, user);
    assert dbOut.matched_count == 1 == dbOut.modified_count;
    return dbOut;

def upsertUser (user):
    "More or less blindly upserts user to db.";
    assert validateUser(user);
    #print("upserting user: ", user);
    dbOut = db.userBox.replace_one(
        {"_id": user._id},
        user,
        upsert=True,
    );
    assert (
        dbOut.upserted_id == user._id or # _OR_
        dbOut.matched_count == 1 == dbOut.modified_count # or
    );
    return dbOut;

def deleteUser (user):
    "Deletes an unverified, invited.";
    assert validateUser(user);
    assert not user.isVerified;                             # Assert not already verified.
    dbOut = db.userBox.delete_one({
        "_id": user._id,
        "isVerified": False,
    });
    assert dbOut.deleted_count in [0, 1];                   # Assert max 1 deletion.
    if dbOut.deleted_count == 0:
        raise NotImplementedError("User deletion failed.");
    # ==> Non-zero records deleted.
    assert dbOut.deleted_count == 1;
    return True;

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
