var isProjectEditing = false;   // 判断project 是否 再修改中
$(document).ready(function(){
    setProjectFrame();
    $('#user-name').html(window.uname);// set username
    getUserProjects();  // get user's projects
});
window.onresize=function(){
	setProjectFrame();
}
function setProjectFrame(){
	var total_height = document.documentElement.clientHeight
	   || window.innerHeight || docuemnt.body.clientHeight;
	document.getElementById('project-area').style.height = total_height+'px';
	document.getElementById('main').style.height = total_height+'px';
	// document.getElementById('device-area').style.height = total_height+'px';
	document.getElementById('project-infos').style.height = total_height+'px';
	var logo_height = $('#logo').height();
	var project_shop_height = $('#project-shop').height();
	var project_content_height = total_height-logo_height-3-project_shop_height;
	$('#project-content').css('height',project_content_height);
}
function getUserProjects(){
	$.ajax({
		url : '/home/getUserProject',
		type: "GET",
		success: function(result){
			displayProjects(result);
		}
	});
}
function displayProjects(result){
	for (var i = 0; i < result['projects'].length; i++){
		var projectInfo = result['projects'][i];
		var name = projectInfo['name'],
		    track = projectInfo['track'],
		    id = projectInfo['id'];
		addProject(name, track, id);
	}
}
// add the new project into #project-content
function addProject (name, track, id) {
	var project_label = $(get_element('li', '', 'class', 'project-label', 'track', track, 'project-id', id ));
	var span_first = $( get_element('span', '', 'class', 'first glyphicon glyphicon-chevron-right'));
	var span_second = $( get_element('span', name, 'class', 'second'));
	// var button = $( get_element('button',''));
	var button = $( get_element('div','', 'class', 'button'));
	var div = $( get_element('div', '', 'class', 'project-label-shop'));
	var edit = $( get_element('span', '', 'class', 'project-edit glyphicon glyphicon-pencil'));
	var add = $( get_element('span', '', 'class', 'project-add glyphicon glyphicon-plus-sign'));
	var remove = $( get_element('span', '', 'class', 'project-remove glyphicon glyphicon-remove-sign'));
	div.append(edit, add, remove);
	button.append(span_first).append(span_second);
	var ul = $( get_element('ul', '', 'class', 'device-menu device-menu-hide'));
	project_label.append(button).append(div).append(ul);
	$('#project-content').append(project_label);
}
// create a new project
function createProject (name, track_id) {
	var postData = {
		'name':name,
		'track': track_id
	};
	$.ajax({
		url:'/home/newProject',
		type:'POST',
		data:postData,
		dataType:'JSON',
		success: function(result){
			$('#addProject').modal('hide');
            if(result['isSuccessful']){
                addProject(result['project_name'], result['track'],result['id']);
                showMsg('New project saved');
            }else{
                showMsg("Project create failed");
            }
		}
	})
}
function setTracks(){
    $.ajax({
        url:'/home/tracks',
        type:'GET',
        success : function(result){
            addTracks(result)
        }
    });
}
function addTracks(result){
	console.log(result);
    if (result['isSuccessful']){
        $('#tracks').empty();
        track_list = result['tracks'];
        for(var i = 0; i < track_list.length; i++){
            var newOption = $('<option></option>');
            newOption.html(track_list[i]['track']);
            newOption.val(track_list[i]['id']);
            var newOptions = newOption;
            $('#tracks').append(newOption);
        }
    }
}
// create a new device 
function createDevice(name, id){
	var postData = {
		'name' : name, 
		'id': id
	};
	$.ajax({
		url:'/home/newDevice',
		dataType:'JSON',
		type: 'POST',
		data:postData,
		success: function(result){
			$('#addDevice').modal('hide');
			if(result['isSuccessful']){
				var element = $( get_element('li', result['name'], 'class', 'device-label', 'chain-id', result['id']) );
				var div = $( get_element('div', '', 'class', 'device-label-shop' ) );
				var edit = $( get_element('span', '', 'class', 'device-edit glyphicon glyphicon-pencil'));
			    var add = $( get_element('span', '', 'class', 'device-add glyphicon glyphicon-plus-sign'));
			    var remove = $( get_element('span', '', 'class', 'device-remove glyphicon glyphicon-remove-sign'));
				div.append(edit, add, remove);
				element.append(div);
				$('ul#project-content li.altering ul#device-menu').append(element);
			}else{
				showMsg('Device create failed');
			}
		}
	})
}
//获取project 的 chain
function getProjectChains(id){
	$.ajax({
		url:'/home/getChainList?id=' + id,
		type:'GET',
		success: function(result){
			displayChains(result);
		}
	});
}
function displayChains(result){
	for(var i = 0; i < result.length; i++){
		var element = $( get_element('li', result[i]['name'], 'class', 'device-label', 'chain-id', result[i]['id']) );
		var div = $( get_element('div', '', 'class', 'device-label-shop' ) );
		var edit = $( get_element('span', '', 'class', 'device-edit glyphicon glyphicon-pencil'));
	    var add = $( get_element('span', '', 'class', 'device-add glyphicon glyphicon-plus-sign'));
	    var remove = $( get_element('span', '', 'class', 'device-remove glyphicon glyphicon-remove-sign'));
		div.append(edit, remove);
		element.append(div);
		$('li.project-label-click ul.device-menu').append(element);
	}
}
function getChainLength (chainId) {
	var text = 'Length: 0';
	$.ajax({
		url: '/home/getChainLength?id=' + chainId,
		type: 'GET',
		success:function(result){
			if(result['isSuccessful']){
				text = 'Length: ' + result['length'];
			}
			$('div#infos-content span').text(text);
		}
	});
}
function showChainImage(chainId){
	$.ajax({
		url:'/home/getResultImage?id=' + chainId,
		type:'GET',
		success:function(result){
			if (result['isSuccessful']){
				$('#chain-img').attr('src', result['filepath']);
			}
		}
	});
}
// alter project name
function alterProjectName(project_id, project_name){
    var postData={
		'id':project_id,
		'name':project_name,
	};
	$.ajax({
		url:'/home/changeProjectname',
		type:'POST',
		data:postData,
		dataType:'JSON',
		success: function(result){
			if(result['isSuccessful']){
				showMsg("alter success");
				$('.altering button span.second').text(project_name);
			}else{
				showMsg('alter failed');
			}
		}
	});
}
//alter project track
function alterProjectTrack(project_id, track_id,track_name){
    var postData={
    	'id':project_id,
    	'track_id':track_id,
    };
    $.ajax({
    	url:'/home/changeTrack',
    	type:'POST',
    	data:postData,
    	dataType:'JSON',
    	success:function(result){
    		if(result['isSuccessful']){
    			showMsg('success');
    			$('.altering').attr('track',track_name);
    		}else{
    			showMsg('failed');
    		}
    	}
    });
}
function showMsg(msg){
    $('div.hint-info').html(msg);
    $('div.hint-info').removeClass('hide');
    $('div.hint-info').show(200).delay(1000).hide(200);
}
function get_element(tag,inner){
    var element = document.createElement(tag); // create a element 
    element.innerHTML = inner;   // set element's inner html
    for(var i = 2; i<arguments.length-1; i=i+2){
        element.setAttribute(arguments[i], arguments[i+1]);
    }
    return element;
}
function isDeviceIn(element, chain_id){
	var elements = element.children('ul').children('li');
	for( var i = 0; i<elements.length; i++){
		if( chain_id == elements[i].getAttribute('chain-id')){
			console.log( chain_id +  '   ' + elements[i].getAttribute('chain-id'));
			return true;
		}
	}
	return false;
}
function deviceToggleShop(){
	$(this).children('div').toggleClass('show');
}
function projectToggleShop(){
	if(!isProjectEditing){
		$(this).next('div').toggleClass('show');
	}	 
}
//  logout click
$(document).on({
	click:function(){
		$.ajax({
			type:'GET',
			url:'/accounts/logout',
			success:function(result){
				window.location='/'
			}
		});
	}
},'#logout');
$(document).on({
	click:function(){
		setTracks();// get tracks 
		var modal = $('#addProject');
		$('#addProject .modal-header h4').text("add new project");
		$('#project-name').attr('value','');
		$('#submit-project').removeAttr('disabled');
		modal.attr("todo","add");
		modal.modal('show');
	}
}, '#add-project');
// submit-project click
$(document).on({
	click:function(){
		$('#submit-project').attr('disabled','disabled'); // 按钮禁用   防止多次提交
		var name = $('#project-name').val(),
		track_id = $('#tracks').val();
		track_name = $('#tracks option:selected').text();
		var todo = $('#addProject').attr('todo');
		if(todo=='add'){
            createProject(name, track_id);
		}else if(todo=='alter'){
			var alter_id = $('#addProject').attr('alter_id');
            alterProjectName(alter_id, name);
            alterProjectTrack(alter_id, track_id, track_name);
            $('#addProject').modal('hide');
		}
		 
	}
},'#submit-project');
//修改 project 按钮
$(document).on({
    click:function(){
    	var elements = $('div#project-area ul#project-content li.project-label div.project-label-shop');
    	if(elements.hasClass('show')){
    		isProjectEditing = false;
    	}else{
    		isProjectEditing = true;
    	}
    	elements.toggleClass('show');
   }
},"#edit-project");
$(document).on({
	click:function(ev){
		var oEvent = ev || event;
		oEvent.cancelBubble = true;
		// event.stopPropagation();  //  阻止事件冒泡 
		var liElement = $(this).parent().parent();
		var project_id = liElement.attr('project-id'),
			track = liElement.attr('track');
		$('.altering').removeClass('altering');
	    liElement.toggleClass('altering');//为这个project 加标记
	    var project_name = liElement.children('button').children('span.second').text();
		if( $(this).hasClass('project-add') ){  
			//  add device
			var myModal = $('#addDevice');
			$('#createChain').removeAttr('disabled');
			myModal.attr('project-id',project_id).modal('show');
		}else if( $(this).hasClass('project-edit') ){
			// edit project
			setTracks();// get tracks 
    		var modal = $('#addProject');
    		$('#submit-project').removeAttr('disabled');
	    	$('#addProject .modal-header h4').text("alter your project");
	    	$('#project-name').attr('value',project_name);
	    	modal.attr("todo","alter").attr("alter_id",project_id).attr('track',track);
	    	modal.modal('show');
		}else if( $(this).hasClass('project-remove') ){
			// remove project
			var myModal = $('#waring-modal');
			var str = 'Are you sure to delete '+ project_name + ' ?';
			$('#waring-content').text(str);
			$('#delete-project').removeClass('hide').removeAttr('disabled');
			myModal.attr('project-id',project_id).modal('show');
		}
	}
},"ul#project-content li.project-label div.project-label-shop span");
$(document).on({
	click:function(){
		$('button#delete-project').attr('disabled','disabled');
		var project_id = $('#waring-modal').attr('project-id');
		var postData = {
			'id' : project_id
		};
		$.ajax({
			url:'/home/deleteProject',
			type:'POST',
			data:postData,
			success:function(result){
				if(result['isSuccessful']){
					var doDesign = $('button#doDesign'),
					    elements = $('li.altering');
					var chain_id = doDesign.attr('chain-id');

					if( isDeviceIn( elements, chain_id ) ){
						doDesign.attr('disabled','disabled');
						$('#project').text('Project');
						$('#track').text('Device');
						$('#infos-content h1').text('Device');
						$('#infos-content span').text('Length: 0');
					}
					elements.remove();
					showMsg('delete successful');
				}else{
					showMsg('delete failed');
				}
			}
		});
	}
},'#waring-modal button#delete-project'); 
// create a new device click
$(document).on({
	click:function(){
		$('#createChain').attr('disabled','disabled');
		var name = $('#device-name').val(),
		project_id = $('#addDevice').attr('project-id');
		createDevice(name, project_id)
	}
}, '#createChain');
//project-label click
$(document).on({
    click:function(event){  
    	//event.stopPropagation();  //  阻止事件冒泡 
    	$('div#project-area ul#project-content li.project-label-click').removeClass("project-label-click");
    	$(this).parent().toggleClass("project-label-click");
    	if( $(this).parent().children('ul.device-menu').hasClass('device-menu-hide') ){
	    	$('li.project-label-click ul.device-menu').empty(); 
	    	var project = $(this).children('span.second').text() + ' ' +$(this).parent().attr('track');
	    	$('#project').text(project);
	    	$('#track').text('');
	    	getProjectChains($(this).parent().attr('project-id'));
	    }
	    var span = $(this).children('span.first');
	    span.toggleClass('glyphicon-chevron-right').toggleClass('glyphicon-chevron-down');
	    $(this).parent().children('ul.device-menu').toggleClass('device-menu-hide');
    }
    // ,
    // mouseover:projectToggleShop,
    // mouseout:projectToggleShop
},'div#project-area ul#project-content li.project-label div.button');

