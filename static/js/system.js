window.onresize=function(){
	setFrame();
};
$(document).ready(function(){
    setFrame();
});
function setFrame(){
   var total_height = document.documentElement.clientHeight; 
   $('#container').css('height',total_height); 
   $('#sidebar').css('height',total_height); 
   $('#main').css('height',total_height); 
   var logo_height = $('#logo').height();     // get #logo height
   var search_container_height = total_height-logo_height;  // figure #search-container height
   $('#search-container').css('height',search_container_height); //set #search-container height
   var search_container_h1_height = $('#search-container h1').height(); // get #search-container h1 height
   var search_area_height = $('#search-container #search-area').height(); // get #search-container #search-area height
   var search_result_height = search_container_height-search_container_h1_height-search_area_height; //figure #search-result height
   $('#search-result').css('height',search_result_height); //set #search-result height 
   
   // var total_width = document.documentElement.clientWidth;  // get total width
   // var total_height = document.documentElement.clientHeight;  // get total height
   // $('#container').css('height',total_height);   // set #container height
   // var logo_height = $('#logo').height();     // get #logo height
   // var search_container_height = total_height-logo_height;  // figure #search-container height
   // $('#search-container').css('height',search_container_height); //set #search-container height
   // var search_container_h1_height = $('#search-container h1').height(); // get #search-container h1 height
   // var search_area_height = $('#search-container #search-area').height(); // get #search-container #search-area height
   // var search_result_height = search_container_height-search_container_h1_height-search_area_height; //figure #search-result height
   // $('#search-result').css('height',search_result_height); //set #search-result height 

   // var sidebar_width = $('#sidebar').width();    // get #sidebar width
   // var main_width = total_width-sidebar_width;   // figure #main width
   // $('#main').css('width',main_width);  //set #main width
   // var main_ul_buttonArea_width = $('#button-area').width(); //get ul button-area width
   // var main_ul_labelArea_width = main_width-main_ul_buttonArea_width;
   // $('#label-area').css('width',main_ul_labelArea_width);
   // var menu_height = $('#menu').height();
   // var my_svg_height = total_height-menu_height; // figure #my-svg height
   // $('#my-svg').css('height',my_svg_height);  // set #my-svg height
}
$(document).on({
   click:function(){
      var input = $('#search-area input').val();  // get input value 
      getSearchResult(input);
      //var insert = [{"compound_id": "C00001", "name": "H2O"}, {"compound_id": "C00137", "name": "myo-Inositol"}, {"compound_id": "C00288", "name": "HCO3-"}, {"compound_id": "C00619", "name": "3-Oxo-delta4-steroid"}, {"compound_id": "C01243", "name": "1D-myo-Inositol1,3,4-trisphosphate"}, {"compound_id": "C01245", "name": "D-myo-Inositol1,4,5-trisphosphate"}, {"compound_id": "C02941", "name": "3-Oxo-delta1-steroid"}, {"compound_id": "C04226", "name": "6-Oxo-1,4,5,6-tetrahydronicotinate"}, {"compound_id": "C02797", "name": "3-Oxo-5beta-steroid"}, {"compound_id": "C02940", "name": "3-Oxo-5alpha-steroid"}];
      //insertSearchResult(insert);
   }
},'#search-area span#search');


