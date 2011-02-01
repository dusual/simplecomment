/*
 * Java Script/JQuery glue for server-side Python code and the comments/fixes
 * stuff which is being served along with the documentation.
 *
 * :copyright: Copyright 2007-2009 by the Sphinx team, see AUTHORS.
 * :license: BSD, see LICENSE for details.
 *
 * Below is a short description of the main functions used to make the tool
 * work. Internal functions are not listed here.
 *
 **  
 *** checking/downloading/printing/adding comments and fixes ****************
 **
 *
 * load_comments(id) -> check if database file with comments for paragraph 'id'
 *                      exists on the server; if yes, invoke comments_found()
 *                      function; if not, invoke no_comments() function.
 *
 * load_fixes(id) -> check if database file with fixes for paragraph 'id'
 *                   exists on the server; if yes, invoke fixes_found()
 *                   function; if not, invoke no_fixes() function.
 *
 * no_comments(id) -> insert a link ('No comments') to the post form after
 *                    the paragraph 'id'.
 *
 * no_fixes(id) -> insert a link ('No fixes') to the post form after the
 *                 'No comments' string.
 *
 * comments_found(id) -> download the comments database file for paragraph 'id'
 *                       and print it under the paragraph.
 *
 * fixes_found(id) -> download the fixes database file for paragraph 'id'
 *                    and print it under the paragraph.
 *
 * print_comments(id, data) -> print comments collected in an array 'data'
 *                             under the paragraph 'id'.
 *                             'data' is an array of objects; every object
 *                             has properties like 'name', 'score', 'comment'.
 *                             This function also prints a link at the end
 *                             of paragraph with a number of comments hidden
 *                             (i.e. "3 Comments").
 *
 * print_fixes(id, data) -> print fixes collected in an array 'data' under
 *                          the paragraph 'id'.
 *                          The description for print_comments() applies.
 *
 * add_new_comment(id) -> ajaxify a comment post form for paragraph 'id'
 *                        and reload comments (with load_comments() function).
 *                        This function also validates the form and resets
 *                        it on successful submit.
 *
 **
 *** displaying/hiding areas *************************************************
 **
 *
 * show_hide_comments(id) -> hide fixes area, show comments area and make sure
 *                           that the main comments/fixes area is shown
 *
 * show_hide_fixes(id) -> hide comments area, show fixes area and make sure
 *                        that the main comments/fixes area is shown
 *
 * show_hide_submitFixFields(id) -> show/hide additional fields in the post
 *                                  form for fixes view (when 'I would like
 *                                  to submit a patch' checkbox is 'true')
 *                                  and fill them with data if needed
 *
 *
 **
 *** rating comments/fixes ***************************************************
 **
 *
 * comments_up_down(id, comment_no, up_down, db)
 *                   -> send a GET request to the server with three parameters:
 *                       - id: paragraph id,
 *                       - comment_no: a number of a comment to score,
 *                       - up_down: two values possible: 'up' or 'down'
 *                                  depending on what kind of action should
 *                                  be taken ('up' means score+=1, and down
 *                                  means score-=1).
 *
 **
 *** sorting comments/fixes ************************************************ 
 **
 * 
 * sort_comments(id, by, db) -> sort comments for paragraph 'id' by 'by' argument
 *                          (two values for 'by' are possible at the moment:
 *                          'score' and 'date'). The sorting order changes
 *                          automatically from increasing to decreasing with
 *                          every sort.
 *
 *
 **
 *** threading ************************************************************
 **
 *
 * new_thread(id) -> make a particular comment a new thread before submitting
 *                   it
 *
 * reply_to(id, comment_no) -> make a comment a reply to comment 'comment_no'
 *
 **
 *** developer's actions ***************************************************
 **
 *
 * delete_comment(db, id, comment_no) -> delete entry from database 'db'
 *                                       located in 'id' file under
 *                                       'comment_no' index
 *
 * commit_fix(node, id, fix_no) -> commit a fix located in 'id' file under
 *                                 'fix_no' index to the repository
 *
 **
 *** general-use functions ************************************************
 **
 *
 * empty_comments(id) -> empty the comments area
 *
 * empty_fixes(id) -> empty the fixes area
 *
 * is_developer() -> returns true when developer rights should be granted
 *                   and false when the rights should not be granted.
 *                   At jQuery level it's only about displaying some
 *                   additional/developer-only-options. Real authorization
 *                   is going on on webapp (appserver.py) level.
 */

