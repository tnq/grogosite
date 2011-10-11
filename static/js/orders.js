$(document).ready(function() {

    var shipping_string = ", Shipping";

    //Called when the shipping checkbox is toggled
    $("#id_shipping").change(function() {
        update_shipping();
    });   
    
    //Called when the patron radio buttons are changed
    $("input[name=patron]").change( function () {
        $("#comments").val( $("input:checked[name=patron]").attr("title") );
        $("#amount").val( $("input:checked[name=patron]").val() );
        update_shipping();
    });
    
    //Called when the button is pressed
    $("#ship_to_bill").click(function() {
        $("#shipTo_street1").val( $("#billTo_street1").val() );
        $("#shipTo_street2").val( $("#billTo_street2").val() );
        $("#shipTo_city").val( $("#billTo_city").val() );
        $("#shipTo_state").val( $("#billTo_state").val() );
        $("#shipTo_postalCode").val( $("#billTo_postalCode").val() );

    });
        
    function update_shipping() {
        if ($("#id_shipping").is(":checked")) {
            $("#required_if_shipping").show();
            var comment_field = $("#comments");
            var shipping_field = $ ("#shipping_price");
            var amount_field = $("#amount");
            
            comment_field.val( comment_field.val() + shipping_string ); 
            amount_field.val( parseInt(amount_field.val()) + parseInt(shipping_field.val()) );
            
                
        } else {
            $("#required_if_shipping").hide();
            var comment_field = $( "#comments" );
            var shipping_field = $ ("#shipping_price");
            var amount_field = $("#amount");
            
            comment_field.val( comment_field.val().replace(shipping_string, ""));
            amount_field.val( parseInt(amount_field.val()) - parseInt(shipping_field.val()) );
        }
    }
     
});
