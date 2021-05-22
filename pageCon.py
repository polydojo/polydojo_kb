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
import pageMod;
import utils;
import auth;


@app.post("/pageCon/createPage")
def post_pageCon_createPage ():
    jdata = bu.get_jdata(ensure="title");
    sesh = auth.getSesh();
    page = pageMod.buildPage(
        title = jdata.title,
        creatorId = sesh.user._id,
    );
    assert pageMod.validatePage(page);
    pageMod.insertPage(page);
    return {"page": page};

@app.post("/pageCon/fetchPageList")
def post_pageCon_fetchPageList ():
    sesh = auth.getSesh();
    return {"pageList": pageMod.getPageList()};

@app.post("/pageCon/updateScratchpad")
def post_pageCon_updatePage ():
    jdata = bu.get_jdata(ensure="""
        pageId, title, scratchpad,
    """);
    sesh = auth.getSesh();
    page = pageMod.getPage(jdata.pageId);
    page.update({
        "title": jdata.title,
        "scratchpad": jdata.scratchpad,
    });
    assert pageMod.validatePage(page);
    pageMod.replacePage(page);
    return {"page": page};

@app.post("/pageCon/deletePage")
def post_pageCon_updatePage ():
    jdata = bu.get_jdata(ensure="pageId");
    sesh = auth.getSesh();
    page = pageMod.getPage(jdata.pageId);
    # TODO: Delete any inner/linked documents.
    pageMod.deletePage(page);
    return {"deletedPageId": page._id};

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
