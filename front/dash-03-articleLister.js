// npm:
var _ = require("underscore");
var $ = require("jquery");

// loc:
var misc = require("./misc.js");
var {uk, app} = require("./dash-00-def.js");

// RouteApp:
var al = {"id": "articleLister", "o": {}, "c": {}};


// Observables & Computeds:
al.c.articleList = app.o.articleMap.list, // Alias, snap-friendly.

// Open:
al.open = function () {
    al.fetchArticleListIfReqd();
};
al.fetchArticleListIfReqd = async function () {
    if (app.o.articleMap.isFetched.get()) {
        // ==> Already fetched.
        return app.o.articleMap.list();
    }
    // ==> Not yet fetched.
    return await al.fetchArticleList();
};
al.fetchArticleList = async function () {
    misc.spinner.start("Fetching Articles ...");
    let resp = await misc.postJson("/articleCon/fetchArticleList", {});
    //misc.alertJson(resp);
    app.o.articleMap.updateMany(resp.articleList);
    app.o.articleMap.isFetched.set(true);
    misc.spinner.stop();
    return resp.articleList;
};

// Creating:
al.onClick_createArticle = async function () {
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
        "id": "articleEditor",
        "articleId": article._id,
    });
};

module.exports = al;
