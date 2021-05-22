// npm:
var _ = require("underscore");
var $ = require("jquery");
var Swal = require('sweetalert2')["default"];

// loc:
var misc = require("./misc.js");
var {uk, app} = require("./dash-00-def.js");

var sp = {"id": "scratchpadr", "o": {}, "c": {}};           // Scratchpad-r

sp.o.dojoId = uk.observable(null);

sp.c.dojo = uk.computed(
    function () {
        var dojoId = sp.o.dojoId.get();
        if (! dojoId) { return null; }  // short ckt.
        var dojo = app.o.dojoMap.get()[dojoId];
        if (! dojo) { return null; }    // short ckt.
        // ==> dojo found.
        return dojo
    },
    [sp.o.dojoId, app.o.dojoMap]
);

sp.open = function (info) {
    sp.o.dojoId.set(info.dojoId);
    if (! sp.c.dojo.get()) {
        app.router.openDefault();
    }
};

sp.onSubmit_saveScratch = async function (event) {
    const $scratchText = $(event.currentTarget.scratchText);
    const dataToSend = {
        "dojoId": sp.o.dojoId.get(),
        "title": sp.c.dojo.get().title,
        "scratchpad": $scratchText.val(),
    };
    misc.spinner.start("Saving ...");
    const resp = await misc.postJson("/dojoCon/updateScratchpad", dataToSend);
    app.o.dojoMap.updateOne(resp.dojo);
    misc.spinner.stop();
};

sp.close = function () {
    sp.o.dojoId.set(null);
};

module.exports = sp;
