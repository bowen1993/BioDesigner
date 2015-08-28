$(document).ready(function(){
    setProjectFrame();
    $('#user-name').html(window.uname);// set username
    getUserProjects();  // get user's projects
});
window.onresize=function(){
	setProjectFrame();
}
function setProjectFrame(){
	var total_height = document.documentElement.clientHeight;
	document.getElementById('project-area').style.height = total_height+'px';
	document.getElementById('main').style.height = total_height+'px';
	document.getElementById('device-area').style.height = total_height+'px';
	document.getElementById('project-infos').style.height = total_height+'px';
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
		var element = getProjectLabel(projectInfo['id'], projectInfo['name'], projectInfo['track']);
		$('#project-content').append(element);
	}
}

function getProjectLabel (project_id, project_name, track) {
	return '<li track="'+track+'" project-id='+project_id+'>' + 
			project_name + '</li>';
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
            }else{
                showMsg("Project create failed");
            }
		}
	})
}
// add the new project into #project-content
function addProject (name, track, id) {
	$('#project-content').append(getProjectLabel(id, name, track));
	showMsg('New Project Saved')
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
				addDevices(result['name'], result['id']);
			}else{
				showMsg('Device create failed');
			}
		}
	})
}
function addDevices (name, id) {
	$('ul#device-content').append(getChainDiv(id, name));
	showMsg("New Device Saved");
}
function getChainDiv(id, name){
	return '<li chain-id="'+id+'">'+name+'</li>'
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
		$('#device-content').append(getChainDiv(result[i]['id'], result[i]['name']));
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
				$('.altering').text(project_name);
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
		modal.attr("todo","add");
		modal.modal('show');
	}
}, '#add-project');


// submit-project click
$(document).on({
	click:function(){
		var name = $('#project-name').val(),
		track_id = $('#tracks').val();
		track_name = $('#tracks option:selected').text();
		var todo = $('#addProject').attr('todo');
		if(todo=='add'){
            createProject(name, track_id);
		}else if(todo=='alter'){
			var alter_id = $('#addProject').attr('alter_id');
			console.log(alter_id +"   "+name);
            alterProjectName(alter_id, name);
            alterProjectTrack(alter_id, track_id, track_name);
            $('#addProject').modal('hide');
		}
		
	}
},'#submit-project');


//修改 project 按钮
$(document).on({
    click:function(){
    	if($('.project-label-click').length==1){
    		setTracks();// get tracks 
    		var element = $('.project-label-click');
    		var modal = $('#addProject');
	    	$('#addProject .modal-header h4').text("alter your project");
	    	var id = element.attr("project-id");
	    	$('.altering').removeClass('altering');
	    	element.toggleClass('altering');//为这个project 加标记
	    	modal.attr("todo","alter").attr("alter_id",id);
	    	modal.modal('show');
    	}else{
    		$('#waring-modal').modal('show');
    	}
   }
},"#edit-project");
//  add a new device 
$(document).on({
	click:function(){
		$('#addDevice').modal('show');
	}
},'#add-device');

// create a new device click
$(document).on({
	click:function(){
		var name = $('#device-name').val(),
		id = $('ul#device-content ').attr('project-id');
		createDevice(name, id)
	}
}, '#createChain');

// project-label click
$(document).on({
    click:function(){
    	$('#device-content').empty();
    	$('div#project-area ul#project-content li').addClass("project-label-click").toggleClass("project-label-click");
    	$(this).toggleClass("project-label-click");
    	$('#device-content').attr('project-id', $(this).attr('project-id'));
    	var project = $(this).text() + ' ' +$(this).attr('track');
    	$('#project').text(project);
    	$('#track').text('');
    	getProjectChains($(this).attr('project-id'));
    }
},'div#project-area ul#project-content li');

// track click
$(document).on({
    click:function(){
    	$('div#device-area ul#device-content li').removeClass("device-label-click");
    	$(this).addClass("device-label-click");
    	var track = $(this).text();
    	$('div#infos-content h1').text(track);
    	$('#track').text(track); 
    	var chain_id = $(this).attr('chain-id');
    	$('div#infos-content button').attr('chain-id', chain_id);
    	showChainImage(chain_id);
    	getChainLength(chain_id);
    }
},'div#device-area ul#device-content li');

$(document).on({
	click:function(){
		window.location = '/home/dashboard?id=' + $(this).attr('chain-id');
	}
},'#infos-content button#doDesign');
$(document).on({
	mouseover:function(){
		$('div#project-infos ul#dropdown-menu').removeClass('menu-hide');
	},
	mouseout:function(){
		$('div#project-infos ul#dropdown-menu').addClass('menu-hide');
	}
},'div#project-infos div#dropdown, div#project-infos ul#dropdown-menu');


function showMsg(msg){
    $('div.hint-info').html(msg);
    $('div.hint-info').removeClass('hide');
    $('div.hint-info').show(200).delay(1000).hide(200);
}









