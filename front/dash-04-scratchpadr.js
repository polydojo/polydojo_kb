// npm:
var _ = require("underscore");
var $ = require("jquery");
var Swal = require('sweetalert2')["default"];

// loc:
var misc = require("./misc.js");
var {uk, app} = require("./dash-00-def.js");

var sp = {"id": "scratchpadr", "o": {}, "c": {}};           // Scratchpad-r

sp.o.pageId = uk.observable(null);

sp.c.page = uk.computed(
    function () {
        var pageId = sp.o.pageId.get();
        if (! pageId) { return null; }  // short ckt.
        var page = app.o.pageMap.get()[pageId];
        if (! page) { return null; }    // short ckt.
        // ==> page found.
        return page
    },
    [sp.o.pageId, app.o.pageMap]
);

sp.open = function (info) {
    sp.o.pageId.set(info.pageId);
    if (! sp.c.page.get()) {
        app.router.openDefault();
    }
};

sp.onSubmit_saveScratch = async function (event) {
    const $scratchText = $(event.currentTarget.scratchText);
    const dataToSend = {
        "pageId": sp.o.pageId.get(),
        "title": sp.c.page.get().title,
        "scratchpad": $scratchText.val(),
    };
    misc.spinner.start("Saving ...");
    const resp = await misc.postJson("/pageCon/updateScratchpad", dataToSend);
    app.o.pageMap.updateOne(resp.page);
    misc.spinner.stop();
};

sp.close = function () {
    sp.o.pageId.set(null);
};

module.exports = sp;
