$(document).ready(function() {

    $("#id_name_comments").hide();
    $("label[for='id_name_comments']").hide();
    num_lines = $("[name=form-TOTAL_FORMS]").val();
    
    check_buttons(num_lines);
    
    //When the add button is clicked, copy the hidden div
    //to allow another old book to be ordered
    $("#add_button").click(function() {
        num_lines = $("[name=form-TOTAL_FORMS]").val();
        $("[name=form-TOTAL_FORMS]").val(parseInt(num_lines)+1);
        
        html = $("#form_template").clone().html().replace(/__prefix__/g, num_lines).replace(/__prefix2__/g, parseInt(num_lines)+1);
        check_buttons(parseInt(num_lines)+1);
        $("#forms").append(html);
    });

    //When the remove button is clicked, remove the last book added
    // (down to the current year's book) and re-validate
    $("#remove_button").click(function() {
        num_lines = $("[name=form-TOTAL_FORMS]").val();
        if (num_lines > 1) { //Always leave one form for the current year
            num_lines = parseInt(num_lines)-1;
            $("[name=form-TOTAL_FORMS]").val(num_lines);
            check_buttons(num_lines);
            $("#activity_section"+num_lines).remove();
        }
    });
    
    $("#show_name_comments").change(function() {
        if ($("#show_name_comments").attr("checked") == "checked") {
            $("#id_name_comments").show();
            $("label[for='id_name_comments']").show();
        } else {
            $("#id_name_comments").hide();
            $("label[for='id_name_comments']").hide();
        }
        
    });
});

function check_buttons (lines) {
    if (lines <= 1) {
        $("#add_button").show();
        $("#remove_button").hide();
    } else if (lines >=4) {
        $("#add_button").hide();
        $("#remove_button").show();
    } else {
        $("#add_button").show();
        $("#remove_button").show();
    }
}
