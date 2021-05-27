// npm:
var _ = require("underscore");
var $ = require("jquery");

window.$ = $;

// loc:
var misc = require("./misc.js");
var {uk, app} = require("./dash-00-def.js");

var av = {"id": "articleViewer", "o": {}, "c": {}};

av.o.articleId = uk.observable(null);

av.c.article = uk.computed(
    // Very similar to corresponding func in articleEditor
    function () {
        var articleId = av.o.articleId.get();
        if (! articleId) { return null; }  // short ckt.
        var article = app.o.articleMap.get()[articleId];
        if (! article) { return null; }    // short ckt.
        // ==> article found.
        return article
    },
    [av.o.articleId, app.o.articleMap]
);

av.open = async function (info) {
    // Very similar to corresponding func in articleEditor
    await app.articleLister.fetchCategoryListIfReqd();
    await app.articleLister.fetchArticleListIfReqd();
    av.o.articleId.set(info.articleId);
    if (! av.c.article.get()) {
        app.router.openDefault();
    }
};

av.close = function () {
    av.o.articleId.set(null);
};

module.exports = av;