comments_path = "/comments/";
fixes_path = "/fixes/";
_db = undefined;

// *** checking/downloading/printing/adding comments ************************

function load_generic(what, id, error_func, success_func) {
   // if the div was filled with the comments before, empty it before appending
   if(_db == 'comments') {
      empty_comments(id);
   } else {
      empty_fixes(id);
   }

   // 'what' -> 'comments_path' or 'fixes_path' variables;
   var c_path = location.protocol + "//" + location.host + what + id;
   $.ajax({ url: c_path,
            type: 'HEAD',
            error: function() { error_func(id) },
            success: function() { success_func(id)}
         });
}

function load_comments(id) {
   return load_generic(comments_path, id, no_comments, comments_found)
}

function load_fixes(id) {
   return load_generic(fixes_path, id, no_fixes, fixes_found)
}

function get_load_cf(db) {
   if(db == 'comments' || db == comments_path) {
      return load_comments;
   }
   return load_fixes;
}

//////////////////////

function not_found_generic(what, id) {
   // 'what' -> 'comment' or 'fix' strings
   plural = what=='comment'?'comments':'fixes';
   $("a[name*=" + what + "_" + id + "]").replaceWith(
         '<a name="' + what + '_' + id + '" href="#' + id + '" '
          + 'onclick="show_hide_' + plural + '(\'' + id + '\')" '
          + 'id="' + id + '">No ' + plural + '</a>'
          + '<a name="' + id + '"></a>');
}

function no_comments(id) {
   not_found_generic('comment', id);
}

function no_fixes(id) {
   not_found_generic('fix', id);
}

//////////////////////////////

function found_generic(what, id, print_func) {
   var c_path = location.protocol + "//" + location.host + what + id + "?id=" + id;
   $.getJSON(c_path, function(data) {
      print_func(id, data);
   });
}

function comments_found(id) {
   found_generic(comments_path, id, print_comments);
}

function fixes_found(id) {
   found_generic(fixes_path, id, print_fixes);
}

///////////////////////////////

