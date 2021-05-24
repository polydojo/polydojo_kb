// npm:
var _ = require("underscore");
var $ = require("jquery");
var Swal = require('sweetalert2')["default"];

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
};

ae.onSubmit_saveArticle = async function (event) {
    const $bodyArea = $(event.currentTarget.bodyArea);
    const dataToSend = {
        "articleId": ae.o.articleId.get(),
        "title": ae.c.article.get().title,
        "body": $bodyArea.val(),
    };
    misc.spinner.start("Saving ...");
    const resp = await misc.postJson("/articleCon/updateArticle", dataToSend);
    app.o.articleMap.updateOne(resp.article);
    misc.spinner.stop();
};

ae.close = function () {
    ae.o.articleId.set(null);
};

module.exports = ae;
