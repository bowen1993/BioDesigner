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
		var liElem = $('#reaction-input-row').tmpl({});
		ulElem.append( liElem );
	}
},'button.new-input-row');
$(document).on({
	click:function(){
		var ulElem = $(this).prev('ul.input-table');
		var liElem = $('#parent-input-row').tmpl({});
		ulElem.append( liElem );
	}
},'button.new-parent-input-row');
$(document).on({
	click:function(){
		var insertElems=$('#reaction-equation-area').tmpl({});
		insertElems.insertBefore( $(this) );
	}
},'button#add');
$(document).on({
	click:function(){
		if( $('div.reaction-equation-area').length != 1 ){
			$(this).parent().remove();
		}
	}
},'div.reaction-equation-area button.remove-reaction-equation');
$(document).on({
	click:function(){
		window.location = '/home/project';
	}
},'div#sidebar span#back');
$(document).on({
	click:function(){
		$('button.remove-reaction-equation').trigger('click');
		$('span.remove-input-row').trigger('click');
		$('input').val('');
	}
},'div#sidebar span#reset');

function get_materials(){
	var material_inputs = $('#parent-material-area ul').find('li.input-row');
	var result_list = [];
	for(var i = 0; i < material_inputs.length; i++){
		var name = $(material_inputs[i]).find('input.material').val();
		var amount = $(material_inputs[i]).find('input.amount').val();
		result_list.push([name, amount]);
	}
	return result_list
}

function get_reactants(reactant_area){
	var reactant_inputs = $(reactant_area).find('input.material');
	result_list = [];
	for (var i = 0; i < reactant_inputs.length; i++){
		result_list.push($(reactant_inputs).val());
	}
	return result_list;
}

function get_products(reactant_area){
	var reactant_inputs = $(reactant_area).find('input.material');
	result_list = [];
	for (var i = 0; i < reactant_inputs.length; i++){
		result_list.push($(reactant_inputs).val());
	}
	return result_list;
}

function get_reactions(){
	var reaction_inputs = $('div.reaction-equation-area'),
	result_list = [];
	for (var i = 0; i < reaction_inputs.length; i++){
		var reactant_list = get_reactants($(reaction_inputs[i]).find('ul.reactant')),
		product_list = get_products($(reaction_inputs[i]).find('ul.resultant')),
		rate = $(reaction_inputs[i]).find('input#rate').val();
		result_list.push({
			'reactants' : reactant_list,
			'products' : product_list,
			'k': rate
		});
	}
	return result_list;
}

$(document).on({
	click:function(){
		var matetial_list = get_materials(),
		reaction_list = get_reactions();
		postData = {
			"reactions" : reaction_list,
			'martials' : matetial_list,
			'reaction_time' : 100
		}

		$.ajax({
			url:'/home/simulate',
			type:'POST',
			contentType: 'application/json; charset=utf-8',
			processData: false,
			data:JSON.stringify(postData),
			dataType:'JSON',
			success:function(result){
				drawResult(result);
			}
		});
	}
},'button#run');
function getElement(tag,inner){
    var element = document.createElement(tag); // create a element 
    element.innerHTML = inner;   // set element's inner html
    for(var i = 2; i<arguments.length-1; i=i+2){
        element.setAttribute(arguments[i], arguments[i+1]);
    }
    return element;
}


