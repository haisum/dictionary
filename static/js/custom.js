/**
 * word model
 */

word = {};
word.init = function(){
	$("#language").on("change", word.languageChanged);
}
word.languageChanged = function(e){
	var language = $(this).val();
	if(language == "english"){
		$(".foreign-lang").hide();
		$(".english-lang").show();
	}
	else{
		$(".foreign-lang").show();
		$(".english-lang").hide();	
		$("#lang_text").html(helpers.capitaliseFirstLetter(language));
	}
}
/**
 * Helpers
 */
helpers = {};
helpers.capitaliseFirstLetter = function(string)
{
    return string.toLowerCase().charAt(0).toUpperCase() + string.slice(1);
}
/**
 * Document ready bindings
 */
$(document).ready(function(){
	word.init();
});