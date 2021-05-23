// npm:
var _ = require("underscore");
var $ = require("jquery");

// loc:
var misc = require("./misc.js");
var {uk, app} = require("./dash-00-def.js");

// RouteApp:
var dl = {"id": "articleLister", "o": {}, "c": {}};            // Article Lister


// Observables & Computeds:
dl.c.articleList = app.o.articleMap.list, // Alias, snap-friendly.

// Open:
dl.open = function () {
    dl.fetchArticleListIfReqd();
};
dl.fetchArticleListIfReqd = async function () {
    if (app.o.articleMap.isFetched.get()) {
        // ==> Already fetched.
        return app.o.articleMap.list();
    }
    // ==> Not yet fetched.
    return await dl.fetchArticleList();
};
dl.fetchArticleList = async function () {
    misc.spinner.start("Fetching Articles ...");
    let resp = await misc.postJson("/articleCon/fetchArticleList", {});
    //misc.alertJson(resp);
    app.o.articleMap.updateMany(resp.articleList);
    app.o.articleMap.isFetched.set(true);
    misc.spinner.stop();
    return resp.articleList;
};

// Creating:
dl.onClick_createArticle = async function () {
    var swalOut = await Swal.fire({
        "title": "Create Article",
        "input": "text",
        "inputLabel": "Enter Article's Title:",
    });
    console.log(swalOut);
    if (! swalOut.isConfirmed) { return null; }
    var dataToSend = {
        "title": swalOut.value,
    };
    misc.spinner.start("Creating ...");
    var resp = await misc.postJson("/articleCon/createArticle", dataToSend);
    var article = resp.article;
    app.o.articleMap.updateOne(article);
    misc.spinner.stop();
    app.router.setInfo({
        "id": "scratchpadr",
        "articleId": article._id,
    });
};

module.exports = dl;