function drawResult(result){
'use strict';
  var list = new Array();
  var path = new Array();
  var svg;
  var circle = new Array();
  var tips;
  var ddata;
  var tag1;
  var tag2;
  var type;
  var typedate = new Array();
  var xAxis;
  var yAxis;
  var x;
  var y;
  var c;
  var colors = new Array('Blue', 'BlueViolet', 'DeepSkyBlue', 'ForestGreen');
  var data = result;
  ddata = data.concat();
  // 定义circle的半径
  var r0 = 3,
    r1 = 5;
  // 定义动画持续时间
  var duration = 500;

  var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = document.body.clientWidth - margin.left - margin.right-120-250,
    height = 500 - margin.top - margin.bottom -20;

  d3.select('.canvs').remove();
  d3.select('.list').remove();
  d3.select('div#header button').remove();
  var container = d3.select('div#content')
    .append('svg')
    .attr('class', 'canvs')
    .attr('width', width + margin.left + margin.right+120)
    .attr('height', height + margin.top + margin.bottom+20);

  typedate = new Array();
  var ts = d3.max(data, function(d) { return d.order; });
  for(var i = 0; i <= ts; i++){
    typedate[i] = new Array();
    list.push(1);
  }

  svg = container.append('g')
    .attr('class', 'content')
    .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')'); 

  data.forEach(function(d) {
        d.dayText = d.date;
        d.pv = d.pv;
        typedate[d.order].push(d);
      });

  var div = d3.select('div#header').append('div').attr('class', 'list');
  for (var i = 0; i < typedate.length; i++){
    d3.select('.list')
    .append('input')
    .attr('class', 'ckbox')
    .attr('type', 'checkbox')
    .attr('value', i)
    .attr('name', 'ck')
    .attr('checked', 'checked');

    d3.select('.list')
    .append('font')
    .attr('class', 'ftext')
    .attr('color', colors[i])
    .text(typedate[i][0].name);

    
  }

  show();
  function show() { 
    list = new Array();
    ddata.forEach(function(d){
      list[d.order] = 1;
    });
    function draw() {
      d3.select('.content').remove();
      svg = container.append('g')
                    .attr('class', 'content')
                    .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');
      x = d3.scale.linear().range([0, width]);  
      y = d3.scale.linear().range([height, 0]);
    
      xAxis = d3.svg.axis()
        .scale(x)
        .orient('bottom')
        .ticks(30);
    
      yAxis = d3.svg.axis()
        .scale(y)
        .orient('left')
        .ticks(10);
 
      //x.domain(d3.extent(ddata, function(d) { return d.date;}));
      x.domain([d3.min(ddata, function(d) { return d.date; }),
                d3.max(ddata, function(d) { return d.date; })]);
      y.domain([d3.min(ddata, function(d) { return d.pv; }),
                d3.max(ddata, function(d) { return d.pv; })]);

      svg.append('text')
        .attr('class', 'title')
        .text('Simulation Result')
        .attr('x', width/2)
        .attr('y', 0);

      svg.append('g')
        .attr('class', 'x axis')
        .attr('transform', 'translate(0,' + height + ')')
        .call(xAxis)
        .append('text')
        .text('seconds')
        .attr('transform', 'translate(' + (width - 20) + ', 0)');

      svg.append('g')
        .attr('class', 'y axis')
        .call(yAxis)
        .append('text')
        .text('Concentration');
      
      var line = d3.svg.line()
                  .x(function(d) { return x(d.date); })
                  .y(function(d) { return y(d.pv); })
                  .interpolate('monotone');
      
      var ps = -1;
      var tag = false;

      typedate = new Array();
      var ts = d3.max(data, function(d) { return d.order; });
      for(var i = 0; i <= ts; i++){
        typedate[i] = new Array();
        list.push(1);
      }
    
      ddata.forEach(function(d) {
            d.dayText = d.date;
            d.pv = d.pv;
            typedate[d.order].push(d);
          });

      for (var i=0; i< typedate.length;i++){  
          if (list[i]==0) {
            continue;
          }
          ps++;
          path[ps] = svg.append('path')
            .attr('class', 'line')
            .attr('stroke', colors[ps])
            .attr('fill', 'none')
            .attr('stroke-width', '2px')
            .attr('d', line(typedate[i]));
      }

      var cs = -1;
      for (var i=0; i< typedate.length;i++){
        if (list[i]==0){
          continue;
        }
        cs++;
        circle[cs] = new Array();
        circle[cs] = svg.selectAll('cirlce')   
                      .data(typedate[i])
                      .enter()
                      .append('g')
                      .append('circle')
                      .attr('class', 'linecircle')
                      .attr('cx', line.x())
                      .attr('cy', line.y())
                      .attr('r', r0)
                      .attr('fill', 'green')
                      .attr('order', function(d){return d.order;})
                      .attr('date', function(d){return d.date;})
                      .attr('py', function(d){return d.py;})
                      .attr('clock', false)
                      .on('mouseover', function() {
                        c = d3.select(this).attr('fill');
                        if (d3.select(this).attr('clock') == 'true'){
                          c = '#FF0000';
                        }
                        d3.select(this).transition().duration(duration).attr('r', r1*2)
                        .attr('fill', 'steelblue');
                      })
                      .on('mouseout', function() {
                      	if (d3.select(this).attr('clock') == 'false'){
                        	d3.select(this).transition().duration(duration).attr('r', r0);
                        	d3.select(this).attr('fill', c);
                    	}
                      })
                      .on('click', function(d, i) {
                        if (tag==true && d.order == type && tag1 != d.date){
                          d3.select(this).attr('fill', '#FF0000');
                          tag = false;
                          for(var i = 0; i < list.length; i++){
                            if (i != type) list[i] = 0;
                          }
                          
                          tag2 = d.date;
                          if (tag2 < tag1){
                            var temp = tag2;
                            tag2 = tag1;
                            tag1 = temp;
                          }
                          ddata = new Array();
                          data.forEach(function(d){
                            if (d.order == type && d.date >= tag1 && d.date <= tag2){
                              ddata.push(d);
                            }
                          });

                          for (var i = 0; i < path.length; i++){
                            path[i].remove();  
                          }
                          for (var i = 0; i < circle.length; i++){
                            circle[i].remove();
                          }
                          show();
                        }     
                        if (tag == false){
                          d3.select(this).attr('fill', '#FF0000');
                          d3.select(this).attr('clock', true);
                          tag = true;
                          type = d3.select(this).attr('order');
                          tag1 = d3.select(this).attr('date');
                        }
                      });

      }
      var tips = svg.append('g').attr('class', 'tips');

      tips.append('rect')
        .attr('class', 'tips-border')
        .attr('width', 200)
        .attr('height', 50)
        .attr('rx', 10)
        .attr('ry', 10);

      var wording1 = tips.append('text')
        .attr('class', 'tips-text')
        .attr('x', 10)
        .attr('y', 20)
        .text('');

      var wording2 = tips.append('text')
        .attr('class', 'tips-text')
        .attr('x', 10)
        .attr('y', 40)
        .text('');

      container
        .on('mousemove', function() {
          var m = d3.mouse(this),
            cx = m[0] - margin.left,
            cy = m[1] - margin.top;
          
          showWording(cx,cy);

          d3.select('.tips').style('display', 'block');
        })
        .on('mouseout', function() {
          d3.select('.tips').style('display', 'none');
        });



      function showWording(cx,cy) {
        var min;
        var d;
        var xlen = d3.extent(ddata, function(d) { return d.date;});
        var ylen = d3.extent(ddata, function(d) { return d.pv;});
        for (var i = 0; i < ddata.length; i++){

          var xp = width / (xlen[1]-xlen[0]) * (ddata[i].date-xlen[0])-cx;
          var yp = height / (ylen[1]-ylen[0]) * (ylen[1] - ddata[i].pv)-cy;
          if (xp < 0) xp = -xp;
          if (yp < 0) yp = -yp;
          
          if (i == 0){
            d = ddata[i];
            min = xp + yp;
          }else{
            if (xp + yp < min){
              min = xp+yp;
              d = ddata[i];
            }
          }
        }
        

        function formatWording(d) {
          return 'seconds：' + (d.date) + 's';
        }
        wording1.text(formatWording(d));
        wording2.text('Concentration：' + d.pv);

        var x1 = x(d.date),
          y1 = y(d.pv);


        // 处理超出边界的情况
        var dx = x1 > width ? x1 - width + 2 : x1 + 2 > width ? 2 : 0;

        var dy = y1 > height ? y1 - height + 2 : y1 + 2 > height ? 2 : 0;
        
        x1 -= dx;
        y1 -= dy;

        d3.select('.tips')
          .attr('transform', 'translate(' + x1 + ',' + y1 + ')');
      }
    }
    draw();
  }
  d3.select("div#header")
  .append("button")
  .text("Show all")
  .on('click', function(){
    for(var i = 0; i < typedate.length; i++)
      list[i] = 1;
    ddata = new Array();
    data.forEach(function(d){
      ddata.push(d);
    });
    for (var i = 0; i < path.length; i++){
      path[i].remove();  
    }
    for (var i = 0; i < circle.length; i++){
      circle[i].remove();
    }
    show();
  });

  function doit(){
    var sum = 0;
    var a = document.getElementsByName("ck");
    ddata = new Array();

    for(var i=0;i<a.length;i++){
        if(!a[i].checked){
          list[i]= 0;
        }else{
          list[i] = 1;
          data.forEach(function(d){
            if (d.order == i){
              ddata.push(d);
            }
          });
        }
    }
    for (var i = 0; i < path.length; i++){
      path[i].remove();
    }
    for (var i = 0; i < circle.length; i++){
      circle[i].remove();
    }
    path = new Array();
    circle = new Array();
    show(); 
  }

  $(document).on({
  	click:function(){
  		doit();
  	}
  }, '.ckbox');

  window.onload = function(){
    var a = document.getElementsByName("ck");
    for(var i=0;i<a.length;i++){
        a[i].onclick = doit;   
    }
  }
}


