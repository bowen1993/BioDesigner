var part_id='0000';
var part_name='1111';
var part_type='2222';
var drop_index=1;
var isReceived=0;//零代表未接收 一代表已接受
var copy_id;
var copy_name;
var copy_type;
var isCopy=0;
$(document).ready(function(){
        setFrame();
        //为本地的接收组件设置为可接受
        setDroppable($('.receive_style'));
        //setAddDroppable($('.add_style'));
        getProjects();
        //为搜索按钮加事件
        $(document).on({
            click:function(){
                var input=$('#search_part_input').val();
                getSearchPart(input);
            }
        },'#search_part_button');
        //为组件 添加 点击出 信息 事件
        $(document).on({
            click:function(){
                $('.part_active').removeClass('part_active');
                $(this).addClass('part_active');
                var part_name = $(this).attr('part_name');
                getPartInfo(part_name);
            }
        },'.show_message');

        //新加的

        $(document).on({
            mousedown: function(e){
                if(e.which==3){
                    //处理组件右键事件
               
                    copy_id=this.getAttribute('part_id');
                    copy_name=this.getAttribute('part_name');
                    copy_type=this.getAttribute('part_type');

                    var html="<div class='click_div'></div>";
                    var click_div=$(html);
                    html="<div class='copy'>Copy</div>";
                    var copy=$(html);
                    html="<div class='part_remove'>Delete</div>";
                    var remove=$(html);
                    click_div.prepend(copy).prepend(remove);
                    $(this).parent().prepend(click_div);
                }
            }
        },'.operation_part_style');
        $(document).on({
            mousedown: function(e){
                if(e.which==3){
                    //处理右键点击出复制 删除
                    var html="<div class='click_div'></div>";
                    var click_div=$(html);
                    html="<div class='paste'>Paste</div>";
                    var copy=$(html);
                    html="<div class='delete'>Delete</div>";
                    var remove=$(html);
                    click_div.prepend(copy).prepend(remove);
                    $(this).prepend(click_div);
                }
            }

        },'.receive_click');
        $(document).on({
            click: function(){
                isCopy=1;
                var elems=$(this).parent().next('*');
                copy_id=elems.attr('part_id');
                copy_name=elems.attr('part_name');
                copy_type=elems.attr('part_type');
            }
        },'.copy');
        $(document).on({
            click:function(){
               var receive_div=$("<div class='col-lg-2 col-md-2 col-sm-2 col-xs-2 receive_style receivable receive_click' ></div>");
               setDroppable(receive_div);
               $(this).parent().parent().replaceWith(receive_div);
               saveChain();
               //return false;
               //event.preventDefault(); 
           }
        },'.part_remove');
        $(document).on({
            click:function(){
                if(isCopy==1){
                part_id=copy_id;
                part_name=copy_name;
                part_type=copy_type;
                drop_index=$(this).parent().parent().prevAll('*').length;
                
                getInsert();
                saveChain();
                }
            }
            
        },'.paste');
        $(document).on({
            click:function(){
                var elems=$(this).parent().parent();
                var dele=elems.next('*').add(elems);
                dele.remove();
                saveChain();
            }
        },'.delete');

        //新加的结束
        
        $(document).on({
            click : function(){
                $('.project-item-active').removeClass('project-item-active');
                $(this).addClass('project-item-active');
                $('#right_container').attr('project_id', $(this).attr('project-id'));
                //get project chain
                getProjectChain($(this).attr('project-id'));
            }
        }, '.switch-project');
        //为右侧按钮加事件
        $(document).on({
            click:function(){
                var add_button=$("<div class=\"col-lg-1 col-md-1 col-sm-1 col-xs-1 add_style add_button_receive\"><span class=\"glyphicon glyphicon-plus\"></span></div>");
                var receive_div=$("<div class='col-lg-2 col-md-2 col-sm-2 col-xs-2 receive_style receivable receive_click' ></div>");
                //setAddDroppable(add_button);
                setDroppable(receive_div);
                $(this).after(receive_div.add(add_button));
                //setFrame();
            }
        },'.add_style');
        getTracks()
});
function setFrame () {
    var total_width=document.documentElement.clientWidth;//获得屏幕宽度
    if(total_width<800)
    {
        total_width=800;
    }
    var total_height=document.documentElement.clientHeight;//获得屏幕高度
    if(total_height<400)
    {
        total_height=400;
    }
    var search_result_height = $('#tab_container').height()*0.7;
    var project_list_height = $('#tab_container').height()*0.7;
    var part_info_height = total_height * 0.8;
    $('.result_container').css("height", search_result_height);
    $('#project_container').css("height", project_list_height);
    $('#part_info').css("height", part_info_height);
}