// track click
$(document).on({
    click:function(event){
    	if( $('button#doDesign').attr('disabled') == 'disabled' ){
    		$('button#doDesign').removeAttr('disabled');
    	}
    	event.stopPropagation();  //阻止事件冒泡
    	$('ul.device-menu li.device-label-click').removeClass("device-label-click");
    	$(this).addClass("device-label-click");
    	var track = $(this).text();
    	$('div#infos-content h1').text(track);
    	$('#track').text(track); 
    	var chain_id = $(this).attr('chain-id');
    	$('div#infos-content button').attr('chain-id', chain_id);
    	showChainImage(chain_id);
    	getChainLength(chain_id);
    },
    mouseover:deviceToggleShop,
    mouseout:deviceToggleShop
},'ul.device-menu li.device-label');
$(document).on({
	click:function(){
		window.location = '/home/dashboard?id=' + $(this).attr('chain-id');
	}
},'#infos-content button#doDesign');

$(document).on({
  click:function(){
    window.location ='/system/system';
  }
}, '#to_system');

$(document).on({
	click:function(){
		$.ajax({
		url:'/home/getResultImage?id=' + chainId,
		type:'GET',
		success:function(result){
			if (result['isSuccessful']){
				window.location.href = result['filepath'];
			}
		}
	});
	}
}, '#get_result');
$(document).on({
	click:function(){
		window.location = '/home/simulation'
	}
}, '#version');
$(document).on({
	mouseover:function(){
		$('div#project-infos ul#dropdown-menu').removeClass('menu-hide');
	},
	mouseout:function(){
		$('div#project-infos ul#dropdown-menu').addClass('menu-hide');
	}
},'div#project-infos div#dropdown, div#project-infos ul#dropdown-menu');
$(document).on({
	click:function(){
		alert('device-remove');
	}
},'div.device-label-shop span.device-remove');
$(document).on({
	click:function(){
		alert('device-edit');
	}
},'div.device-label-shop span.device-edit');









