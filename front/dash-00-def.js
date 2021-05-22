// npm:
var _ = require("underscore");
var $ = require("jquery");

// loc:
var misc = require("./misc.js");
var underkick = require("./underkick.js");
var underkick_qsRouter = require("./underkick_qsRouter.js");

// prelims:
var uk = underkick({
    "pluginList": [underkick_qsRouter],
    //"throttleWait": 0,      // No throttling. We deal w/ lots of non-observable input and don't want future-render-queueing.
    //"debounceWait": 0,
    //"jsonRouter_animateCss": "animated fadeInLeft",
});

var app = {
    "name": "Polydojo",
    "o": {}, "c": {},
    "router": uk.qsRouter(),
};

app.o.userMap = uk.observableDocMap("fname");
app.o.dojoMap = uk.observableDocMap("title");

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

module.exports = {
    uk, app,
};
