/*
 * Cufon setup
 * */
Cufon.replace('#cat_selector li a', {fontFamily:'mokka_sc',hover:true,fontSize:'19px',textTransform:'lowercase'});
Cufon.replace('#cat_selector li.selected a',{fontFamily:'mokka_sc',hover:false,fontSize:'19px',textTransform:'lowercase'});
Cufon.replace('h2',{textShadow: '1px 1px rgba(255, 255, 255, 0.6)',fontFamily:'mokka',hover:true});
Cufon.replace('h3',{textShadow: '1px 1px rgba(255, 255, 255, 0.2)',fontFamily:'mokka',hover:true});
Cufon.replace('ol li#nav-projects i',{fontFamily:'mokka_sc'});

function loadImages(selector) {
    // ex. loadImages('div.somediv img.load');
    
    $(selector).each(function(index, element){
        if (!element.complete) {
            var elHeight = $(this).height();
            var elWidth = $(this).width();
            var elPosition = $(this).position();
            $(this).parent().css({"position": "relative"});
            var spinner = $("<ins></ins>").height(elHeight).width(elWidth).css({
                "background": "transparent url('http://media.divensis.no/media/gfx/spinner.gif') no-repeat center center",
                "position": "absolute",
                "left": 0,
                "top": 0
            }).addClass("loader");
            $(this).before(spinner);
            $(this).css("visibility", "hidden");
        }
    });
    
    $(selector).load(function(event){
        var spinnerDiv = $(this).prev("ins.loader");
        if (spinnerDiv.length > 0) {
            $(this).hide();
            $(this).css({"visibility": "visible"});
            $(this).fadeIn(250);
            $(this).prev("ins.loader").fadeOut(250, function(){
                $(this).hide();
                //$(this).remove();
            });
            $(this).removeClass("load");
        }
    }).each(function(){
        if(this.complete) {
            $(this).trigger("load");
        }
    });
}

$(document).ready(function() {
    /*
     * Return to top
     * */
    $('#returntotop').click(function(){
        return !$('html,body').animate({scrollTop:0});
    });

    /*
     * Image loader
     * */
    loadImages('img.load');
});
