jQuery(document).ready(function(t){function e(){var e=t(this).attr("data-desc");null==t(this).attr("data-desc")&&(e="family"),t.ajax({type:"GET",url:"/halls/sessionschange/",data:{view:e},dataType:"json",cache:!1,success:function(e){"ok"==e.response&&(t("#session").html(e.html),t("#title").html(e.title),t("#desc").html(e.desc))}})}e(),t(".view").click(e)});