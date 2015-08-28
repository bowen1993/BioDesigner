var part_id;
var part_name;
var part_type;
var copy_id;
var copy_name;
var copy_type;
var isCopy;
var recommandIDs = new Array();
var recommandNames = new Array();
var recommandTypes = new Array();
var isOperationDrag;
var leaveElement;
//监听视口变化
window.onresize=function(){
    setFrame();
}   
$(document).ready(function(){
    getProjectChain(window.chainId);
    //消除右键默认事件
    $(document).bind('contextmenu', function (e) {  
        return false;  
    }); 　
    setFrame();//根据浏览器计算框架
    setDroppable($('.receive_style'));//将本地的接收组件设置为可以接受
    setDashboardDroppable($('#dashboard'));
    //为bananer 添加按钮加事件
    $(document).on({
        click:function(){
            var elems = $('ul#select-track').children('li');
            if(elems.length==0){
                //获取track 并添加到 模态框中
                getTracks(); 
            }else{
                $('#myModal').modal('show');
            }           
        }
    },'#bananer button#add');
    //为选择功能按钮加事件
    $(document).on({
        click:function(){
            $('ul#buttonArea').empty();
            var elems = $('#myModal input');
            for(var i = 0; i<elems.length; i++){
                if(elems[i].checked){
                    var span_elem = $(elems[i]).prev('span');
                    var html = 
                        "<li>"+
                            "<span function-id=\""+span_elem.attr('function-id')+"\" class=\"label\">"+span_elem.text()+"</span>"+
                            "<button class=\"close\"><span class=\"glyphicon glyphicon-remove\"></span></button>"+
                        "</li>";
                    var insert = $(html);
                    $('ul#buttonArea').append(insert);
                }
            }
        }
    },'.modal-footer #select');
    //为bananer 标签按钮加事件
    $(document).on({
        click:function(){
            $(this).parent().remove();//删除标签
            //后台交互
        }
    },'#bananer ul#buttonArea li button.close');
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
     //处理右键点击出 复制 粘贴 删除
    $(document).on({
        mousedown: function(e){
            if(e.which==3){
                $('.click_div').remove();
                var html="<div class='click_div'></div>";
                var click_div=$(html);
                if($(this).children('.operation_part_style').length==0){
                    html="<div class='paste'>paste</div>";
                }else{
                    html="<div class='copy'>copy</div>";
                }
                var copy=$(html);
                html="<div class='delete'>delete</div>";
                var remove=$(html);
                click_div.prepend(copy).prepend(remove);
                $(this).prepend(click_div);
            }
        }
    },'.receive_style');
    //点击 复制
    $(document).on({
        click: function(){
            isCopy=1;
            var elems=$(this).parent().parent().children('.operation_part_style');
            copy_id=elems.attr('part_id');
            copy_name=elems.attr('part_name');
            copy_type=elems.attr('part_type');
            $('.click_div').remove();
        }
    },'.copy');
    //点击粘贴 
    $(document).on({
        click:function(){
            if(isCopy==1){
            part_id=copy_id;
            part_name=copy_name;
            part_type=copy_type;
            getInsert( $(this).parent().parent() );
            afterInsert();//进行操作后的推荐及保存
            }
            $('.click_div').remove();
        }   
    },'.paste');
    //点击删除 接收组件
    $(document).on({
        click:function(){
            var isDropped = $(this).parent().next('.operation_part_style').length==1;//判断有没有组件
            var isOnly = $('.part-cell').length==1;//判断是否是唯一的接收组件
            var isFirst = $(this).parent().parent().parent().prevAll('.part-cell').length==0;//判断是否是第一个接收组件
            if(isOnly){
                if(isDropped){
                    $(this).parent().parent().droppable("enable").empty().addClass('receive_style_color');//将接收组件清空
                    saveChain();//保存操作
                }else{
                    $(this).parent().remove();//将弹出的 粘贴删除 清除
                }
            }else{
                $(this).parent().parent().parent().remove();//删除
                setDashBoardFloat();//重新设置浮动
                if(isDropped){
                    getRecommend();//获取左侧推荐
                    saveChain();//保存操作
                }
                if(isFirst){
                    var add_button_front=$("<div class=\" add_style btn-front add_button_receive\"><span class=\"glyphicon glyphicon-plus\"></span></div>");
                    var front = $(add_button_front);
                    $($('.part-cell')[0]).prepend(front);
                }
            }
        }
    },'.delete');

    //为加号按钮设置点击的事件
    $(document).on({
        click:function(){
            $('.click_div').remove();
            //$('.operation_recommends_list').remove();
            var add_button=$("<div class=\" add_style btn-back add_button_receive\"><span class=\"glyphicon glyphicon-plus\"></span></div>");
            var receive_div=$("<div class='receive_style receive_style_color receivable receive_click' ></div>");
            //setAddDroppable(add_button);
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
            //$('.operation_recommends_list').remove();
            var add_button_front=$("<div class=\" add_style btn-front add_button_receive\"><span class=\"glyphicon glyphicon-plus\"></span></div>");
            var add_button_back=$("<div class=\" add_style btn-back add_button_receive\"><span class=\"glyphicon glyphicon-plus\"></span></div>");
            var receive_div=$("<div class='receive_style receive_style_color receivable receive_click' ></div>");
            /*setAddDroppable(add_button_front);
            setAddDroppable(add_button_back);*/
            setDroppable(receive_div);
            var new_cell = $('<div class="part-cell col-lg-2 col-md-2 col-sm-3 col-xs-4"></div>');
            new_cell.append(add_button_front);
            new_cell.append(receive_div);
            new_cell.append(add_button_back);
            $(this).parent().before(new_cell);
            $(this).remove();
            setDashBoardFloat();//重新设置浮动
        }
    },'.btn-front');
    $(document).on({
        click:function(){
            $('div#myModal ul#select-track li.active').removeClass('active');
            $(this).addClass('active');
            var id = this.getAttribute('track-id');
            getFunctions(id);
        }
    },'div#myModal ul#select-track li');
});
//设置框架大小
function setFrame () {
    var total_height = document.documentElement.clientHeight;
    document.getElementById('container').style.height = total_height + 'px';
    var bananer_height = $('#bananer').height();
    var sidebar_height = total_height-bananer_height;
    var search_part_container_height = sidebar_height*0.6;
    var part_result_container_height = search_part_container_height-73;
    $('#part_result_container').css("height",part_result_container_height);
    var recommand_container_height = sidebar_height-search_part_container_height;
    var recommand_search_height = recommand_container_height-33;
    $('#recommand_search_container').css('height',recommand_search_height);
    var operation_recommand_height=$('#operation_recommand_container').height();
    var dashboard_container_height = sidebar_height-operation_recommand_height;
    $('#dashboard_container').css("height",dashboard_container_height);
    setDashBoardFloat();

    // var total_width=document.documentElement.clientWidth;//获得屏幕宽度
    // if(total_width<800){
    //     total_width=800;
    // }
    // var total_height=document.documentElement.clientHeight;//获得屏幕高度
    // if(total_height<400){
    //     total_height=400;
    // }

    // $('#container').css("height",total_height).css("width",total_width);
    // var bananer_height = $('#bananer').height();
    // var main_height = total_height-bananer_height;
    // $('#main').css("height",main_height);//设置主区域高度

    // var sidebar_width = $('#sidebar').width();
    // var main_right_width = total_width-sidebar_width;
    // $('#main_right').css("width",main_right_width);//设置右侧宽度
    // var operation_recommand_height=$('#operation_recommand_container').height();
    // var dashboard_container_height = main_height-operation_recommand_height;
    // $('#dashboard_container').css("height",dashboard_container_height);

    // var search_part_container_height = main_height*0.6;
    // var recommand_container_height = main_height-search_part_container_height;
    // $('#search_part_container').css("height",search_part_container_height);//设置search_part_container高度
    // $('#recommand_container').css("height",recommand_container_height);//设置推荐区域高度
    
    // var title_height = $('.title').height();
    // var search_container_height = $('.search_container').height();
    // var result_container_height = search_part_container_height-title_height-search_container_height;
    // $('#part_result_container').css("height",result_container_height);
    // $('#recommand_search_container').css("height",recommand_container_height-title_height);

     
}
function getFunctions(track_id){
    // $.ajax({
    //     url:'/home/getTrackFunctions?track_id='+track_id,
    //     type:'GET',
    //     success:function(result){
    //         if(result['isSuccessful']){
    //             addFunctions(result['functions']);
    //         }
    //     }
    //});
var result = {"functions": [{"id": 25, "name": "artificial biofilm"}, {"id": 30, "name": "Genetic memory devices "}, {"id": 27, "name": "water purification"}, {"id": 26, "name": "degrading, and decolourising azo-dyes"}, {"id": 28, "name": "genetic lock"}, {"id": 29, "name": "intracellular calcium spikes"}, {"id": 61, "name": "phage cocktail"}, {"id": 64, "name": "biological signals"}, {"id": 38, "name": "target gene replacement "}, {"id": 63, "name": "chlorophyll biosynthetic pathway "}, {"id": 80, "name": "gene therapy"}, {"id": 85, "name": "environment  threaten"}, {"id": 84, "name": "decontamination"}, {"id": 99, "name": "extract metal\u2028"}, {"id": 98, "name": "raising n-butanol"}, {"id": 90, "name": "circuits implementing intercellular regulation"}, {"id": 104, "name": "electricity"}, {"id": 106, "name": "antibiotic resistant bacteria"}, {"id": 143, "name": "protein libraries "}, {"id": 177, "name": "bio-imaging system"}, {"id": 175, "name": "detecte and prevent bacteria"}, {"id": 157, "name": "degrade smelly molecules"}, {"id": 170, "name": "human body for healthcare"}], "isSuccessful": true};
            if(result['isSuccessful']){
                addFunctions(result['functions']);
            }
}
function addFunctions(functions){
    $('div#myModal ul#select-function').empty();
    for(var i = 0; i<functions.length; i++){
        var li_elem = $("<li></li>");
        var html = "<span function-id=\""+functions[i]['id']+"\">"+functions[i]['name']+"</span>";
        li_elem.append($(html));
        html = "<input type=\"checkbox\"/>";
        li_elem.append($(html));
        $('div#myModal ul#select-function').append(li_elem);
    }
}
function getTracks(){
    $.ajax({
        url:'/home/tracks',
        type:'GET',
        success:function(result){
            if(result['isSuccessful']){
                addTracks(result['tracks']);
            }
        }
    });
}
function addTracks(tracks){
    for(var i = 0; i<tracks.length; i++){
        var html = "<li track-id=\""+tracks[i]['id']+"\">"+tracks[i]['track']+"</li>";
        $('div#myModal ul#select-track').append($(html));
    }
    $('#myModal').modal('show');
}
function insertChain(chain){
    var html="<div class=\"part-cell col-lg-2 col-md-2 col-sm-3 col-xs-4 \"> " +
        "<div class=\"receive_style receive_click\">" + 
            "<div class=\"show_message operation_part_style\" part_type=\""+chain['part_type']+"\" part_name=\""+chain['part_name']+"\" part_id=\""+chain['part_id']+"\">" + 
                "<img class=\"img-rounded\" alt=\"logo\" src=\"/static/img/"+chain['part_type']+".png\">" + 
                "<span>" +chain['part_name']+"</span>" + 
            "</div>" + 
        "</div>" + 
        "<div class=\"add_style btn-back add_button_receive\"><span class=\" glyphicon glyphicon-plus\"></span></div>" +
    "</div>";
    return $(html);
}
function showChain(result){
    if (result['isSuccessful']){
        chain = result['chain'];
        var chainLength = chain.length;
        if (chainLength != 0){
            $('#dashboard').empty();
            for( var i=0; i<chain.length; i++){
                var insert = insertChain(chain[i]);
                insert.appendTo('#dashboard');
            }
            var add_button_front=$("<div class=\" add_style btn-front add_button_receive\"><span class=\"glyphicon glyphicon-plus\"></span></div>");
            //$(add_button_front).prependTo($( $('.part-cell')[0] ));
            $($('.part-cell')[0]).prepend(add_button_front);
            setDroppable( $('.receive_style'));
            $('.receive_style').droppable('disable');
            setOperationDraggable( $('.operation_part_style') );
            setDashBoardFloat();
        }        
    }else{
        showMsg("Chain not gained")
    }
}
function getProjectChain(id){
    $.ajax({
        url : "/home/getChain?id=" + id,
        type: "GET",
        success : function(result){
            showChain(result);
        }
    });
}
function showMsg(msg){
    $('div.hint-info').html(msg);
    $('div.hint-info').removeClass('hide');
    $('div.hint-info').show(200).delay(1000).hide(200);
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
            var html="<div class='drag'>"+this.getAttribute('part_name')+"</div>";
            return $(html);
        },
        start:function(){
            $('.click_div').remove();
            //$('.operation_recommends_list').remove();
            part_id=this.getAttribute('part_id');
            part_name=this.getAttribute('part_name');
            part_type=this.getAttribute('part_type');
        },
        cursor:'crosshair',
        cursorAt:{top:10,left:40}
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
            leaveElement = $(this).parent();//记录离开的位置
            //$('.operation_recommends_list').remove(); 
            part_id=this.getAttribute('part_id');
            part_name=this.getAttribute('part_name');
            part_type=this.getAttribute('part_type');            
            //var par=$(this).parent();
            // par.addClass('receive_click');
            $(this).parent().droppable('enable').addClass('receive_style_color');//将父元素 设置为可以接受组件
            $(this).remove();
        },
        cursor:'crosshair',
        cursorAt:{top:10,left:40}
    });
}
//设置操作区 推荐组件的拖放
function setOperationRecommandDraggable(elems){
    elems.draggable({
        helper:function(){
            return $("<div>dragging</div>");
        },
        start:function(){
            isOperationDrag = 1;
            setRecommandArray($(this));
        },
        cursor:'crosshair',
        cursorAt:{top:10,left:40}

    });
}
function setRecommandArray(obj){
    recommandIDs.length = 0;
    recommandNames.length = 0;
    recommandTypes.length = 0;
    var elems = obj.parent().children('.operation_recommand_part').children('input');
    for(var i = 0; i<elems.length; i++){
        if( elems[i].checked ){
            recommandIDs.push($(elems[i]).parent().attr('part_id'));
            recommandNames.push($(elems[i]).parent().attr('part_name'));
            recommandTypes.push($(elems[i]).parent().attr('part_type'));
        }
    }
}
//设置操作区 接收组件
function setDroppable(elems){
    elems.droppable({        
        drop:function(){
            if(isOperationDrag==1){
                if(recommandIDs.length!=0){
                    var dropElement = $(this);
                    for(var i = 0; i<recommandIDs.length; i++){
                        part_id = recommandIDs[i];
                        part_name = recommandNames[i];
                        part_type = recommandTypes[i];
                        getInsert(dropElement);
                        dropElement.next('.btn-back').trigger("click");
                        dropElement = dropElement.parent().next('*').children('.receive_style');
                    }
                    dropElement.parent().remove();
                    isOperationDrag = 0;
                }
            }else{
                $('.operation_recommends_list').remove();
                getInsert( $(this) );
            }
            afterInsert();//进行操作后的推荐及保存
            setDashBoardFloat();
        },
        over:function(){
            $('#dashboard').droppable("disable");
        },
        out:function(){
            $('#dashboard').droppable("enable");
        },
        hoverClass:"receive_hover"
    });
}
//设置大区域的接收
function setDashboardDroppable(elems){
    elems.droppable({
        drop:function(){
            getInsert(leaveElement);//将没有放置在接收组件的原件放回原处
        },
        accept:".operation_part_style"
    });
}
//设置操作区 加号按钮的接收
/*function setAddDroppable(elems){
    elems.droppable({        
        drop:function(){
            //var element = $(this).parent();
             //$('.operation_recommends_list').remove();
             //判断是前按钮 还是后按钮
             
            if( $(this).is('.btn-front') ){
                     有问题
                $('.btn-front').trigger('click');
                getInsert( $( $('receive_style')[0] ) );
                
            }else{
                $('.btn-back').trigger('click');
                getInsert( $(this).parent().next('.part-cell').children('.receive_style') );
            }
            
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
}*/
//巩的方法
function saveChain(){
    //showMsg('Saving...');
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
//巩的方法
function getCurrChain(){
    var chain = "";
    $('.operation_part_style').each(function(index,elem){
        chain=chain+"_"+elem.getAttribute('part_id');
    });
    return chain;
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
        $('#part_info div.part_url a').html(result['part_url'])
        $('#part_info div.part_url a').attr('href' ,result['part_url'])
    }
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
function getOperationRecommend(){
    $.ajax({
        url:'/home/seqRecommend?part='+part_id,
        type:'GET',
        dateType:'JSON',
        success:function(result){
            if(result['isSuccessful']){
                $('#operation_recommand_container').empty();//将之前的推荐清除
                for(var i = 0; i<result['recommend_list'].length; i++){
                    result_list = result['recommend_list'][i];
                    var insertElems=$('#recommand_part_list').tmpl(result_list);
                    var row = $("<div class='row'></div>");
                    row.append(insertElems);
                    var line = $("<div class='line'></div>");
                    var list = $("<div class='operation_recommand_list'></div>");
                    list.append(row).append(line);
                    $('#operation_recommand_container').append(list);
                }  
                setOperationRecommandDraggable($('.operation_recommand_part'));
            }          
        }
    });
}
//在一个接收组件上插入操作的组件
function getInsert(obj){
    $('.recommand_div').remove();
    var html="<div part_id='"+part_id+"' part_name='"+part_name+"' part_type='"+
           part_type+"' class='show_message operation_part_style'><img src=\"/static/img/"+part_type+".png\" alt=\"logo\" class=\"img-rounded\"  /><span>"+part_name+"</span></div>";
    var operation_div=$(html);
    setOperationDraggable(operation_div);
    obj.append(operation_div);
    obj.droppable('disable');//将接收组件设置为不可用 
    obj.removeClass('receive_style_color'); //改变接受组件颜色 
}
function afterInsert(){
    getRecommend();//获取左侧推荐
    getOperationRecommend();//获取操作区推荐
    saveChain();//保存操作
}


