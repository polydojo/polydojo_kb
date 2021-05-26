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
import categoryMod;
import utils;
import auth;
import bleachUp;


@app.post("/articleCon/createArticle")
def post_articleCon_createArticle ():
    jdata = bu.get_jdata(ensure="title");
    sesh = auth.getSesh();
    article = articleMod.buildArticle(
        creatorId = sesh.user._id,
        title = jdata.title,
    );
    assert articleMod.validateArticle(article);
    articleMod.insertArticle(article);
    return {"article": article};

@app.post("/articleCon/fetchArticleList")
def post_articleCon_fetchArticleList ():
    sesh = auth.getSesh();
    return {"articleList": articleMod.getArticleList()};

@app.post("/articleCon/updateArticle")
def post_articleCon_updateArticle ():
    jdata = bu.get_jdata(ensure="""
        articleId, title, body, categoryId,
    """);
    sesh = auth.getSesh();
    oldArticle = articleMod.getArticle(jdata.articleId);    # old => before update
    assert oldArticle;
    if jdata.categoryId:
        newCategory = categoryMod.getCategory(jdata.categoryId);
        assert newCategory;
    newArticle = utils.deepCopy(oldArticle);                # new => after update
    newArticle.update({
        "title": jdata.title,
        "body": bleachUp.bleachHtml(jdata.body),
        "categoryId": jdata.categoryId,
    });
    assert articleMod.validateArticle(newArticle);
    if oldArticle != newArticle:
        articleMod.replaceArticle(newArticle);
    return {"article": newArticle};

@app.post("/articleCon/deleteArticle")
def post_articleCon_updateArticle ():
    jdata = bu.get_jdata(ensure="articleId");
    sesh = auth.getSesh();
    article = articleMod.getArticle(jdata.articleId);
    # TODO: Delete any inner/linked documents.
    articleMod.deleteArticle(article);
    return {"deletedArticleId": article._id};

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
