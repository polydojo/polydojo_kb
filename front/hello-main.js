var _ = require("underscore");
var $ = require("jquery");

$("button").on("click", function (event) {
    window.alert("Thanks for clicking! You're so nice!!");
});

// topLevelError_foo();

/*var errorfulFunc = function () {
    return (function () {
        return (function () {
            return nestedError_bar();
        }());
    }());
};
errorfulFunc();*/

window._ = _;
window.$ = $;
