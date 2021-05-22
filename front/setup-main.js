var $ = require("jquery");
var _ = require("underscore");
var Swal = require('sweetalert2')["default"];
//var DOMPurify = require("dompurify")["default"](window);
var misc = require("./misc.js");


$(function () { misc.spinner.stop(); });

$("form.setupr").on("submit", async function (event) {
    event.preventDefault();
    var form = event.currentTarget;
    if (form.pw.value !== form.repeatPw.value) {
        Swal.fire("Passwords don't match.");
        return null;
    }
    var dataToSend = {
        "fname": form.fname.value,
        "lname": form.lname.value,
        "email": form.email.value,
        "pw": form.pw.value,
    };
    //console.log(dataToSend);
    misc.spinner.start("Setting up ...");
    var resp = await misc.postJson("/userCon/setupFirstUser", dataToSend);
    await Swal.fire("Setup complete. Please log in.");
    misc.spinner.flash("Redirecting ...");
    location.href = "/login";
});
