var part_id;
var part_name;
var part_type;
var drop_index=1;
var leave_index;
var isReceived=0;//零代表未接收 一代表已接受
var copy_id;
var copy_name;
var copy_type;
var isCopy=0;//0代表没有复制
//监听视口变化
window.onresize=function(){
    setFrame();
}   
$(document).ready(function(){
        var total_width=document.documentElement.clientWidth;//获得屏幕宽度
        if(total_width<1400){
            setDashBoardFrame(700);
        }else{
            setDashBoardFrame(1000);
        }
        setFrame();
        setDashBoardFloat();
        //为本地的接收组件设置为可接受
        setDroppable($('.receive_style'));
        setAddDroppable($('.add_style'));

        getProjects();
        //为搜索加事件
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
                $('.click_div').remove();
            }
        },'.show_message');
        /*
         //处理右键点击出复制 删除
        $(document).on({
            mousedown: function(e){
                if(e.which==3){
                    $('.click_div').remove();
                    //copy_id=this.getAttribute('part_id');
                    //copy_name=this.getAttribute('part_name');
                    //copy_type=this.getAttribute('part_type');
                    var html="<div class='click_div'></div>";
                    var click_div=$(html);
                    html="<div class='copy'>copy</div>";
                    var copy=$(html);
                    html="<div class='part_remove'>delete</div>";
                    var remove=$(html);
                    click_div.prepend(copy).prepend(remove);
                    $(this).parent().prepend(click_div);
                }
            }
        },'.operation_part_style');

         //处理右键点击出粘贴 删除
        $(document).on({
            mousedown: function(e){
                if(e.which==3){
                    $('.click_div').remove();
                    var html="<div class='click_div'></div>";
                    var click_div=$(html);
                    html="<div class='paste'>paste</div>";
                    var copy=$(html);
                    html="<div class='delete'>delete</div>";
                    var remove=$(html);
                    click_div.prepend(copy).prepend(remove);
                    $(this).prepend(click_div);
                }
            }
        },'.receive_click');

        //点击 复制
        $(document).on({
            click: function(){
                isCopy=1;
                var elems=$(this).parent().next('*');
                copy_id=elems.attr('part_id');
                copy_name=elems.attr('part_name');
                copy_type=elems.attr('part_type');

                $('.click_div').remove();
            }
        },'.copy');
        //点击  删除组件
        $(document).on({
            click:function(){
               var receive_div=$("<div class=' receive_style receivable receive_click' ></div>");
               setDroppable(receive_div);
               $(this).parent().parent().replaceWith(receive_div);
               $('.click_div').remove();
           }
        },'.part_remove');

        //点击粘贴 
        $(document).on({
            click:function(){
                if(isCopy==1){
                part_id=copy_id;
                part_name=copy_name;
                part_type=copy_type;
                drop_index=$(this).parent().parent().prevAll('*').length;
                getInsert();
                }
                $('.click_div').remove();
            }   
        },'.paste');

        //点击删除 接收组件
        $(document).on({
            click:function(){
                var elems=$(this).parent().parent();
                var dele=elems.next('*').add(elems);
                dele.remove();
                $('.click_div').remove();
            }
        },'.delete');
        */
        $(document).on({
            click : function(){
                $('.click_div').remove();
                $('.project-item-active').removeClass('project-item-active');
                $(this).addClass('project-item-active');
                $('#right_container').attr('project_id', $(this).attr('project-id'));
                //get project chain
                getProjectChain($(this).attr('project-id'));
            }
        }, '.switch-project');

        //为加号按钮设置点击的事件
        $(document).on({
            click:function(){
                $('.click_div').remove();
                var add_button=$("<div class=\" add_style btn-back add_button_receive\"><span class=\"glyphicon glyphicon-plus\"></span></div>");
                var receive_div=$("<div class='receive_style receivable receive_click' ></div>");
                setAddDroppable(add_button);
                setDroppable(receive_div);
                var new_cell = $('<div class="part-cell col-lg-2 col-md-2 col-sm-3 col-xs-4"></div>');
                new_cell.append(receive_div);
                new_cell.append(add_button);
                $(this).parent().after(new_cell);
                setDashBoardFloat();//重新设置浮动
            }
        },'.btn-back');

        $(document).on({
            click:function(){
                $('.click_div').remove();
                var add_button=$("<div class=\" add_style btn-front add_button_receive\"><span class=\"glyphicon glyphicon-plus\"></span></div>");
                var receive_div=$("<div class='receive_style receivable receive_click' ></div>");
                setAddDroppable(add_button);
                setDroppable(receive_div);
                var new_cell = $('<div class="part-cell col-lg-2 col-md-2 col-sm-3 col-xs-4"></div>');
                new_cell.append(receive_div);
                new_cell.append(add_button);
                $(this).parent().before(new_cell);
                setDashBoardFloat();//重新设置浮动
            }
        },'.btn-front');

        getTracks()
});
//清除操作区弹出的推荐组件
function clear(){
    $('.click_div').remove();
}
//设置框架大小
function setFrame () {
    var total_width=document.documentElement.clientWidth;//获得屏幕宽度
    if(total_width<800){
        total_width=800;
    }
    var total_height=document.documentElement.clientHeight;//获得屏幕高度
    if(total_height<400){
        total_height=400;
    }

    $('#container').css("height",total_height).css("width",total_width);
    var bananer_height = $('#bananer').height();
    var main_height = total_height-bananer_height;
    $('#main').css("height",main_height);//设置主区域高度

    var sidebar_width = $('#sidebar').width();
    var dashboard_container_width = total_width-sidebar_width;
    $('#dashboard_container').css("width",dashboard_container_width);//设置操作区宽度

    var search_part_container_height = main_height*0.6;
    var recommand_container_height = main_height-search_part_container_height;
    $('#search_part_container').css("height",search_part_container_height);//设置search_part_container高度
    $('#recommand_container').css("height",recommand_container_height);//设置推荐区域高度
    
    var title_height = $('.title').height();
    var search_container_height = $('.search_container').height();
    var result_container_height = search_part_container_height-title_height-search_container_height;
    $('#part_result_container').css("height",result_container_height);
    $('#recommand_search_container').css("height",recommand_container_height-title_height);
}


