window.onresize=function(){
    setFrame();
}
$(document).ready(function(){
	setFrame()
});
function setFrame(){
	var totalHeight = document.documentElement.clientHeight
	   || window.innerHeight || docuemnt.body.clientHeight;
	$('#container').css('height', totalHeight);
	var headerHeight = $('#header').height();
	var mainHeight = totalHeight - headerHeight;
	$('#sidebar').css('height', mainHeight);
	$('#content').css('height', mainHeight);
}
$(document).on({
	click:function(){
		if( $(this).parent().parent().children('li.input-row').length != 1 ){
			$(this).parent().remove();
		}
	}
},'span.remove-input-row');
$(document).on({
	click:function(){
		var ulElem = $(this).prev('ul.input-table');
		var liElem = $('#input-row').tmpl({});
		ulElem.append( liElem );
	}
},'button.new-input-row');
$(document).on({
	click:function(){
		var insertElems=$('#reaction-equation-area').tmpl({});
		insertElems.insertBefore( $(this) );
	}
},'button#add');

$(document).on({

}, 'button#reset');

$(document).on({
	click:function(){
		if( $('div.reaction-equation-area').length != 1 ){
			$(this).parent().remove();
		}
	}
},'div.reaction-equation-area button.remove-reaction-equation');

function getElement(tag,inner){
    var element = document.createElement(tag); // create a element 
    element.innerHTML = inner;   // set element's inner html
    for(var i = 2; i<arguments.length-1; i=i+2){
        element.setAttribute(arguments[i], arguments[i+1]);
    }
    return element;
}

$(document).on({
}, 'button#run');


