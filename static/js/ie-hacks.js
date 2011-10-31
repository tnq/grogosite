/* Some little extras (using jquery) */
$(function(){
   $("#content").addClass('rar');
   $("#content ol li").filter(":last").addClass('last');
   $("#content.support p").filter(":last").addClass('last');
   $("#content.hire .imagerow img:last-child").addClass('last');
   console.log("Classes applied");
});