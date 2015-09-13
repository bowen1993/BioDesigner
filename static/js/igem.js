var part_id='0000';
var part_name='1111';
var part_type='2222';
var drop_index=1;
$(document).ready(function(){
		setFrame();
        //为本地的接收组件设置为可接受
        setDroppable($('.receive_style'));
        setAddDroppable($('.add_style'));
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
            }
        },'.show_message');

        //为右侧按钮加事件
        $(document).on({
            click:function(){
                var add_button=$("<div class='add_style ' ></div>");
                var receive_div=$("<div class='receive_style ' ></div>");
                setAddDroppable(add_button);
                setDroppable(receive_div);
                $(this).after(receive_div.add(add_button));
                setFrame();
                setDragDrop();
            }
        },'.add_style');
});

window.onresize=function(){
	setFrame();
}	
function setFrame(){

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
    $('#total_container').css("height",total_height);//设置 #total_container 高度为屏幕高度
    var left_container_width=$('#left_container').width();//获取 #left_container 的宽度
    //计算#right_container宽度为屏幕宽度减去#left_container宽度
    var right_container_width=total_width-left_container_width;
    //设置#right_container 宽度和margin
    $('#right_container').css("margin-left",left_container_width).css("width",right_container_width);
    var logo_width=$('#logo').width();// 获取#logo宽度
    var logo_height=logo_width/3;//计算#logo高度
    $('#logo').css("height",logo_height);//设置#logo 高度
    var tab_container_height=(total_height-logo_height)*0.6;//计算 #tab_container 高度
    $('#tab_container').css("height",tab_container_height);//设置  #tab_container 高度
    var recommand_container_height=total_height-logo_height-tab_container_height;//计算#recommand_container 高度
    $('#recommand_container').css("height",recommand_container_height);//设置 #recommand_container 高度
    $('#tab_container').tabs();//将#tab_container设置为标签组件
    var tab_ul_height=$('#tab_ul').height();//获取 标签组件 标签的高度
    var search_part_container_height=tab_container_height-tab_ul_height-2; //计算 标签组件 内容区域高度
    $('#search_part_container').css("height",search_part_container_height);
    var search_container_height=$('.search_container').height();//获取搜索区域高度
    var result_container_height=search_part_container_height-search_container_height;// 计算搜索结果区域高度
    $('.result_container').css("height",result_container_height);
    var recommand_title_height=$('h1').height();//获取 组件推荐标题 的高与宽
    var recommand_title_width=$('h1').width();
    var recommand_search_container_height=recommand_container_height-recommand_title_height;//计算 组件推荐区域高度
    $('#recommand_search_container').css("height",recommand_search_container_height).css("width",recommand_title_width);
    //右侧区域
    var bananer_height=$('#bananer').height();
    var operation_height=total_height-bananer_height;
    $('#operation').css("height",operation_height);

    var margin_size=right_container_width/37;//margin 是操作区的1/3
    var margin_height=operation_height/21;
    $('.add_style').css("height",4*margin_height).css("width",margin_size)
       .css("margin-top",margin_height).css("margin-left",margin_size);
    $('.receive_style').css("height",4*margin_height).css("width",6*margin_size)
      .css("margin-top",margin_height).css("margin-left",margin_size);
    //$('.operation_part_style').css("height",4*margin_height*0.8).css("width",6*margin_size*0.8);
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
            part_id=this.getAttribute('part_id');
            part_name=this.getAttribute('part_name');
            part_type=this.getAttribute('part_type');            
            var par=$(this).parent();
            setDroppable(par);
            $(this).remove();
        }
    });
}
function setDroppable(elems){
    elems.droppable({        
        drop:function(){
            drop_index=$(this).prevAll('*').length;
            getInsert();
        },
        hoverClass:"receive_hover"
    });
}
function setAddDroppable(elems){
    elems.droppable({        
        drop:function(){
            drop_index=$(this).prevAll('*').length;
            getAdd();
        },
        hoverClass:"receive_hover"
    });
}
//获取左侧推荐的组件
function getRecommend(){
    var message;
    $('.operation_part_style').each(function(index,elem){
        message=message+"_"+elem.getAttribute('part_id');
    });
    $.ajax({
        url:'/home/arecommend?seq='+message,
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
            result_list = result['recommend_list'];
            var insertElems=$('#recommand_part_list').tmpl(result_list);
            setDraggable(insertElems);
            var recommand_div=$("<div class='recommand_div'> </div>");
            recommand_div.append(insertElems);
            var s= $('#operation').children().filter('*').eq(here);
            s.css("position","relative").append(recommand_div);
            setFrame();
                   
        }
    });
   
}
function getInsert(){
    $('.recommand_div').remove();
    $('#operation').children().filter('*').eq(drop_index).remove();
    var html="<div part_id='"+part_id+"' part_name='"+part_name+"' part_type='"+
           part_type+"' class='show_message operation_part_style'>"+part_name+"</div>";
    var operation_div=$(html);
    setOperationDraggable(operation_div);
    html="<div class='receive_style'></div>";
    var receive_div=$(html).prepend(operation_div);
    $('#operation').children().filter('*').eq(drop_index-1).after(receive_div);   
    getRecommend();
    getOperationRecommend(drop_index);
    setFrame();
}
function getAdd(){
    $('.recommand_div').remove();
    var html="<div part_id='"+part_id+"' part_name='"+part_name+"' part_type='"+
           part_type+"' class='show_message operation_part_style'>"+part_name+"</div>";
    var operation_div=$(html);
    setOperationDraggable(operation_div);
    html="<div class='receive_style'></div>";
    var receive_div=$(html).prepend(operation_div);
    html="<div class='add_style'></div>";
    var add_div=$(html);
    setAddDroppable(add_div);
    var t=receive_div.add(add_div);
    $('#operation').children().filter('*').eq(drop_index).after(t);
    getRecommend();
    getOperationRecommend(drop_index+1);
    setFrame();
}

