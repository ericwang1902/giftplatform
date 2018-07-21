$(function(){
	
	$(".nav ul li").hover(function () {
		if($(this).find(".item").find("p").length>0){
			$(this).find(".item").show();
		}
	}, function () {
		$(this).find(".item").hide();
	});
})
function setTabGG(name, cursel, n) {
	for (i = 1; i <= n; i++) {
		var menu = document.getElementById(name + i);
		var con = document.getElementById("lmu_" + name + "_" + i);
		menu.className = i == cursel ? "act" : "";
		con.style.display = i == cursel ? "block" : "none";
	}
}