$(function () {

    var $category = $(".category");

    console.log($category);
    $category.click(function(event){
    var $div = $("div");
    $div.toggleClass('hidden');

    });


});
