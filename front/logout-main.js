var _ = require("underscore");
var $ = require("jquery");
var misc = require("./misc.js");

var hitLogout = async function () {
    misc.spinner.flash("Logging out ...");
    var resp = await misc.postJson("/userCon/logout", {});
    $("#logout_main").show();
    misc.spinner.stop();
};
hitLogout();
