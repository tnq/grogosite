$(document).ready(function() {
    $("#add_button").click(function() {
        num_lines = $("[name=form-TOTAL_FORMS]").val();
        $("[name=form-TOTAL_FORMS]").val(parseInt(num_lines)+1);
        
        html = $("#form_template").clone().html().replace(/__prefix__/g, num_lines);
        $("#forms").append(html);
    });

    $("#remove_button").click(function() {
        num_lines = $("[name=form-TOTAL_FORMS]").val();
        if (num_lines > 0) {
            num_lines = parseInt(num_lines)-1;
            $("[name=form-TOTAL_FORMS]").val(num_lines);
            $("#booksection"+num_lines).remove();
        }
    });
    $("#show_button").click(function() {
        data = $("#order_form").serialize(true);
        Dajaxice.scripts.purchase.update_purchase('Dajax.process', {'form':data});
    });
});