function getSearchResult(input){
   $.ajax({
      url:'/system/searchCompound?keyword=' + input,
      type:'GET',
      success:function(result){
          insertSearchResult(result);
      }
   });
}
function insertSearchResult(result){
   $('#search-result').empty();
   for(var i = 0; i<result.length; i++){
       var item = getInsertLabel(result[i]['compound_id'], result[i]['name']);
       $('#search-result').append(item);
   }
}
function getInsertLabel(compound_id, compound_name){
   if(compound_name.length>13){
      var name = compound_name.substr(0,11)+'...';
   }else{
      var name = compound_name;
   }
   var html = "<li class=\"search-result-item\">"+
                  "<span  compound-name=\""+compound_name+"\" compound-id=\""+compound_id+"\">"+name+"</span>"+
                  "<button class=\"add-label btn\">add</button></li>";
   return $(html);
}
$(document).on({
   click:function(){
       var element = $(this).prev('span');
       var compound_id = element.attr('compound-id');
       var name = element.attr('compound-name');
       var id_array = getArray();
       var count = 0;
       for(var i = 0; i<id_array.length; i++){
          if(compound_id!=id_array[i]){
            count++;
          }
       }
       if(count==id_array.length){
         addLabel(compound_id, name);
       }
       
   }
},'.add-label');
function addLabel(compound_id, name){
   var html = "<li><span class=\"label\" compound-name=\""+name+"\" compound-id=\""+compound_id+"\">"+name+"</span>"+
                   "<span class=\" remove glyphicon glyphicon-remove\"></span></li>";
   var label = $(html);
   $('#label-area').append(label);
}
$(document).on({
    click:function(){
      $(this).parent().remove();
    }
},'.remove');
$(document).on({
   click:function(){
      $('#label-area').empty();
   }
},'#remove-labels');
$(document).on({
   click:function(){
      $('.label-click').removeClass('label-click');
      $(this).addClass('label-click');
      var compound_id = $(this).children('span')[0].getAttribute('compound-id');
      //var compound_name = $(this).children('span')[0].getAttribute('compound-name');
      getCompoundMessage(compound_id);
   }
},'ul#search-result li.search-result-item,#menu ul#label-area li');
function getCompoundMessage(compound_id){
   $.ajax({
      url:'/system/getCompound?id=' + compound_id,
      type:'GET',
      success:function(result){
          if(result['isSuccessful']){
            showCompoundMessage(result['info']);
          }else{

          }
      }
   });  
}

function getGeneMessage(gene_id){
  $.ajax({
      url:'/system/getGene?id=' + gene_id,
      type:'GET',
      success:function(result){
          if(result['isSuccessful']){
            showGeneMessage(result['info']);
          }else{

          }
      }
   });
}

function showGeneMessage(info){
 $('#gene-message span#gene-id').text(info['gene_id']);
 $('#gene-message span#name').text(info['name']);
 $('#gene-message span#definition').text(info['definition']);
 $('#gene-message span#organism-short').text(info['organism_short']);
 $('#gene-message span#organism').text(info['organism']);
 $('#gene-message').removeClass('hide');
}

function showCompoundMessage(info){
   $('#message span#compound-id').text(info['compound_id']);
   $('#message span#name').text(info['name']);
   $('#message span#nicknames').text(info['nicknames']);
   $('#message span#mol-weight').text(info['mol_weight']);
   $('#message span#exact-mass').text(info['exact_mass']);;
   $('#message span#formula').text(info['formula']);
   $('div#message').removeClass('hide');
}

$(document).on({
   click:function(){
      $('div#gene-message').addClass('hide');
   }
},'#close-gene-message');

$(document).on({
   click:function(){
      $('div#message').addClass('hide');
   }
},'#close-message');
$(document).on({
    click:function(){
      var id_array = getArray(),
      postData = {
        'id' : getIdStr(id_array),
      };
      $.ajax({
        url: '/system/related',
        type: 'POST',
        data: postData,
        dataType: 'JSON',
        success:function(result){
          console.log(result);
          draw(result);

        }
      });
    }
},'button#run');
function getArray(){
   var id_array = new Array();
   var elements = $('#menu #label-area li');
   for(var i = 0; i<elements.length; i++){
      id_array[i] = $(elements[i]).children('span')[0].getAttribute('compound-id');
   }
   return id_array;
}

function getIdStr(id_array){
  var result = '';
  for (var i =0; i < id_array.length; i++){
    result += id_array[i] + '_';
  }
  return result;
}
$(document).on({
    mouseover:function(){
      $(this).children('button').toggleClass('show');
    },
    mouseout:function(){
      $(this).children('button').toggleClass('show');
    }
},'li.search-result-item');

