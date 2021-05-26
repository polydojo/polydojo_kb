// npm:
var _ = require("underscore");
var $ = require("jquery");
var bootbox = require("bootbox");

// loc:
var misc = require("./misc.js");
var {uk, app} = require("./dash-00-def.js");

// RouteApp:
var al = {"id": "articleLister", "o": {}, "c": {}};


// Observables & Computeds:
al.c.articleList = app.o.articleMap.list,   // Alias, snap-friendly.
al.c.categoryList = app.o.categoryMap.list; // Alias, snap-friendly.

al.c.combo = uk.computed(function () {
    let articleMap = app.o.articleMap.get();
    let categoryMap = app.o.categoryMap.get();
    let articleList = al.c.articleList.get();
    let categoryList = al.c.categoryList.get();
    
    let childParent_categoryMap = {};       // childId -> parent
    let parentChildren_categoryMap = {};    // parentId -> child list.
    let categoryArticlesMap = {};           // categoryId -> articleList
    
    _.each(categoryList, function (category) {
        let parentId = category.parentId;
        let childId = category._id;
        //
        childParent_categoryMap[childId] = categoryMap[parentId];
        //
        if (! _.isArray(parentChildren_categoryMap[parentId])) {
            parentChildren_categoryMap[parentId] = [];
        }
        parentChildren_categoryMap[parentId].push(category);
    });
    
    _.each(articleList, function (article) {
        category = categoryMap[article.categoryId];
        if (! _.isArray(categoryArticlesMap[category._id])) {
            categoryArticlesMap[category._id] = [];
        }
        categoryArticlesMap[category._id].push(article);
    });
    
    let buildCatNode = function (startCategoryId) {
        let startCategory = categoryMap[startCategoryId];
        let childCategoryIdList = _.pluck(
            parentChildren_categoryMap[startCategoryId], "_id",
        );
        let catNode = {
            "_id": startCategoryId,
            "childNodes": _.map(childCategoryIdList, buildCatNode),
        };
        return catNode;
    };
    let topCatNode = buildCatNode("");
    
    let catDropOptList = [];
    let traverse_fillDropOpts = function (catNode, prefix) {
        prefix = prefix || "";
        let category = categoryMap[catNode._id];
        let optText = prefix + category.name;
        let nextPrefix = optText + " > ";
        if (category._id === "") {
            optText = "None (Top Level)";
            nextPrefix = "";
        }
        catDropOptList.push({
            "value": category._id,
            "text": optText,
        });
        _.each(catNode.childNodes, function (childCatNode) {
            traverse_fillDropOpts(childCatNode, nextPrefix);
        });
    };
    traverse_fillDropOpts(topCatNode); // Fills `catDropOptList`.
    
    return {
        "childParent_categoryMap": childParent_categoryMap,
        "parentChildren_categoryMap": parentChildren_categoryMap,
        "categoryArticlesMap": categoryArticlesMap,
        "topCatNode": topCatNode,
        "catDropOptList": catDropOptList,
    };
}, [ // Deps:
    app.o.articleMap,   app.o.categoryMap,
    al.c.articleList,   al.c.categoryList,
]);

// Open:
al.open = async function () {
    await al.fetchCategoryListIfReqd();
    await al.fetchArticleListIfReqd();
};
al.fetchArticleListIfReqd = async function () {
    if (app.o.articleMap.isFetched.get()) {
        // ==> Already fetched.
        return app.o.articleMap.list();
    }
    // ==> Not yet fetched.
    return await al.fetchArticleList();
};
al.fetchArticleList = async function () {
    misc.spinner.start("Fetching Articles ...");
    let resp = await misc.postJson("/articleCon/fetchArticleList", {});
    //misc.alertJson(resp);
    app.o.articleMap.updateMany(resp.articleList);
    app.o.articleMap.isFetched.set(true);
    misc.spinner.stop();
    return resp.articleList;
};
al.fetchCategoryListIfReqd = async function () {
    if (app.o.categoryMap.isFetched.get()) {
        // ==> Already fetched.
        return app.o.categoryMap.list();
    }
    // ==> Not yet fetched.
    return await al.fetchCategoryList();
};
al.fetchCategoryList = async function () {
    misc.spinner.start("Fetching Categories ...");
    let resp = await misc.postJson("/categoryCon/fetchCategoryList", {});
    //misc.alertJson(resp);
    app.o.categoryMap.updateMany(resp.categoryList);
    app.o.categoryMap.isFetched.set(true);
    misc.spinner.stop();
    return resp.categoryList;
};

// Creating:
al.onClick_createArticle = async function () {
    let title = await misc.prompt("Article's Title:");
    if (! title) { return null; }
    let dataToSend = {
        "title": title,
    };
    misc.spinner.start("Creating ...");
    var resp = await misc.postJson("/articleCon/createArticle", dataToSend);
    var article = resp.article;
    app.o.articleMap.updateOne(article);
    misc.spinner.stop();
    app.router.setInfo({
        "id": "articleEditor",
        "articleId": article._id,
    });
};

al.onClick_createCategory = async function () {
    app.modalComponent("modalbox_createCategory", {}, {});
};
al.onSubmit_createCategory = async function (event) {
    const form = event.currentTarget;
    const dataToSend = {
        "name": form.name.value,
        "rank": Number(form.rank.value),
        "parentId": form.parentId.value,
    };
    $(form).find(".bootbox-close-button").click();
    misc.spinner.start("Creating ...");
    var resp = await misc.postJson("/categoryCon/createCategory", dataToSend);
    var category = resp.category;
    app.o.categoryMap.updateOne(category);
    misc.spinner.stop();
    misc.alert("Done! Category created.");
};

module.exports = al;
