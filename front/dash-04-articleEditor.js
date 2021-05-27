// npm:
var _ = require("underscore");
var $ = require("jquery");
var Swal = require('sweetalert2')["default"];
var __summernote = require("summernote/dist/summernote-bs4.min.js");

window.$ = $;

// loc:
var misc = require("./misc.js");
var {uk, app} = require("./dash-00-def.js");

var ae = {"id": "articleEditor", "o": {}, "c": {}};

ae.o.articleId = uk.observable(null);

ae.c.article = uk.computed(
    function () {
        var articleId = ae.o.articleId.get();
        if (! articleId) { return null; }  // short ckt.
        var article = app.o.articleMap.get()[articleId];
        if (! article) { return null; }    // short ckt.
        // ==> article found.
        return article
    },
    [ae.o.articleId, app.o.articleMap]
);

ae.open = function (info) {
    ae.o.articleId.set(info.articleId);
    if (! ae.c.article.get()) {
        app.router.openDefault();
    }
    $("#summernote_bodyArea").summernote({
        "minHeight": 300,
        "focus": false,     // No auto-focus
    });
};

ae.onSubmit_saveArticle = async function (event) {
    const form = event.currentTarget;
    const dataToSend = {
        "articleId": ae.o.articleId.get(),
        "title": form.title.value,
        "body": form.bodyArea.value,
        "categoryId": form.categoryId.value,
        "status": form.status.value,
    };
    misc.spinner.start("Saving ...");
    const resp = await misc.postJson("/articleCon/updateArticle", dataToSend);
    app.o.articleMap.updateOne(resp.article);
    misc.spinner.stop();
};

ae.close = function () {
    ae.o.articleId.set(null);
    $("#summernote_bodyArea").summernote("destroy");
};

module.exports = ae;
