var $ = require("jquery");
var _ = require("underscore");
var Swal = require('sweetalert2')["default"];
//var DOMPurify = require("dompurify")["default"](window);
var misc = require("./misc.js");

const makeshift_parseQs = function (qs, shouldTrim) {
    // Makeshift helper, from uk's parseQs.
    var pairRe, info;
    qs = qs || location.search.slice(1);
    shouldTrim = shouldTrim || false;
    pairRe =  /[^=&]+\=[^=&]+/g;                        // Something of the form "foo=bar"
    info = {};
    _.each(qs.match(pairRe), function (pair) {
        var kv = _.map(pair.split("="), decodeURIComponent);
        if (shouldTrim) {
            kv[0] = kv[0].trim();
            kv[1] = kv[1].trim();
        }
        info[kv[0]] = kv[1];
    });
    return info;
};

const QS = makeshift_parseQs();
window.QS = QS;

const fetchInvitee = async function () {
    const dataToSend = {
        "userId": QS.inviteeId,
        "veriCode": QS.veriCode,
    };
    const resp = await misc.postJson("/userCon/fetchInvitedUserByVeriCode", dataToSend);
    window.user = resp.user;
    return resp.user;
};

$("form.joinr").on("submit", async function (event) {
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
        "userId": form.userId.value,
        "veriCode": form.veriCode.value,
        "pw": form.pw.value,
    };
    console.log(dataToSend);
    misc.spinner.start("Joining ...");
    var resp = await misc.postJson("/userCon/acceptInvite", dataToSend);
    misc.spinner.flash("Redirecting ...");
    location.href = "/dash";
});

$(async function () {
    let invitee = await fetchInvitee();
    let form = $("form.joinr")[0];
    form.fname.value = invitee.fname;
    form.lname.value = invitee.lname;
    form.email.value = invitee.email;
    form.userId.value = invitee._id,
    form.veriCode.value = QS.veriCode;
    misc.spinner.stop();
});