function addChainPart(infos){
    var name = infos['part_name'],
        id = infos['part_id'],
        type = infos['part_type'],
        receive_div = $(getReceiveDiv(false)),
        add_button = $(getAddButtonHtml());
    var opeartion_part = $(getOperationPart(id, name, type))
    //setAddDroppable(add_button);
    //setDroppable(receive_div);
    setOperationDraggable(opeartion_part);
    receive_div.append(opeartion_part);
    $('#operation').append(receive_div);
    $('#operation').append(add_button);
    
}

function showChain(result){
    if (result['isSuccessful']){
        chain = result['chain']
        $('#operation').html('');
        var button_before = $(getAddButtonHtml());
        //setAddDroppable(button_before);
        $('#operation').append(button_before);
        for (var i = 0; i < chain.length; i++){
            addChainPart(chain[i])
        }
    }else{
        showMsg("Chain not gained")
    }
}

function getProjectChain(id){
    cleanDesign();
    $.ajax({
        url : "/home/getChain?id=" + id,
        type: "GET",
        success : function(result){
            showChain(result);
        }
    });
}

function showProjects(result){
    if (result['isSuccessful']){
        pro_list = result['projects']
        $('#project-info').tmpl(pro_list).appendTo('#project_container');
    }else{
        showMsg("Error, can't get project information");
    }
}

function getProjects(){
    $.ajax({
        url : "/home/getUserProject",
        type : "GET",
        success : function(result){
            showProjects(result);
        }
    });
}

function getOperationPart(id, name, type){
    return "<div part_id='"+id+"' part_name='"+name+"' part_type='"+
           type+"' class='show_message operation_part_style'><img src=\"/static/img/"+type+".png\" alt=\"logo\" class=\"img-rounded\" style=\"width: 60px;height: 30px;\" />"+name+"</div>";
}

function getAddButtonHtml(){
    return "<div class=\"col-lg-1 col-md-1 col-sm-1 col-xs-1 add_style add_button_receive\"><span class=\"glyphicon glyphicon-plus\"></span></div>";
}

function getReceiveDiv(isReceived){
    if (isReceived){
        return "<div class='col-lg-2 col-md-2 col-sm-2 col-xs-2 receive_style receivable receive_click' ></div>";
    }
    else{
        return "<div class='col-lg-2 col-md-2 col-sm-2 col-xs-2 receive_style receivable' ></div>";
    }
    
}

function cleanDesign(){
    //saveChain();
    $('#operation').html('');
    var button_before = $(getAddButtonHtml()),
        receive_div = $(getReceiveDiv(true)),
        button_after = $(getAddButtonHtml());
    //setAddDroppable(button_before);
    //setAddDroppable(button_after);
    setDroppable(receive_div);
    $('#operation').append(button_before);
    $('#operation').append(receive_div);
    $('#operation').append(button_after);
}

function showMsg(msg){
    $('div.hint-info').html(msg);
    $('div.hint-info').removeClass('hide');
    $('div.hint-info').show(200).delay(1000).hide(200);
}

function addProject(name, id, creator){
    var html = '<div class="project-item switch-project" project-id="'+id+'">'+name+'Created by '+creator+'</div>'
    $('#project_container').prepend(html);
}

