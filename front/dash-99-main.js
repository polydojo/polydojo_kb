// npm:
var _ = require("underscore");
var $ = require("jquery");
var bootbox = require("bootbox");
var __bootstrap = require("bootstrap");
//var __popper = require("popper.js")["default"];

// loc:
var misc = require("./misc.js");
var {uk, app} = require("./dash-00-def.js");

app.articleLister = require("./dash-03-articleLister.js");
app.articleViewer = require("./dash-03.5-articleViewer.js");
app.articleEditor = require("./dash-04-articleEditor.js");
app.userLister = require("./dash-06-userLister.js");

app.detectLogin = async function () {
    var resp = await misc.postJson("/userCon/detectLogin", {});
    if (! (resp && resp.user && resp.user._id)) {
        location.href = "/login";
        return null;
    }
    // ==> Detection succeeded.
    app.o.userMap.updateOne(resp.user);
    app.o.currentUserId.set(resp.user._id);
    misc.spinner.stop();
    return null;
};

$.extend(window, {$, _, uk, app, bootbox}); // Pre-tpl-rendering.

$(async function () {
    await app.detectLogin();
    uk.render(app, "ukSource", "ukTarget", "model",);
    app.router.autoRegister(app); // Post-first-render
    app.router.trigger();
});
