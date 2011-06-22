$(document).ready(function() {
    // Add one to the total forms for the current year
    num_lines = $("[name=form-TOTAL_FORMS]").val();
    $("[name=form-TOTAL_FORMS]").val(parseInt(num_lines)+1);

    $("#add_button").click(function() {
        num_lines = $("[name=form-TOTAL_FORMS]").val();
        $("[name=form-TOTAL_FORMS]").val(parseInt(num_lines)+1);
        
        html = $("#form_template").clone().html().replace(/__prefix__/g, num_lines);
        $("#forms").append(html);
    });

    $("#remove_button").click(function() {
        num_lines = $("[name=form-TOTAL_FORMS]").val();
        if (num_lines > 1) { //Always leave one form for the current year
            num_lines = parseInt(num_lines)-1;
            $("[name=form-TOTAL_FORMS]").val(num_lines);
            $("#booksection"+num_lines).remove();
        }
        validate();
    });

    $("#clear_button").click(function() {
        $("input:radio").removeAttr("checked");
        validate();
    });

    $("#order_form input, #order_form").change(function() {
        validate();
    });

    function validate(){
        data = $("#order_form").serialize(true);
        Dajaxice.scripts.purchase.update_purchase('Dajax.process', {'form':data});
    }

});
