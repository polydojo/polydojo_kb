// npm:
var _ = require("underscore");
var $ = require("jquery");

// loc:
var misc = require("./misc.js");
var {uk, app} = require("./dash-00-def.js");

// RouteApp:
var dl = {"id": "dojoLister", "o": {}, "c": {}};            // Dojo Lister


// Observables & Computeds:
dl.c.dojoList = app.o.dojoMap.list, // Alias, snap-friendly.

// Open:
dl.open = function () {
    dl.fetchDojoListIfReqd();
};
dl.fetchDojoListIfReqd = async function () {
    if (app.o.dojoMap.isFetched.get()) {
        // ==> Already fetched.
        return app.o.dojoMap.list();
    }
    // ==> Not yet fetched.
    return await dl.fetchDojoList();
};
dl.fetchDojoList = async function () {
    misc.spinner.start("Fetching Dojos ...");
    let resp = await misc.postJson("/dojoCon/fetchDojoList", {});
    //misc.alertJson(resp);
    app.o.dojoMap.updateMany(resp.dojoList);
    app.o.dojoMap.isFetched.set(true);
    misc.spinner.stop();
    return resp.dojoList;
};

// Creating:
dl.onClick_createDojo = async function () {
    var swalOut = await Swal.fire({
        "title": "Create Dojo",
        "input": "text",
        "inputLabel": "Enter Dojo's Title:",
    });
    console.log(swalOut);
    if (! swalOut.isConfirmed) { return null; }
    var dataToSend = {
        "title": swalOut.value,
    };
    misc.spinner.start("Creating ...");
    var resp = await misc.postJson("/dojoCon/createDojo", dataToSend);
    var dojo = resp.dojo;
    app.o.dojoMap.updateOne(dojo);
    misc.spinner.stop();
    app.router.setInfo({
        "id": "scratchpadr",
        "dojoId": dojo._id,
    });
};

module.exports = dl;