function print_generic(what, id, data) {
   var c_flag = (what == 'comments') ? true : false;
   var singular = (what == 'comments') ? 'comment' : 'fix';
   var isdev = is_developer();
   var node = $('div[class=submitFixFields_' + id + ']').attr('value');
   
   if(what == 'comments') {
      empty_comments(id);
   } else {
      empty_fixes(id);
   }

   // A 'factory' function which generates '+' and '-' buttons for every comment.
   //       'what'  is a kind of database (db for comments or for fixes)
   //         'id'  is a paragraph id.
   // 'comment_no'  is a place of a comment in the list of comments for given
   //               paragraph.
   //    'up_down'  is passed to POST method. It should be 'up' or 'down'.
   //       'sign'  is what's displayed on the button, by default it's '+' or '-'.
   function rate_comment_up_down_button(what, id, comment_no, up_down, sign) {
      return ' <a href="#' + id + '" onclick="comments_up_down(\'' + id + '\', \'' + comment_no + '\', \'' + up_down + '\', \'' + what + '\')"><b>' + sign + '</b></a> '
   }

   // in fixes view - show proposed diff
   function proposed_fix(c_flag, paragraph) {
      if(!c_flag) {
         return   '<tr>'
                +   '<td>'
                +     'Fix: ' + paragraph
                +   '</td>'
                + '</tr>'
                +  "<tr><td>&nbsp;</td></tr>"
      }
      return '';
   }

   // for every comment/fix generate a 'Reply' button
   function link_reply_to(id, comment_no) {
      return 'Comment no.: ' + data[i].comment_no
             + ' (<a href="#" onclick="reply_to(\'' + id + '\', \'' + comment_no + '\')">reply</a>).'
   }

   /* <developer's actions> */
   function delete_comment_button(db, id, comment_no) {
      return '<a href="#" onclick="delete_comment(\'' + db + '\', \'' + id +  '\', \'' + comment_no + '\')">delete</a>' 
   } 

   function commit_button(node, id, fix_no) {
      return '<a href="#" onclick="commit_fix(\'' + node + '\', \'' +  id + '\', \''
                  + fix_no + '\')">commit</a>'
   }

   function developers_actions(what, id, data, i) {
       return  '<tr>'
             +  '<td>'
             +    'Admin actions: '
             +    delete_comment_button(what, id, data[i].comment_no)
             +    ', '
             +    commit_button(node, id, data[i].comment_no)
             +    '.'
             +  '</td>'
             + '</tr>' 
   }
   /* </developer's actions> */

   // add the comments for paragraph
   for(i=0; i<data.length; i++) {
      // 'data[i]['date'] * 1000' to convert from milliseconds to seconds
      var commentDate = new Date(data[i]['date']*1000);

      $('div[class*=' + what + '_for_' + id + ']').append(
           "<table name='" + id + "' width='" + data[i].width + "%' align=center "
         +  "style='background-color: #f1ffc5; border: solid 1px lightblue;'>"
         +  "<tr>"
         +    "<td>"
         +     "Name: <a href='" + data[i].url + "'>" + data[i].name + "</a>. "
         +     "(" + get_date(commentDate) + ")"
         +    '</td>'
         +  '</tr>'
         +  '<tr>'
         +    '<td>'
         +     ' Score: <span class="score"><b>' + data[i].score + '</b></span>'
         +     rate_comment_up_down_button(what, id, data[i].comment_no, 'up', '+') 
         +     rate_comment_up_down_button(what, id, data[i].comment_no, 'down', '-')
         +     '. '
         +     link_reply_to(id, data[i].comment_no)
         +    '</td>'
         +  '</tr>'
         +  (isdev ? developers_actions(what, id, data, i) : '')
         +  '<tr><td>&nbsp;</td></tr>'
         +  proposed_fix(c_flag, data[i].paragraph_diff)
         +  "<tr>"
         +    "<td>"
         +      'Comment: ' + data[i].comment
         +    "</td>"
         +  "</tr>"
         + "</table><br>");
   }

   // add a button for showing/hiding the comments and post form
   $("a[name*=" + singular + "_" + id + "]").replaceWith(
                                   '<a name="' + singular + '_' + id
                                    + '" href="#' + id + '"' +
                                    'onclick="show_hide_' + what + '(\'' +
                                    id + '\')" '
                                    + 'id="' + id + '">'
                                    + data.length + ' ' + what + '</a>'
                                    + '<a name="' + id + '"></a>');

   if(what == 'comments') {
      hide_fixes(id);
      show_comments(id);
   } else {
      hide_comments(id);
      show_fixes(id);
   }
}


function print_comments(id, data) {
   print_generic('comments', id, data);
}

function print_fixes(id, data) {
   print_generic('fixes', id, data);
}

/////////////////////////////

