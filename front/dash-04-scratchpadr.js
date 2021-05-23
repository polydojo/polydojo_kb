// npm:
var _ = require("underscore");
var $ = require("jquery");
var Swal = require('sweetalert2')["default"];

// loc:
var misc = require("./misc.js");
var {uk, app} = require("./dash-00-def.js");

var sp = {"id": "scratchpadr", "o": {}, "c": {}};           // Scratchpad-r

sp.o.articleId = uk.observable(null);

sp.c.article = uk.computed(
    function () {
        var articleId = sp.o.articleId.get();
        if (! articleId) { return null; }  // short ckt.
        var article = app.o.articleMap.get()[articleId];
        if (! article) { return null; }    // short ckt.
        // ==> article found.
        return article
    },
    [sp.o.articleId, app.o.articleMap]
);

sp.open = function (info) {
    sp.o.articleId.set(info.articleId);
    if (! sp.c.article.get()) {
        app.router.openDefault();
    }
};

sp.onSubmit_saveScratch = async function (event) {
    const $scratchText = $(event.currentTarget.scratchText);
    const dataToSend = {
        "articleId": sp.o.articleId.get(),
        "title": sp.c.article.get().title,
        "scratchpad": $scratchText.val(),
    };
    misc.spinner.start("Saving ...");
    const resp = await misc.postJson("/articleCon/updateScratchpad", dataToSend);
    app.o.articleMap.updateOne(resp.article);
    misc.spinner.stop();
};

sp.close = function () {
    sp.o.articleId.set(null);
};

module.exports = sp;
