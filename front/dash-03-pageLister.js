// npm:
var _ = require("underscore");
var $ = require("jquery");

// loc:
var misc = require("./misc.js");
var {uk, app} = require("./dash-00-def.js");

// RouteApp:
var dl = {"id": "pageLister", "o": {}, "c": {}};            // Page Lister


// Observables & Computeds:
dl.c.pageList = app.o.pageMap.list, // Alias, snap-friendly.

// Open:
dl.open = function () {
    dl.fetchPageListIfReqd();
};
dl.fetchPageListIfReqd = async function () {
    if (app.o.pageMap.isFetched.get()) {
        // ==> Already fetched.
        return app.o.pageMap.list();
    }
    // ==> Not yet fetched.
    return await dl.fetchPageList();
};
dl.fetchPageList = async function () {
    misc.spinner.start("Fetching Pages ...");
    let resp = await misc.postJson("/pageCon/fetchPageList", {});
    //misc.alertJson(resp);
    app.o.pageMap.updateMany(resp.pageList);
    app.o.pageMap.isFetched.set(true);
    misc.spinner.stop();
    return resp.pageList;
};

// Creating:
dl.onClick_createPage = async function () {
    var swalOut = await Swal.fire({
        "title": "Create Page",
        "input": "text",
        "inputLabel": "Enter Page's Title:",
    });
    console.log(swalOut);
    if (! swalOut.isConfirmed) { return null; }
    var dataToSend = {
        "title": swalOut.value,
    };
    misc.spinner.start("Creating ...");
    var resp = await misc.postJson("/pageCon/createPage", dataToSend);
    var page = resp.page;
    app.o.pageMap.updateOne(page);
    misc.spinner.stop();
    app.router.setInfo({
        "id": "scratchpadr",
        "pageId": page._id,
    });
};

module.exports = dl;