function add_new_comment(id) {
   function validate(formData, jqForm, options) {
      var form = jqForm[0];
      if(!form.name.value) {
         alert("Please provide your name");
         return false;
      } else if(!form.comment.value) {
         alert("Please provide your comment");
         return false;
      } else if(form.submitFix.checked && !form.licence.checked) {
         alert("You have to agree to publish your fix on our licence!");
         return false;
      }

      if(form.submitFix.checked) {
         _db = 'fixes';
      } else {
         _db = 'comments';
      }
   }

   function form_reset() {
      $('#commentForm_' + id).resetForm()
      new_thread(id);
      if(_db == 'comments') {
         load_comments(id);
      } else {
         load_fixes(id);
      }
   }

   // bind 'commentForm' and provide a simple callback function 
   $('#commentForm_' + id).ajaxForm({
                                       beforeSubmit: validate,
                                       success: form_reset
                                    }); 
}

//////////////////////////////

function hide_main_div(id) {
   $('div.x' + id).css('display', 'none');  
}

function show_main_div(id) {
   $('div.x' + id).css('display', 'block');  
}

function hide_submitFixFields(id) {
   $('div.submitFixFields_' + id).css('display', 'none');
}

function show_submitFixFields(id) {
   node = $('div[class=submitFixFields_' + id + ']').attr('value');
   fill_paragraph_from_repo(node, id);
   $('input[name=submitFix]').attr('checked', true);
   $('div.submitFixFields_' + id).css('display', 'block'); 
   _db = 'fixes';

}

function hide_comments(id) {
   $('input[name=submitFix]').attr('checked', false);
   $('div.comments_for_' + id).css('display', 'none');
}

function hide_fixes(id) {
   $('div.fixes_for_' + id).css('display', 'none');
   hide_submitFixFields(id);
}

function show_comments(id) {
   $('input[name=submitFix]').attr('checked', false);
   $('div.comments_for_' + id).css('display', 'block');
   _db = 'comments';
}

function show_fixes(id) {
   $('div.fixes_for_' + id).css('display', 'block');
   show_submitFixFields(id);
}

function mainDivIsHidden(id) {
   return $('div.x' + id).is(':hidden');
}

function show_menu_hide(what, id) {
   function sort_comments_by_button(what, id, by) {
      return '<a href="#" onclick="sort_comments(\'' + id + '\', \'' + by + '\', \'' + what + '\')">' + by + '</a>'
   }

   sort_hide_menu = '<table style="background: #d9fff0; border: #008f57 1px solid;" width="100%"><tr><td>'
         + '<a name="hide_main_div_'
         + id
         + '" href="#" onclick="hide_main_div(\''
         + id
         +'\')">Hide</a>'
         + '</td><td>'
         +     ' Sort by: '
         +     sort_comments_by_button(what, id, 'date')
         +     ', '
         +     sort_comments_by_button(what, id, 'score')
         +     ', '
         +     sort_comments_by_button(what, id, 'thread')
         +   '.'
         + '</td></tr></table><br>'

   $('div[class=hide_menu_' + id + ']').replaceWith(sort_hide_menu);
}

function show_hide_comments(id) {
   show_menu_hide('comments', id);
   hide_fixes(id);
   show_comments(id);

   if(mainDivIsHidden(id)) {
      show_main_div(id);
   }
}

function show_hide_fixes(id) {
   show_menu_hide('fixes', id);
   hide_comments(id);
   show_fixes(id);

   if(mainDivIsHidden(id)) {
      show_main_div(id);
   }
}

function show_hide_submitFixFields(id) {
   // show or hide more form fields when 'i would like to submit a fix' is true
   var fixes_area_hidden =  $('div.submitFixFields_'+id).is(':hidden');
   if(fixes_area_hidden) {
      show_submitFixFields(id);
   } else {
      hide_submitFixFields(id);
   }
}

function fill_paragraph_from_repo(node, id) {
   var p_path = location.protocol + "//" + location.host
                + "/get_paragraph?node=" + node + "&id=" + id;
   $.getJSON(p_path, function(data) {
        $('textarea[name=paragraph_' + id + ']').replaceWith(
           '<textarea name="paragraph_' + id + '" rows=10 cols=70>' + data + '</textarea>');
        $('textarea[name=paragraph_orig_' + id + ']').replaceWith(
           '<textarea name="paragraph_orig_' + id + '" style="display: none;">' + data + '</textarea>');

   });
   
}

