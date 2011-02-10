/*
 * Project filterbox
 * */
function showProjects(selector, speed) {
    var targets = $(selector);
    var numTargets = targets.length;
    var newHeight = Math.ceil(numTargets/3)*$("#filterbox>li").height();
    var filterBox = $("ol#filterbox");
    var currentHeight = filterBox.height();
    filterBox.height(currentHeight);

    if (currentHeight < newHeight) {
        $("ol#filterbox").stop().animate({
            "height": newHeight
        }, 150);
    }

    targets.stop().animate({
        "width": "245px",
        "height": "145px",
        "opacity": 1
    }, speed);
}

function hideProjects(selector, speed) {
    $(selector).stop().animate({
        "width": 0,
        "width": 0,
        "opacity": 0
    }, speed);
}

function switchCategory(categoryName, speed) {
    setSelected(categoryName);
    showProjects("#filterbox>li." + categoryName, speed);
    hideProjects("#filterbox>li:not(." + categoryName + ")", speed);
    /* spin menu-text to current category */
    var prefix=$('ol i[title='+categoryName+']'),span=prefix.parent();
    !span.width(span.width()).addClass('animate').animate({
        width:prefix.width(),
        marginTop:prefix.height()*prefix.prevAll().length*-1
    });
}

function setSelected(id) {
  $("#cat_selector>ul>li").removeClass("selected");
  $("#cat_selector>ul>li:has(a#"+id+")").addClass("selected");
  Cufon.refresh();
}

$(document).ready(function() {
    lastCategory = $.cookie("last_project_category");
    if (lastCategory == null) {
        /* if cookie doesn't exist set last category to "featured" */
        $.cookie("last_project_category", "featured", {'path':'/'});
        lastCategory = "featured";
    }
    /* hide all, show last selected category */
    $("#filterbox>li").hide();
    switchCategory(lastCategory, 0);

    $("a.project_filter").click(function(event){
        /* switch category */
        event.preventDefault();
        var target_id = this.id
        switchCategory(target_id, 250);
        $.cookie("last_project_category", target_id, {'path':'/'});
    });

    /* show all projects */
    $("a.project_filter#all").click(function(event){
        event.preventDefault();
        switchCategory("all", 250);
        $.cookie("last_project_category", "all", {'path':'/'});
    });
});