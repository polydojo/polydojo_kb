# std:
# n/a

# pip-ext:
# n/a

# pip-int:
import dotsi;

# loc:
import bu;
from appDef import app;
from constants import K;
import articleMod;
import utils;
import auth;


@app.post("/articleCon/createArticle")
def post_articleCon_createArticle ():
    jdata = bu.get_jdata(ensure="title");
    sesh = auth.getSesh();
    article = articleMod.buildArticle(
        title = jdata.title,
        creatorId = sesh.user._id,
    );
    assert articleMod.validateArticle(article);
    articleMod.insertArticle(article);
    return {"article": article};

@app.post("/articleCon/fetchArticleList")
def post_articleCon_fetchArticleList ():
    sesh = auth.getSesh();
    return {"articleList": articleMod.getArticleList()};

@app.post("/articleCon/updateScratchpad")
def post_articleCon_updateArticle ():
    jdata = bu.get_jdata(ensure="""
        articleId, title, scratchpad,
    """);
    sesh = auth.getSesh();
    article = articleMod.getArticle(jdata.articleId);
    article.update({
        "title": jdata.title,
        "scratchpad": jdata.scratchpad,
    });
    assert articleMod.validateArticle(article);
    articleMod.replaceArticle(article);
    return {"article": article};

@app.post("/articleCon/deleteArticle")
def post_articleCon_updateArticle ():
    jdata = bu.get_jdata(ensure="articleId");
    sesh = auth.getSesh();
    article = articleMod.getArticle(jdata.articleId);
    # TODO: Delete any inner/linked documents.
    articleMod.deleteArticle(article);
    return {"deletedArticleId": article._id};

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
