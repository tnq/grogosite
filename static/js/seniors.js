$(document).ready(function() {

    num_lines = $("[name=form-TOTAL_FORMS]").val();

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
            $("#activity_section"+num_lines).remove();
        }
    });
});
