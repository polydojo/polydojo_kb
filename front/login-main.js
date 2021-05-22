var $ = require("jquery");
var _ = require("underscore");
var misc = require("./misc.js");

$(function () { misc.spinner.stop(); });

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
