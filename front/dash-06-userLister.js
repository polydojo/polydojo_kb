// npm:
var _ = require("underscore");
var $ = require("jquery");

// loc:
var misc = require("./misc.js");
var {uk, app} = require("./dash-00-def.js");

// RouteApp:
var ul = {"id": "userLister", "o": {}, "c": {}};

// Observables & Computeds:
ul.o.isInviteFormVisible = uk.observableBool(false);
ul.c.userList = app.o.userMap.list; // Alias, snap-friendly.

// Open:
ul.open = function () {
    ul.fetchUserListIfReqd();
};
ul.fetchUserListIfReqd = async function () {
    if (app.o.userMap.isFetched.get()) {
        // ==> Already fetched.
        return app.o.userMap.list();
    }
    // ==> Not yet fetched.
    return await ul.fetchUserList();
};
ul.fetchUserList = async function () {
    misc.spinner.start("Fetching Users ...");
    let fulResp = await misc.postJson("/userCon/fetchUserList", {});
    //misc.alertJson(fulResp);
    app.o.userMap.updateMany(fulResp.userList);
    app.o.userMap.isFetched.set(true);
    misc.spinner.stop();
    return fulResp.userList;
};

// Inviting:
ul.onClick_toggleInviteForm = function () {
    ul.o.isInviteFormVisible.toggle();
};
ul.onSubmit_inviteForm = async function (evnet) {
    formEl = event.target;
    window.formEl = formEl; console.log(formEl);
    await ul.sendInvite(
        formEl.fname.value,
        formEl.lname.value,
        formEl.email.value,
    );
    formEl.reset();
};
ul.sendInvite = async function (fname, lname, email) {
    // Helper, for re/inviting a user.
    let dataToSend = {
        "invitee_fname": fname,
        "invitee_lname": lname,
        "invitee_email": email.trim().toLowerCase(),      // Normalized email, lowercase + trimmed.
    };
    misc.spinner.start("Processing ...");
    let resp = await misc.postJson("/userCon/inviteUser", dataToSend);
    app.o.userMap.updateOne(resp.user);
    misc.spinner.stop();
    if (resp.inviteLink) {
        await misc.alert("Done! Joining link: " + resp.inviteLink);
    } else {
        await misc.alert("Done! Invitation email sent.");
    }
};
ul.onClick_reinvite = async function (thatUserId) {
    let thatUser = app.o.userMap.get()[thatUserId];
    await ul.sendInvite(thatUser.fname, thatUser.lname, thatUser.email);
};

// Re/Deactivating:
ul.onClick_toggle_isDeactivated = async function (thatUserId) {
    let thatUser = app.o.userMap.get()[thatUserId];
    console.assert(thatUser, "Assert `thatUser` exists.");
    let dataToSend = {
        "thatUserId": thatUser._id,
        "preToggle_isDeactivated": thatUser.isDeactivated,                      // <-- To prevent accidental oppsite toggle.
    };
    let z = thatUser.isDeactivated ? "r" : "d";                                 // CLI only. Helps flash spinner msg.
    misc.spinner.start(z.toUpperCase() + "eactivating ...");                    // Flash 'Deactivating ...' or 'Reactivating ...'
    let resp = await misc.postJson("/userCon/toggleUser_isDeactivated", dataToSend);
    app.o.userMap.updateOne(resp.user);
    misc.spinner.stop();
    await misc.alert("Done! User account " + z + "eactivated.");
};

// Close:
ul.close = function () {
    ul.o.isInviteFormVisible.set(false);
};

// Export:
module.exports = ul;
