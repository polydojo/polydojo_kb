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
import dojoMod;
import utils;
import auth;


@app.post("/dojoCon/createDojo")
def post_dojoCon_createDojo ():
    jdata = bu.get_jdata(ensure="title");
    sesh = auth.getSesh();
    dojo = dojoMod.buildDojo(
        title = jdata.title,
        creatorId = sesh.user._id,
    );
    assert dojoMod.validateDojo(dojo);
    dojoMod.insertDojo(dojo);
    return {"dojo": dojo};

@app.post("/dojoCon/fetchDojoList")
def post_dojoCon_fetchDojoList ():
    sesh = auth.getSesh();
    return {"dojoList": dojoMod.getDojoList()};

@app.post("/dojoCon/updateScratchpad")
def post_dojoCon_updateDojo ():
    jdata = bu.get_jdata(ensure="""
        dojoId, title, scratchpad,
    """);
    sesh = auth.getSesh();
    dojo = dojoMod.getDojo(jdata.dojoId);
    dojo.update({
        "title": jdata.title,
        "scratchpad": jdata.scratchpad,
    });
    assert dojoMod.validateDojo(dojo);
    dojoMod.replaceDojo(dojo);
    return {"dojo": dojo};

@app.post("/dojoCon/deleteDojo")
def post_dojoCon_updateDojo ():
    jdata = bu.get_jdata(ensure="dojoId");
    sesh = auth.getSesh();
    dojo = dojoMod.getDojo(jdata.dojoId);
    # TODO: Delete any inner/linked documents.
    dojoMod.deleteDojo(dojo);
    return {"deletedDojoId": dojo._id};

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
