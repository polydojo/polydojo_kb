// npm:
var _ = require("underscore");
var $ = require("jquery");
var bootbox = require("bootbox");

// loc:
var K = require("./constants.js");
var misc = require("./misc.js");
var underkick = require("./underkick.js");
var underkick_qsRouter = require("./underkick_qsRouter.js");

// prelims:
var uk = underkick({
    "pluginList": [underkick_qsRouter],
    //"throttleWait": 0,      // No throttling. We deal w/ lots of non-observable input and don't want future-render-queueing.
    //"debounceWait": 0,
    //"jsonRouter_animateCss": "animated fadeInLeft",
    "listenTarget": "body",
});

var app = {
    "name": "Polydojo",
    "o": {}, "c": {},
    "router": uk.qsRouter(),
    "K": K,
};

app.o.userMap = uk.observableDocMap("fname");
app.o.articleMap = uk.observableDocMap("title");
app.o.categoryMap = uk.observableDocMap("rank");
app.o.categoryMap.updateOne({
    "_id": "",
    "name": "",
    "rank": 0,
    "parentId": null, // special null, not "", to avoid inf-recursion
});

app.o.currentUserId = uk.observable(null);
app.c.currentUser = uk.computed(
    function () {
        let cuid = app.o.currentUserId.get();
        if (! cuid) { return null; }    // Short ckt.
        let currentUser = app.o.userMap.get()[cuid];
        return currentUser || null;
    },
    [app.o.userMap, app.o.currentUserId],
);

app.modalComponent =  function (id, submodel, bootboxConfig) {
    bootboxConfig = bootboxConfig || {};
    return bootbox.dialog(_.extend({}, {
        "message": uk.component(id, submodel),
        "onEscape": true,   // 'esc' key => close.
        "backdrop": true,   // Click outside => close.  (This depends on 'onEscape' being truthy. See docs for more.)
        "size": null,       // That's bootbox's default. Also accepts 'small' and 'large'.
    }, bootboxConfig));
};
app.onClick_toggleDropdownByBtnId = function (ddBtnId) {
    let $ddBtn = $("#" + ddBtnId);
    _.defer(function () {
        // XXX: Can't explain the need for _.defer().
        // TODO: Investigate IFF reqd.
        $ddBtn.dropdown("toggle");
    });
};

module.exports = {
    uk, app,
};
