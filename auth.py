# std:
# n/a

# pip-int:
import dotsi;

# pip-ext:
# n/a

# loc:
import bu;
from constants import K;
import utils;
import userMod;
import articleMod;
import conAlm;

############################################################
# Anti-CSRF related:                                       #
############################################################

def genXCsrfToken (userId):
    return bu.hasher.signWrap(
        data = userId,
        secret = K.ANTI_CSRF_SECRET,
    );

def validateXCsrfToken (xCsrfToken, userId):
    try:
        #print("xCsrfToken = ", repr(xCsrfToken));
        #print(bu.getCookie("userId"));
        unwrappedUserId = bu.hasher.signUnwrap(
            xCsrfToken,
            secret = K.ANTI_CSRF_SECRET,                    # <-- Even though we use `bu.hasher`, we specify an overriding secret.
            maxExpiryInDays = K.REMEMBER_ME_DAY_COUNT,      # <-- Note: Can set to 0 or 0.0001 to see XSRF validation being enforced.
            # ^ This talks about signature-expiry, not cookie expiry.
        );
    except bu.hasher.SignatureInvalidError as e:
        return bu.abort("1. X-CSRF validation failed. Please log out and then log back in.");
    # ==> No unwrapping error.
    if unwrappedUserId != userId:
        return bu.abort("2. X-CSRF validation failed. Please log out and then log back in.");
    # ==> Unwrapped data is as expected.
    return True;

############################################################
# Success response:                                        #
############################################################

def sendAuthSuccessResponse (user, rememberMe=False):
    maxAge = None; # Assumption
    if rememberMe:  # Correction
        maxAge = K.REMEMBER_ME_DAY_COUNT * 24 * 60 * 60;
        # N days * 24 hrs * 60 mins * 60 sec => N days in sec
    signWrapped = bu.setCookie(
        name = "userId",
        data = user._id,
        secret = K.AUTH_COOKIE_SECRET,
        maxAge = maxAge,
    );
    xCsrfToken = genXCsrfToken(user._id);
    bu.setUnsignedCookie(
        name = "xCsrfToken",
        value = xCsrfToken,
        httpOnly = False,
        maxAge = maxAge,
    );
    return {"user": userMod.snipUser(user)};

############################################################
# Getting current user etc.                                #
############################################################

def getSesh (strict=True, validateCsrf=None, req=None):
    "Get sesh (session-like) object with current 'user' property.";
    req = req or bu.request;                                    # Defaults to (global) bu.request.
    if validateCsrf is None:
        validateCsrf = bool(req.method != "GET");               # Default behavior: false for GET, else true.
    # Check the 'userId' cookie:
    userId = bu.getCookie("userId",
        strict=strict, secret=K.AUTH_COOKIE_SECRET, req=req,
    );
    if not userId:
        assert not strict;
        return dotsi.fy({"user": None});
    # ==> Cookie found, signature valid.
    assert userId;
    if validateCsrf:
        # Ref: https://laravel.com/docs/5.8/csrf#csrf-x-csrf-token
        xCsrfToken = req.headers.get("X-Csrf-Token");
        assert validateXCsrfToken(xCsrfToken, userId);
        # ==> CSRF TOKEN IS VALID.
    # ==> CSRF PREVENTED, if applicable.
    user = userMod.getUser(userId);
    assert user and user.isVerified;                        # User shouldn't be able to log-in if not .isVerified. Asserting here.
    if user.isDeactivated:
        # XXX:Note: Below 'log out' should force CLI logout.
        return bu.abort("ACCOUNT DEACTIVATED\n\n" +
            "Your account has been deactivated by your admin." +
            "You shall now proceed to log out." #+
        );
    # ==> User exists, is verified, non-deactivated.
    return dotsi.fy({"user": user});

############################################################
# Access Control: ##########################################
############################################################

alm = conAlm.build(K.USER_ACCESS_LEVEL_LIST);
assert alm.getMinLevel() == "reader";
assert alm.getMaxLevel() == "admin";

def checkIfUserCanReadArticle (article, user):
    canAnyUserRead = article.status in [
        "published_internally", "published_externally",
    ];
    if canAnyUserRead:
        return True;
    # otherwise ...
    if alm.contains(user.accessLevel, "editor"):
        assert user.accessLevel in ["editor", "admin"];
        return True;
    # otherwise ...
    if alm.contains(user.accessLevel, "author"):
        return bool(article.creatorId == user._id);
    # otherwise ...
    assert user.accessLevel == "reader";
    assert article.status == "draft";
    return False;

def getUserReadableArticleList (user):
    return utils.filter(
        articleMod.getArticleList({}),
        lambda a: checkIfUserCanReadArticle(a, user),
    );

#XXX:Untested, commented out.
#def getUserReadableArticleList (user):
#    if alm.contains(user.accessLevel, "editor"):
#        assert user.accessLevel in ["editor", "admin"];
#        return articleMod.getArticleList({});
#    # ==> Not editor+
#    if alm.exceeds("author", user.accessLevel):
#        assert user.accessLevel == "reader";
#        return articleMod.getArticleList({
#            "status": {"$ne": "draft"},
#        });
#    # ==> Not author+
#    assert user.accessLevel == "author";
#        return articleMod.getArticleList({
#            "$or": [
#                {"status": {"$ne": "draft"}},
#                {"creatorId": user._id},
#            ],
#        });

def validateAccessLevel(reqdAccessLevel, user):
    ok = alm.contains(user.accessLevel, reqdAccessLevel);
    if not ok:
        raise bu.abort("Access level insufficient.");
    # otherwise ... => ok
    return True;

def checkArticleEditable (article, user):
    if alm.contains(user.accessLevel, "editor"):
        assert user.accessLevel in ["editor", "admin"];
        return True;    # Short ckt.
    if not alm.contains(user.accessLevel, "author"):
        assert user.accessLevel == "reader";
        return False;   # Short ckt.
    assert user.accessLevel == "author";
    return bool(article.creatorId == user._id);

def validateArticleEditable (article, user):
    if not checkArticleEditable(article, user):
        raise bu.abort("Access level insufficient.");
    # otherwise ...
    return True;
validateCategoryEditable = validateArticleEditable;         # <-- For now, both article & category objs have `.creatorId`.

validateArticleDeletable = validateArticleEditable;         # <-- For now, article deletability <==> editability.
validateCategoryDeletable = validateCategoryEditable;       # <-- For now, category deletability <==> editability.


# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
