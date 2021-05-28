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


@app.get("/")
@app.get("/category/<categoryId>")
def get_kb_category (categoryId=""):
    category = K.TOP_BLANK_CATEGORY;        # assumption
    if categoryId != "":
        category = categoryMod.getCategory(categoryId);
        assert category and category._id;   # correction
    subcategoryList = categoryMod.getCategoryList({
        "parentId": categoryId,
    });
    articleList = articleMod.getArticleList({
        "status": "published_externally",
        "categoryId": categoryId,
    });
    return bu.render("extern-kb-category.html", **{
        "category": category,
        "subcategoryList": subcategoryList,
        "articleList": articleList,
    });

@app.get("/article/<articleId>")
def get_kb_article (articleId):
    article = articleMod.getArticle({
        "_id": articleId,
        "status": "published_externally",
    });
    if not article:
        raise bu.abort("Artile not found. " + 
            "It may have been moved or deleted." #+
        );
    # ==> Found externally published article.
    return bu.render("extern-kb-article.html", **({
        "article": article,
        "bleachUp": bleachUp,
    }));

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