function addChainPart(infos){
    var name = infos['part_name'],
        id = infos['part_id'],
        type = infos['part_type'],
        receive_div = $(getReceiveDiv()),
        add_button = $(getAddButtonHtml());
    var opeartion_part = $(getOperationPart(id, name, type))
    //setAddDroppable(add_button);
    setDroppable(receive_div);
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
//获取操作区组件的 html
function getOperationPart(id, name, type){
    return "<div part_id='"+id+"' part_name='"+name+"' part_type='"+
           type+"' class='show_message operation_part_style'><img src=\"/static/img/"+type+".png\" alt=\"logo\" class=\"img-rounded\" style=\"width: 60px;height: 30px;\" />"+name+"</div>";
}
//获取操作区加号按钮的 html
function getAddButtonHtml(){
    return '<div class="add_style btn-back add_button_receive"><span class=" glyphicon glyphicon-plus"></span></div>';
}
//获取操作区接收组件的 html
function getReceiveDiv(){
    return '<div class="receive_style receivable receive_click"></div>';
}

function getPartCellDiv(){
    return '<div class="part-cell col-lg-2 col-md-2 col-sm-3 col-xs-4"></div>';
}
//巩的方法
function cleanDesign(){
    //saveChain();
    $('#operation').html('');
    var button_before = $(getAddButtonHtml()),
        receive_div = $(getReceiveDiv()),
        button_after = $(getAddButtonHtml());
    //setAddDroppable(button_before);
   //setAddDroppable(button_after);
    setDroppable(receive_div);
    $('#operation').append(button_before);
    $('#operation').append(receive_div);
    $('#operation').append(button_after);
}
//巩的方法
function showMsg(msg){
    $('div.hint-info').html(msg);
    $('div.hint-info').removeClass('hide');
    $('div.hint-info').show(200).delay(1000).hide(200);
}
//巩的方法
function addProject(name, id, creator){
    var html = '<div class="project-item switch-project" project-id="'+id+'">'+name+'Created by '+creator+'</div>'
    $('#project_container').prepend(html);
}
//巩的方法
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
//巩的方法
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
//巩的方法
function getTracks(){
    $.ajax({
        url:'/home/tracks',
        type:'GET',
        success : function(result){
            addTracks(result)
        }
    });
}

//获取组件搜索的结果并显示出来
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
//设置左侧组件的拖放
function setDraggable(elems){
    elems.draggable({
        helper:function(){
            var html="<img style=\" width:50px;height:50px;background:white \"  />";
            return $(html);
        },
        start:function(){
            $('.click_div').remove();
            part_id=this.getAttribute('part_id');
            part_name=this.getAttribute('part_name');
            part_type=this.getAttribute('part_type');
        }
    });
}
//设置操作区组件的拖放
function setOperationDraggable(elems){
    elems.draggable({
        helper:function(){
            var html="<div class='drag'>"+this.getAttribute('part_name')+"</div>";
            return $(html);
        },
        start:function(){
            $('.click_div').remove();
            $('.recommand_div').remove();
            leave_index=$(this).parent().prevAll('*').length;
            
            part_id=this.getAttribute('part_id');
            part_name=this.getAttribute('part_name');
            part_type=this.getAttribute('part_type');            
            var par=$(this).parent();
            par.addClass('receive_click');
            setDroppable(par);
            $(this).remove();
        },
        stop:function(){ 
            /*
            if(success==0){
                drop_index=leave_index;
                getInsert();
                
            }*/
        }
    });
}
function setBigDroppable(elems){
    elems.droppable({
        drop:function(){
            alert("大的被触发");
        }
    });
}
//设置操作区 接收组件
function setDroppable(elems){
    elems.droppable({        
        drop:function(){
            drop_index=$(this).prevAll('*').length;
            getInsert(this);
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

//设置操作区 加号按钮的接收
function setAddDroppable(elems){
    elems.droppable({        
        drop:function(){
            drop_index=$(this).prevAll('*').length;//获取接收的按钮的位置，0开始
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
//巩的方法
function saveChain(){
    var chain = getCurrChain();
    var postData = {
        'chain' : chain,
        'id' : window.chainId
    };
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
//获取组建的详细信息
function getPartInfo(part_name){
    $.ajax({
        url : "/home/get?partname=" + part_name,
        type : "GET",
        success : function(result){
            showPartInfo(result)
        }
    });
}
//巩的方法
function showPartInfo(result){
    if (result['isSuccessful']){
        $('#part_info').removeClass('hide');
        $('#part_info h3').html(result['part_name']);
        $('#part_info div.part_type').html('Type: ' + result['part_type']);
        $('#part_info div.part_nickname').html('Nickname: '+result['nickname']);
        $('#part_info div.part_short_desc').html(result['short_desc']);
        $('#part_info div.part_description').html(result['description']);
        //console.log(result['part_url']);
        $('#part_info div.part_url a').html(result['part_url'])
        $('#part_info div.part_url a').attr('href' ,result['part_url'])
        //$('#part_info div.part_sequence').html(result['sequence']);
    }
}
//巩的方法
function getCurrChain(){
    var chain = "";
    $('.operation_part_style').each(function(index,elem){
        chain=chain+"_"+elem.getAttribute('part_id');
    });
    return chain;
}
//获取左侧推荐的组件并显示
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
//获取操作区推荐的组件并显示
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
//在一个接收组件上插入操作的组件
function getInsert(obj){
    $('.recommand_div').remove();
    //$('#dashboard').children().filter('*').eq(drop_index).remove();
    var html="<div part_id='"+part_id+"' part_name='"+part_name+"' part_type='"+
           part_type+"' class='show_message operation_part_style'><img src=\"/static/img/"+part_type+".png\" alt=\"logo\" class=\"img-rounded\"  />"+part_name+"</div>";
    var operation_div=$(html);
    setOperationDraggable(operation_div);
    $(obj).append(operation_div);
    /*
    html='<div class="receive_style receivable receive_click"></div>';
    var receive_div=$(html).prepend(operation_div);
    html='<div class="add_style btn-back add_button_receive"><span class=" glyphicon glyphicon-plus"></span></div>';
    var add_div=$(html);
    setAddDroppable(add_div);
    var part_cell = $('<div class="part-cell col-lg-2 col-md-2 col-sm-3 col-xs-4"></div>');
    part_cell.append(receive_div);
    part_cell.append(add_div);
    $('#dashboard').children().filter('*').eq(drop_index-1).after(part_cell);  
    setDashBoardFloat();
    getRecommend();
    getOperationRecommend(drop_index);
    */
    success=0;
}
function getAdd(){
    $('.recommand_div').remove();
    var html="<div part_id='"+part_id+"' part_name='"+part_name+"' part_type='"+
           part_type+"' class='show_message operation_part_style'><img src=\"/static/img/"+part_type+".png\" alt=\"logo\" class=\"img-rounded\"  />"+part_name+"</div>";
    var operation_div=$(html);
    setOperationDraggable(operation_div);
    html='<div class="receive_style receivable receive_click"></div>';
    var receive_div=$(html).prepend(operation_div);
    html='<div class="add_style btn-back add_button_receive"><span class=" glyphicon glyphicon-plus"></span></div>';
    var add_div=$(html);
    setAddDroppable(add_div);
    var part_cell = $('<div class="part-cell col-lg-2 col-md-2 col-sm-3 col-xs-4"></div>');
    part_cell.append(receive_div);
    part_cell.append(add_div);
    $('#dashboard').children().filter('*').eq(drop_index).after(part_cell);
    setDashBoardFloat();
    getRecommend();
    getOperationRecommend(drop_index+1);
    //setFrame();
    success=0;
}