function createProject(){
    var name = $('input#new-pro-name').val(),
    id = $('select#tracks').val();
    var postData = {
        'name' : name,
        'track' : id
    }
    $.ajax({
        url:"/home/newProject",
        type:"POST",
        data:postData,
        dataType : "JSON",
        success : function(result){
            $('#new-project').modal('hide');
            if(result['isSuccessful']){
                cleanDesign();
                addProject(result['project_name'], result['id'],result['creator'])
                showMsg("Project created");
                $('#right_container').attr('project_id', result['id'])
            }else{
                showMsg("Project create failed");
            }
        }
    });
}

function addTracks(result){
    if (result['isSuccessful']){
        $('#tracks').html('')
        track_list = result['tracks']
        for(var i = 0; i < track_list.length; i++){
            var newOption = $('<option></option>')
            newOption.html(track_list[i]['track'])
            newOption.val(track_list[i]['id'])
            $('#tracks').append(newOption)
        }
    }
}

function getTracks(){
    $.ajax({
        url:'/home/tracks',
        type:'GET',
        success : function(result){
            addTracks(result)
        }
    });
}

window.onresize=function(){
    setFrame();
}   
function getSearchPart(input){
    $.ajax({
        url:'/home/search?keyword='+input,
        type:'GET' ,
        dateType:'JSON',
        success:function(result){
            $('#part_result_container').empty();
            $('#search_part').tmpl(result).appendTo('#part_result_container'); 
            setDraggable($('.part_style'));
        }
    });
}
function setDraggable(elems){
    elems.draggable({
        helper:function(){
            var html="<div class='drag'>"+this.getAttribute('part_name')+"</div>";
            return $(html);
        },
        start:function(){
            part_id=this.getAttribute('part_id');
            part_name=this.getAttribute('part_name');
            part_type=this.getAttribute('part_type');
        }
    });
}
function setOperationDraggable(elems){
    elems.draggable({
        helper:function(){
            var html="<div class='drag'>"+this.getAttribute('part_name')+"</div>";
            return $(html);
        },
        start:function(){

            drop_index=$(this).parent().prevAll('*').length;
            
            part_id=this.getAttribute('part_id');
            part_name=this.getAttribute('part_name');
            part_type=this.getAttribute('part_type');            
            var par=$(this).parent();
            setDroppable(par);
            $(this).remove();
        },
        stop:function(){ 
            
            if(success==0){
                //alert("here");
                getInsert();
                if(drop_index%2==0){
                    //alert("shiling");
                    var add_button=$("<div class=\"col-lg-1 col-md-1 col-sm-1 col-xs-1 add_style add_button_receive\"><span class=\"glyphicon glyphicon-plus\"></span></div>");
                    //setAddDroppable(add_button);
                    $('#operation').children().filter('*').eq(drop_index).replaceWith(add_button);
                }
            }
        }
    });
}
function setDroppable(elems){
    elems.droppable({        
        drop:function(){
            drop_index=$(this).prevAll('*').length;
            getInsert();
            saveChain();
        },
        out:function(){
            success=0;
        },
        over:function(){
            success=1;
        },
        hoverClass:"receive_hover"
    });
}
function setAddDroppable(elems){
    elems.droppable({        
        drop:function(){
            drop_index=$(this).prevAll('*').length;
            getAdd();
            saveChain();
        },
        out:function(){
            success=0;
        },
        over:function(){
            success=1;
        },
        hoverClass:"receive_hover"
    });
}

function saveChain(){
    var chain = getCurrChain(),
    project_id = $('#right_container').attr('project_id');
    if( project_id.length == 0){
        showMsg("No project selected");
        return;
    }
    var postData = {
        'chain' : chain,
        'id' : project_id
    }
    $.ajax({
        url:'/home/updateChain',
        type:'POST',
        data:postData,
        dataType: 'JSON',
        success : function(result){
            if(result['isSuccessful']){
                showMsg('Save Success');
            }else{
                showMsg('Save Failed');
            }
        }
    });
}

function getPartInfo(part_name){
    $.ajax({
        url : "/home/get?partname=" + part_name,
        type : "GET",
        success : function(result){
            showPartInfo(result)
        }
    });
}

