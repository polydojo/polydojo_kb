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

assert K.CURRENT_ARTICLE_V == 1;
db = dotsi.fy({"articleBox": mongo.db.articleBox});   # Isolate
    
############################################################
# Article building and validation:                            #
############################################################

validateArticle = vf.dictOf({
    "_id": utils.isObjectId,
    "_v": lambda x: x == K.CURRENT_ARTICLE_V,
    #
    # Intro'd in _v0:
    #
    "title": vf.typeIs(str),
    #"scratchpad": vf.typeIs(str),  -- Renamed in _v1 to 'body'
    "creatorId": utils.isObjectId,
    "createdAt": utils.isInty,
    #
    # Intro'd in _v1:
    #
    "body": vf.typeIs(str),
    "categoryId": utils.isBlankOrObjectId,
    "sectionId": utils.isBlankOrObjectId,
});

def buildArticle (creatorId, title=""):
    assert K.CURRENT_ARTICLE_V == 1;
    return dotsi.fy({
        "_id": utils.objectId(),
        "_v": K.CURRENT_ARTICLE_V,
        #
        # Intro'd in _v0:
        #
        "title": title,
        #"scratchpad": "",           -- Renamed in _v1 to 'body'
        "creatorId": creatorId,
        "createdAt": utils.now(),
        #
        # Intro'd in _v1:
        #
        "body": "",
        "categoryId": "",   # blank => Untitled, topmost category.
        "sectionId": "",    # blank => Untitled, topmost section.
    });

############################################################
# Adapting:
############################################################

articleAdp = stdAdpBuilder.buildStdAdp(
    str_fooBox = "articleBox",
    str_CURRENT_FOO_V = "CURRENT_ARTICLE_V",
    int_CURRENT_FOO_V = K.CURRENT_ARTICLE_V,
    func_validateFoo = validateArticle,
);

@articleAdp.addStepAdapter
def stepAdapterCore_from_0_to_1 (articleY):                 # Note: This _CANNOT_ be a lambda as `addStepAdapter` relies on .__name__
    # article._v: 0 --> 1
    # Renamed:
    #   ~ scratchpad --> body
    # Added:
    #   + categoryId
    #   + sectionId
    articleY.update({
        "body": articleY.pop("scratchpad"),
        "categoryId": "",
        "sectionId": "",
    });

#@articleAdp.addStepAdapter
#def stepAdapterCore_from_0_to_1 (articleY):                # Note: This _CANNOT_ be a lambda as `addStepAdapter` relies on .__name__
#    # article._v: X --> Y
#    # Added:
#    #   + foo
#    articleY.update({
#        "foo": "foobar",
#    });

assert articleAdp.getStepCount() == K.CURRENT_ARTICLE_V;

# Adaptation Checklist:
# Assertions will help you.
# You'll need to look at:
#   + constants.py
#   + articleMod.py
#       + top (K) assertion
#       + define stepAdapterCore_from_X_to_Y
#       + modify builder/s as needed
#       + modify validator/s as needed
#       + modify snip/s if any, as needed
#   + articleCon.py and others:
#       + modify funcs that call articleMod's funcs.

############################################################
# Getting:
############################################################

def getArticle (q, shouldUpdateDb=True):
    "Query traditionally for a single article.";
    assert type(q) in [str, dict];
    article = db.articleBox.find_one(q);
    if article is None:
        return None;
    return articleAdp.adapt(article, shouldUpdateDb);


def getArticleList (q=None, shouldUpdateDb=True):
    "Query traditionally for multiple articles.";
    q = q or {};
    assert type(q) is dict;
    adaptWrapper = lambda article: (                                       # A wrapper around `adapt`, aware of `shouldUpdateDb`.
        articleAdp.adapt(article, shouldUpdateDb)#, # NO COMMA
    );
    return utils.map(adaptWrapper, db.articleBox.find(q));

def getArticleCount (q=None):
    return db.articleBox.count_documents(q or {});

############################################################
# Inserting, Updating & Deleting:
############################################################

def insertArticle (article):
    "More or less blindly INSERTS article to db.";             # Used primarily for inviting articles.
    assert validateArticle(article);
    #print("inserting article: ", article);
    dbOut = db.articleBox.insert_one(article);
    assert dbOut.inserted_id == article._id;
    return dbOut;

def replaceArticle (article):
    "More or less blindly REPLACES article in db.";            # Used primarily for updating fname/lname/password etc of logged-in articles.
    assert validateArticle(article);
    dbOut = db.articleBox.replace_one({"_id": article._id}, article);
    assert dbOut.matched_count == 1 == dbOut.modified_count;
    return dbOut;

def deleteArticle (article):
    "Deletes an unverified, invited.";
    assert validateArticle(article);
    dbOut = db.articleBox.delete_one({"_id": article._id});
    assert dbOut.deleted_count == 1;
    return True;

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