// *** rating comments ******************************************************

function comments_up_down(id, comment_no, up_down, db) {
   // request for a 'score' change
   load_func = get_load_cf(db);
   var rate_path = location.protocol + "//" + location.host + "/rate_comment";
   $.ajax({ url: rate_path,
            type: 'GET',
            data: "id=" + id + "&comment_no=" + comment_no + "&up_down=" + up_down + "&db=" + db,
            success: function() { load_func(id)}
         });
}

// *** developer actions ****************************************************

function delete_comment(db, id, comment_no) {
   load_func = get_load_cf(db);
   var rate_path = location.protocol + "//" + location.host + "/delete_comment";
   $.ajax({ url: rate_path,
            type: 'GET',
            data: "id=" + id + "&cno=" + comment_no + "&db=" + db,
            success: function() { load_func(id)}
         });
}

function commit_fix(node, id, fix_no) {
   var c_path = location.protocol + "//" + location.host + "/commit_fix";
   $.ajax({ url: c_path,
            type: 'GET',
            data: "node=" + node + "&id=" + id + "&fix_no=" + fix_no,
            success: function() { load_func(id)}
         });
}

// *** sorting comments *****************************************************

function sort_comments(id, by, db) {
   // request for a sort of comments, display json data structure ('data')
   var c_path = location.protocol + "//" + location.host
                + "/sort_comments?id=" + id + "&by=" + by + "&db=" + db;
   $.getJSON(c_path, function(data) {
         if(db=='comments') {
            print_comments(id, data);
         } else {
            print_fixes(id, data);
         }
   });
}

// *** general-use functions ***********************************************

function empty_comments(id) {
   $('div[class=comments_for_' + id + ']').replaceWith('<div class="comments_for_' + id + '" style=\"display: none;\"> </div>');
}

function empty_fixes(id) {
   $('div[class=fixes_for_' + id + ']').replaceWith('<div class="fixes_for_' + id + '" style=\"display: none;\"> </div>');
}

function is_developer() {
   var isdev_path = location.protocol + "//" + location.host + "/isdeveloper";
   http = new XMLHttpRequest();
   http.open('HEAD', isdev_path, false);
   http.send(null);
   return http.status!=404;
}

function get_date(d) {
   var month=["January", "February", "March", "April",
              "May", "June", "July", "August",
              "September", "October", "November", "December"];
   var t_date = d.getDate();      // Returns the day of the month
   var t_mon = d.getMonth();      // Returns the month as a digit
   var t_year = d.getFullYear();  // Returns 4 digit year
   var t_hour = d.getHours();     // Returns hours
   var t_min = d.getMinutes();    // Returns minutes
   var t_sec = d.getSeconds();    // Returns seocnds
   return t_hour + ':'
          + (t_min < 10 ? '0' : '') + t_min
          + ', ' + month[t_mon] + ' ' + t_date + ' ' + t_year
}

// *** threading **********************************************************

function reply_to(id, comment_no) {
   $('span[name=replyto_' + id + ']').replaceWith('<span name="replyto_' + id + '">' + comment_no + '</span>');
   $('textarea[name=replyto_' + id + ']').replaceWith('<textarea name="replyto_' + id + '" style="display: none;">' + comment_no + '</textarea>');
}

function new_thread(id) {
   $('span[name=replyto_' + id + ']').replaceWith('<span name="replyto_' + id + '">new thread</span>');
   $('textarea[name=replyto_' + id + ']').replaceWith('<textarea name="replyto_' + id + '" style="display: none;"></textarea>');
}

$(document).ready(function() {
   // load the comments for each paragraph when the DOM is ready
   $("span[name*=paragraph]").each(function() {
      var id = $(this).attr('value');
      load_comments(id);
      load_fixes(id);
   });
});
