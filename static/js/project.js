$(document).ready(function(){
    setProjectFrame();
    $('#user-name').html(window.uname)
    getUserProjects();
    setTracks();
});
window.onresize=function(){
	setProjectFrame();
}
function setProjectFrame(){
	var totalHeight = document.documentElement.clientHeight;//获取视口 高度 宽度
	var totalWidth = document.documentElement.clientWidth;
	var bananerHeight = $('#project-bananer').height();//获取bananer 高度
	var projectMainHeight = totalHeight-bananerHeight;//计算主体区域高度
	$('#project-main').css("height",projectMainHeight);//设置主题区域高度
	var projectMainLeftTopHeight = $('#project-main-left-top').height();//获取左侧上方区域高度
	var projectMainLeftBottomHeight = projectMainHeight-projectMainLeftTopHeight;//计算左侧下方区域高度
	$('#project-main-left-bottom').css("height",projectMainLeftBottomHeight);//设置左侧下方区域高度
    var projectMainLeftWidth = $('#project-main-left').width();//获取左侧宽度
    var projectMainRightWidth = totalWidth-projectMainLeftWidth-20;//计算右侧宽度
	$('#project-main-right').css("width",projectMainRightWidth);//设置右侧宽度

	var projectMainRightTopHeight = $('#project-main-right-top').height();
	var projectMainRightBottomHeight = projectMainHeight-projectMainRightTopHeight;
	$('#project-main-right-bottom').css("height",projectMainRightBottomHeight);
	$('#menu').css("height",projectMainRightBottomHeight);
	var menuWidth = $('#menu').width();
	var chainIdfosWidth = projectMainRightWidth-menuWidth;
	$('.chain-infos').css("width",chainIdfosWidth);
}
//获取用户所有project
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
		$('#project-main-left-bottom').append(getProjectLabel(projectInfo['id'], projectInfo['name'], projectInfo['track']));
	}
}
function getProjectLabel (project_id, project_name, track) {
	return '<div class="project-label" track="'+track+'" project-id='+project_id+'>' + 
			project_name + '</div>'
}
//获取track信息
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
function createProject (name, track) {
	var postData = {
		'name':name,
		'track': track
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
// add the new project into #project-main-left-bottom
function addProject (name, track, id) {
	$('#project-main-left-bottom').append(getProjectLabel(id, name, track));
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
	$('#menu').append(getChainDiv(id, name));
	showMsg("New Device Saved");
}
function getChainDiv(id, name){
	return '<div class="track-label" chain-id="'+id+'">'+name+'</div>'
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
		$('#menu').append(getChainDiv(result[i]['id'], result[i]['name']));
	}
}

// delete a project
function deleteProject(project_id){
	var postData = {
		'id':project_id,
	};
	$.ajax({
		url:'/home/deleteProject',
		type:'POST',
		data:postData,
		dataType:'JSON',
		success: function(result){
			showMsg("delete success");
			$('#menu').empty();
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
function alterProjectTrack(project_id, project_track){
    var postData={
    	'id':project_id,
    	'track_id':project_track,
    };
    $.ajax({
    	url:'/home/changeTrack',
    	type:'POST',
    	data:postData,
    	dataType:'JSON',
    	success:function(result){
    		if(result['isSuccessful']){
    			showMsg('success');
    			$('.altering').attr('track',project_track);
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
function getChainLength (chainId) {
	$.ajax({
		url: '/home/getChainLength?id=' + chainId,
		type: 'GET',
		success:function(result){
			if(result['isSuccessful']){
				$('.text-info').find('#length').html('Length: ' + result['length']);
			}else{
				$('.text-info').find('#length').html('Length: 0');
			}
		}
	});
}
function showChainImage(chainId){
	$.ajax({
		url:'/home/getResultImage?id=' + chainId,
		type:'GET',
		success:function(result){
			if (result['isSuccessful']){
				$('.img-info #chain-img').attr('src', result['filepath'].replace('downloads/', 'static/'));
			}else{
				$('.img-info #chain-img').attr('src', '/static/img/logo_black_op.png');
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

//添加project按钮
$(document).on({
	click:function(){
		var modal = $('#addProject');
		$('#addProject .modal-header h4').text("add new project");
		modal.attr("todo","add");
		modal.modal('show');
	}
}, '#addProjectButton');

//修改 project 按钮
$(document).on({
    click:function(){
    	var modal = $('#addProject');
    	$('#addProject .modal-header h4').text("alter your project");
    	var id = $(this).parent().parent().attr("project-id");
    	$('.altering').removeClass('altering');
    	$(this).parent().parent().toggleClass('altering');//为这个project 加标记
    	modal.attr("todo","alter").attr("alter_id",id);
    	modal.modal('show');
    	$('.project-label-over').remove();
    }
},".label-edit");

// create-project click
$(document).on({
	click:function(){
		var name = $('#project-name').val(),
		trackid = $('#tracks').val();
		var todo = $('#addProject').attr('todo');
		if(todo=='add'){
            createProject(name, trackid);
		}else if(todo=='alter'){
			var alter_id = $('#addProject').attr('alter_id');
            alterProjectName(alter_id, name);
            alterProjectTrack(alter_id, trackid);
            $('#addProject').modal('hide');
		}
		
	}
},'#create-project');


// add device click
$(document).on({
	click:function(){
		$('#addDevice').modal('show');
	}
},'#addDeviceBtn');

// project-label click
$(document).on({
    click:function(){
    	$('#menu').empty();
    	$('.project-label').addClass("toggle-class").toggleClass("toggle-class");
    	$(this).toggleClass("toggle-class");
    	$('#menu').attr('project-id', $(this).attr('project-id'));
    	var project = $(this).text() + ' ' +$(this).attr('track');
    	$('#project').text(project);
    	$('#track').text("");
    	getProjectChains($(this).attr('project-id'));
    }
},'.project-label');

// create a new device click
$(document).on({
	click:function(){
		var name = $('#device-name').val(),
		id = $('#menu').attr('project-id');
		createDevice(name, id)
	}
}, '#createChain');

// track click
$(document).on({
    click:function(){
    	$('.track-label').addClass('device-choosen').toggleClass("device-choosen");
    	$(this).toggleClass("device-choosen");
    	var track = $(this).text();
    	$('.text-info').removeClass('hide');
    	getChainLength($(this).attr('chain-id'));
    	$('button#doDesign').attr('chain-id', $(this).attr('chain-id'));
    	$('#part_title').html(track);
    	$('#track').text(track); 
    	showChainImage($(this).attr('chain-id'));
    }
},'.track-label');

//为最上方修改按钮加事件
$(document).on({
	click:function(){
		var html = "<button class=\"label-edit btn btn-primary\">edit</button>";
		var edit = $(html);
		html = "<button class=\"label-delete btn btn-primary\"><span class=\"glyphicon glyphicon-remove\"></span></button>";
		var deleteButton = $(html);
	    html = "<div class=\"project-label-over\"></div>";
		var container = $(html);
		container.append(deleteButton).append(edit);
		$('.project-label').append(container);
	}
},'#editButton');



//为每一个删除按钮加事件
$(document).on({
    click:function(){
    	var project_id = $(this).parent().parent().attr("project-id");//获取删除工程的id
    	$(this).parent().parent().remove();
    	deleteProject(project_id);
    	$('.project-label-over').remove();

    }
},'.label-delete');



$(document).on({
	click:function(){
		window.location = '/home/dashboard?id=' + $(this).attr('chain-id');
	}
},'#doDesign');
$(document).on({
	click:function(){
		$('div.text-info').addClass('hide');
	}
}, '#close_info');





















