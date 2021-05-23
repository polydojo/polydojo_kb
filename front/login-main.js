var $ = require("jquery");
var _ = require("underscore");
var misc = require("./misc.js");
var K = require("./constants.js");

$(function () {
    misc.spinner.stop();
    // TODO-the-following:
    /*
    _.each($(".ghRepoUrl"), function (el) {                 // <-- TODO: Set .ghRepoUrl's href not only for login.html, but others too.
        el.href = K.GH_REPO_URL;
        el.target = "_blank";
    });
    */
});

$("form.loginr").on("submit", async function (event) {
    event.preventDefault();
    var form = event.currentTarget;
    var dataToSend = {
        "email": form.email.value,
        "pw": form.pw.value,
    };
    console.log(dataToSend);
    misc.spinner.start("Logging in ...");
    var resp = await misc.postJson("/userCon/loginDo", dataToSend);
    misc.spinner.flash("Redirecting ...");
    location.href = "/dash";
});
