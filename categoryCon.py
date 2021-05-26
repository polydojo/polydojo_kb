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
import categoryMod;
import utils;
import auth;


@app.post("/categoryCon/createCategory")
def post_categoryCon_createCategory ():
    jdata = bu.get_jdata(ensure="name rank parentId");
    sesh = auth.getSesh();
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



# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