function showPartInfo(result){
    if (result['isSuccessful']){
        $('#part_info').removeClass('hide');
        $('#part_info h3').html(result['part_name']);
        $('#part_info div.part_type').html('Type: ' + result['part_type']);
        $('#part_info div.part_nickname').html('Nickname: '+result['nickname']);
        $('#part_info div.part_short_desc').html(result['short_desc']);
        $('#part_info div.part_description').html(result['description']);
        console.log(result['part_url']);
        $('#part_info div.part_url a').html(result['part_url'])
        $('#part_info div.part_url a').attr('href' ,result['part_url'])
        //$('#part_info div.part_sequence').html(result['sequence']);
    }
}

function getCurrChain(){
    var chain = "";
    $('.operation_part_style').each(function(index,elem){
        chain=chain+"_"+elem.getAttribute('part_id');
    });
    return chain;
}

//获取左侧推荐的组件
function getRecommend(){
    var message = getCurrChain();
    $.ajax({
        url:'/home/arecommend?seq='+ message,
        type:'GET',
        dataType:'JSON',
        success:function(result){
            result_list = result['recommend_list'];
            $('#recommand_search_container').empty();
            var insertElems=$('#recommand_part').tmpl(result_list);
            setDraggable(insertElems);
            insertElems.appendTo('#recommand_search_container');
        }
    });
}
//获取操作区推荐的组件
function getOperationRecommend(here){

    $.ajax({
        url:'/home/seqRecommend?part='+part_id,
        type:'GET',
        dateType:'JSON',
        success:function(result){
            if(result['isSuccessful']){
                result_list = result['recommend_list'][0];
                var insertElems=$('#recommand_part_list').tmpl(result_list);
                setDraggable(insertElems);
                var recommand_div=$("<div class='recommand_div row'></div>");
                recommand_div.append(insertElems);
                var s= $('#operation').children().filter('*').eq(here);
                s.css("position","relative").append(recommand_div);
            }
            
            //setFrame();
                   
        }
    });
   
}
function getInsert(){
    $('.recommand_div').remove();
    $('#operation').children().filter('*').eq(drop_index).remove();
    var html="<div part_id='"+part_id+"' part_name='"+part_name+"' part_type='"+
           part_type+"' class='show_message operation_part_style'><img src=\"/static/img/"+part_type+".png\" alt=\"logo\" class=\"img-rounded\" style=\"width: 60px;height: 30px;\" />"+part_name+"</div>";
    var operation_div=$(html);
    setOperationDraggable(operation_div);
    html="<div class='col-lg-2 col-md-2 col-sm-2 col-xs-2 receive_style receivable' ></div>";
    var receive_div=$(html).prepend(operation_div);
    $('#operation').children().filter('*').eq(drop_index-1).after(receive_div);   
    getRecommend();
    getOperationRecommend(drop_index);
    //setFrame();
    success=0;
}
function getAdd(){
    $('.recommand_div').remove();
    var html="<div part_id='"+part_id+"' part_name='"+part_name+"' part_type='"+
           part_type+"' class='show_message operation_part_style'><img src=\"/static/img/"+part_type+".png\" alt=\"logo\" class=\"img-rounded\" style=\"width: 60px;height: 30px;\" />"+part_name+"</div>";
    var operation_div=$(html);
    setOperationDraggable(operation_div);
    html="<div class='col-lg-2 col-md-2 col-sm-2 col-xs-2 receive_style receivable' ></div>";
    var receive_div=$(html).prepend(operation_div);
    html="<div class=\"col-lg-1 col-md-1 col-sm-1 col-xs-1 add_style add_button_receive\"><span class=\"glyphicon glyphicon-plus\"></span></div>";
    var add_div=$(html);
    //setAddDroppable(add_div);
    var t=receive_div.add(add_div);
    $('#operation').children().filter('*').eq(drop_index).after(t);
    getRecommend();
    getOperationRecommend(drop_index+1);
    //setFrame();
    success=0;
}

