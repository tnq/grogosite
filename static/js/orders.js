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
    
    $("#submitbutton").click(function() {
        return validateForm();
    });
        
    function update_shipping() {
        if ($("#id_shipping").is(":checked")) {
            $("#required_if_shipping").show();
            $("#shipTo_country").val( "us" );
            
            var comment_field = $("#comments");
            var shipping_field = $ ("#shipping_price");
            var amount_field = $("#amount");
            
            comment_field.val( comment_field.val() + shipping_string ); 
            amount_field.val( parseInt(amount_field.val()) + parseInt(shipping_field.val()) );
            
                
        } else {
            $("#required_if_shipping").hide();
            $("#shipTo_country").val( "" );
            
            var comment_field = $( "#comments" );
            var shipping_field = $ ("#shipping_price");
            var amount_field = $("#amount");
            
            comment_field.val( comment_field.val().replace(shipping_string, ""));
            amount_field.val( parseInt(amount_field.val()) - parseInt(shipping_field.val()) );
        }
    }
    
    function validateForm() {
    
        var errorString = "";
        
        // verify that a positive numeric amount has been entered
        var amount = $('#amount').val();
        var amountValue = parseInt(amount);
                
        if ( isNaN(amountValue) || amountValue <= 0) {
            errorString = "The amount entered is invalid\n";
        }
        
        // Validate Bill To Fields
        if (
          ($('#billTo_firstName').val().length < 1)
          ||
          ($('#billTo_lastName').val().length < 1)
         ) {
            errorString = errorString + "Billing First and Last names are required\n";
        }
        
        if ($('#billTo_street1').val().length < 1) {
            errorString = errorString + "Billing Street Address is required\n";
        }
        
        if ($('#billTo_city').val().length < 1) {
            errorString = errorString + "Billing City is required\n";
        }
        
        if ($('#billTo_state').val().length < 1) {
            errorString = errorString + "Billing State is required\n";
        }
        
        if ($('#billTo_postalCode').val().length < 1) {
            errorString = errorString + "Billing Postal Code is required\n";
        }
        
        
        if ($('#billTo_phoneNumber').val().length < 1) {
            errorString = errorString + "Billing Phone Number is required\n";
        }
        
        if ($('#billTo_email').val().length < 1) {
            errorString = errorString + "Billing Email is required\n";
        }
        
        
        // Validate Ship To Fields
        if (
           ($('#shipTo_firstName').val().length < 1)
           ||
           ($('#shipTo_lastName').val().length < 1)
         ) {
             errorString = errorString + "Shipping First and Last names are required\n";
        }
        
        if ($("#id_shipping").is(":checked")) {
        
            if ($('#shipTo_street1').val().length < 1) {
                errorString = errorString + "Shipping Street Address is required\n";
            }
            
            if ($('#shipTo_city').val().length < 1) {
                errorString = errorString + "Shipping City is required\n";
            }
            
            if ($('#shipTo_state').val().length < 1) {
                errorString = errorString + "Shipping State is required\n";
            }
            
            if ($('#shipTo_postalCode').val().length < 1) {
                errorString = errorString + "Shipping Postal Code is required\n";
            }
        }
                
        if (errorString == "") {
            return true;
        } else {
            alert(errorString);
            return false;
        }
    }
    
    
});
