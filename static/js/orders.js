$(document).ready(function() {
    // Add one to the total forms for the current year
    num_lines = $("[name=form-TOTAL_FORMS]").val();
    $("[name=form-TOTAL_FORMS]").val(parseInt(num_lines)+1);

    //Disable shipping address by default
    $("#address :input").attr("disabled", true);

    //Remove "0" as an option for older books
    $("#id_form-__prefix__-numbers option[value='0']").remove();

    //Remove the current year's book from the old books
    $("#id_form-__prefix__-years option[value='2012']").remove();

    //When the add button is clicked, copy the hidden div
    //to allow another old book to be ordered
    $("#add_button").click(function() {
        num_lines = $("[name=form-TOTAL_FORMS]").val();
        $("[name=form-TOTAL_FORMS]").val(parseInt(num_lines)+1);
        
        html = $("#form_template").clone().html().replace(/__prefix__/g, num_lines);
        $("#forms").append(html);
    });

    //When the remove button is clicked, remove the last book added
    // (down to the current year's book) and re-validate
    $("#remove_button").click(function() {
        num_lines = $("[name=form-TOTAL_FORMS]").val();
        if (num_lines > 1) { //Always leave one form for the current year
            num_lines = parseInt(num_lines)-1;
            $("[name=form-TOTAL_FORMS]").val(num_lines);
            $("#booksection"+num_lines).remove();
        }
        validate();
    });

    //Clear the patron choice and re-validate
    $("#clear_button").click(function() {
        $("input:radio").removeAttr("checked");
        validate();
    });

    //Validate on any order change
    $("#order_form input, #order_form").change(function() {
        validate();
    });

    //Disable the address fields if shipping is not chosen
    $("#id_shipping").change(function() {
        if ($("#id_shipping").is(":checked")) {
            $("#address :input").removeAttr("disabled");
        } else {
            $("#address :input").attr("disabled", true);
        }

    });

    function validate(){
        data = $("#order_form").serialize(true);
        Dajaxice.purchase.update_purchase(Dajax.process, {'form':data});
    }

});
