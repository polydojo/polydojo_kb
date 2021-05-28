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


@app.post("/categoryCon/createCategory")
def post_categoryCon_createCategory ():
    jdata = bu.get_jdata(ensure="name rank parentId");
    sesh = auth.getSesh();
    assert auth.validateAccessLevel("author", sesh.user);
    category = categoryMod.buildCategory(
        creatorId = sesh.user._id,
        name = jdata.name,
        rank = jdata.rank,
        parentId = jdata.parentId,
    );
    assert categoryMod.validateCategory(category);
    categoryMod.insertCategory(category);
    return {"category": category};

@app.post("/categoryCon/fetchCategoryList")
def post_categoryCon_fetchCategoryList ():
    sesh = auth.getSesh();
    return {"categoryList": categoryMod.getCategoryList()};

@app.post("/categoryCon/editCategory")
def post_categoryCon_editCategory ():
    jdata = bu.get_jdata(ensure="categoryId name rank parentId");
    sesh = auth.getSesh();
    oldCategory = categoryMod.getCategory(jdata.categoryId);    # old => before update
    assert oldCategory and oldCategory._id;
    assert auth.validateCategoryEditable(oldCategory, sesh.user);
    # TODO: Disallow mutually-infinitely-recursive category parents.
    # Eg.   catA.parent -> catB;  &  catB.parent -> catA;
    if jdata.parentId and jdata.parentId != oldCategory.parentId:
        assert jdata.categoryId != jdata.parentId;
        newKaParent = categoryMod.getCategory(jdata.parentId);
        assert newKaParent;
    newCategory = utils.deepCopy(oldCategory);                  # new => after update
    newCategory.update({
        "name": jdata.name,
        "rank": jdata.rank,
        "parentId": jdata.parentId,
    });
    assert categoryMod.validateCategory(newCategory);
    if oldCategory != newCategory:
        categoryMod.replaceCategory(newCategory);
    return {"category": newCategory};

@app.post("/categoryCon/deleteCategory")
def post_categoryCon_deleteCategory ():
    jdata = bu.get_jdata(ensure="categoryId");
    sesh = auth.getSesh();
    category = categoryMod.getCategory(jdata.categoryId);
    assert category;
    assert auth.validateCategoryDeletable(category, sesh.user);
    articleCount = articleMod.getArticleCount({
        "categoryId": category._id,
    });
    childCategoryCount = categoryMod.getCategoryCount({
        "parentId": category._id,                               # i.e. child.parentId == category._id;
    });
    if not (articleCount == 0 == childCategoryCount):
        return bu.abort("Can't delete non-empty categories.");
    assert articleCount == 0 == childCategoryCount;
    categoryMod.deleteCategory(category);
    return {"deletedCategoryId": category._id};

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
