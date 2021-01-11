function flashboxEnd(){
    var flash_red=document.getElementById("flash_box-red");
    var flash_green=document.getElementById("flash_box-green");

    if (flash_red !== null){
        flash_red.style.display="none";

    }else if (flash_green !== null){
        flash_green.style.display="none";

    }else{
        console.log("Nothing changed")
    }
}

var $animateBox = $(".link-box");
var $window = $(window);
