var $ = require("jquery");
var _ = require("underscore");
var Cookies = require("js-cookie");

var misc = {Cookies: Cookies};


// SPINNER:
misc.spinner = (function () {
    "use strict";
    var sp = {};
    sp.$spinner = $(".spinner");
    sp.$spinnerFlash = $(".spinnerFlash");
    sp.flash = function (msg, isHtml) {
        isHtml = isHtml || false;
        if (! isHtml) {
            sp.$spinnerFlash.text(msg || "Loading ...");
        } else {
            sp.$spinnerFlash.html(msg || "Loading ...");
        }
    };
    sp.start = function (msg, isHtml) {
        sp.flash(msg, isHtml);
        sp.$spinner.fadeIn("fast");                         //sp.$spinner.slideDown("fast");    // Show (slideDown => slideIn)
    };
    sp.stop = function () {
        sp.$spinner.fadeOut("fast");                        //sp.$spinner.slideUp("slow");      // Hide (slideUp => slideOut)
    };
    sp.stopWith = function (msg, timeMS) {
        timeMS = timeMS || 1500;
        sp.start(msg);
        window.setTimeout(function () {
            sp.stop();
        }, timeMS);
    };
    return sp;
}());

misc.postJson = async function (url, data, success) {
    if (! _.isString(data)) { data = JSON.stringify(data); }
    var ajaxOpt = {
        "type": "POST",
        "url": url,
        "data": data,
        "success": success,
        "dataType": "json",
        "contentType": "application/json",
        "headers": {
            "X-Csrf-Token": Cookies.get("xCsrfToken") || "",
        },
    };
    //console.log(ajaxOpt);
    return $.ajax(ajaxOpt);
};

$(document).ajaxError(function (event, jqXhr) {
    window.jqXhr = jqXhr;
    //console.log(jqXhr.responseText);
    //console.trace();
    if (jqXhr.status == 418 && jqXhr.responseJSON && jqXhr.responseJSON.status === "fail") {
        // ==> 418 JSON Error
        var reason = jqXhr.responseJSON.reason;
        if (reason.toLowerCase().split(" ").join("").includes("logout")) {
            // ==> Force logout
            alert("Error: " + reason);
            location.href = "/logout";
        } else {
            // ==> Needn't force logout.
            alert("Error: " + reason);
        }
    } else if (jqXhr.status === 0) {
        alert("Network error, please check your Internet connection and retry.");
    } else {
        // Unknown error:
        alert("An unknown error occured. | Status Code: " + jqXhr.status);
    }
    misc.spinner.stop();
});

// Break out of iframes:
misc.frameBreak = function () {
    "use strict";
    // Ref. https://css-tricks.com/snippets/javascript/break-out-of-iframe/
    if (window.location !== window.top.location) {
        // Later try:
        _.delay(function () {
            $("html").html("FRAME ERROR: Please contact support@polydojo.com.");
        }, 100);
        // First try:
        window.top.location = window.location;              // <-- If browser blocks top-nav, then delayed 'FRAME ERROR' msg shown.
    }
};


module.exports = misc;
