function qid(id) {
  return id.replace(/([.:])/g, "\\$1");
}

function beforeComment(formData, jqForm, options) {
  var form=jqForm[0];

  if (form.comment.textLength.toString()=='0') {
    $("span.comment_error").empty().append(
      "<span class=\"comment_error\">  Your comment is empty</span>");
    return false;
  }
  if (form.name.textLength.toString()=='0') {
    $("span.comment_error").empty().append(
      "<span class=\"comment_error\">   Please provide a name</span>");
    return false;
  }
  $(options.target + " span.comment_error").empty().after(
    "<img src=\"/support/icons/throbber.gif\" style=\"vertical-align: middle\"/>");
  $("input[@name=submit]").attr("disabled", true);
}

function ajaxifyForm(id) {

// $(' #form_basic_python_func_2').replaceWith('something');
 
   var substring=id.substr(9);

   $('#form_'+substring).ajaxForm({beforeSubmit: beforeComment,
  			      success: function(){ loadComments(id);}

  			     });}


function toggleComment(id) {
  $("#toggle_" + qid(id)).nextAll().toggle();
  return false;
}


function loadComments(id)
{

  var substring=id.substr(9);

  //  $('#comments_'+substring).replaceWith(location.protocol+ "//" + location.host + "/single/"+ substring +'/')


      $('#comments_'+substring).load(location.protocol+ "//" + location.host + "/single/"+ substring +'/',function() { ajaxifyForm(id);}
  				);

}




function loadAllComments() {
  $("a.commenttoggle").each(function() {
    var id = $(this).attr("pid");
    if (id) {
      loadComments(id);
    }
  });
}



$(document).ready(function() {
 var url_string=window.location.pathname;
 var temp = new Array();
 temp = url_string.split('/pages/');
 var chap_name=temp[1].split('.')[0];


  function loading(id) {
    return " <span id=\"comments_" + id + "\" class=\"comment\">" +
	"<span pid=\"" + id + "\" class=\"commenttoggle\"><p>" + "loading..." +
      "</span>";
  }

$("p[@id]").each(function() {
    $(this).append(loading($(this).attr("id")));

	});


 var url_string=window.location.pathname;
 var temp = new Array();
 temp = url_string.split('/pages/');
 var chap_name=temp[1].split('.')[0];

 jQuery.getJSON(location.protocol+"//" + location.host +  "/count/" + chap_name, function(data) {

 		 $("span.comment").each(function(data_val) {
 		 var id = $(this).attr("id");
 		var substring=id.substr(9);

 					  if (data.count[substring]){


		$(this).replaceWith("<span class='comment'" +  ' id='+ id+ " <a   +  href=javascript:loadComments('"+id+"');>" + data.count[substring] +' comments'+ "</a>");
					    }

					else {$(this).replaceWith("<span class='comment'" +  ' id='+ id+ " <a   +  href=javascript:loadComments('"+id+"');>" + 'No comments'+ "</a>");
}


					});


 	       });

 		  });













