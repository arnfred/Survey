$(function() {

    // Go to step 2 when button is clicked
    $( "#step1" ).click(step2)
    $( "#step2" ).click(step3)
    $( "#step3" ).click(step4)

    // Remove error box when we click on a radio field
    $( "input[type=radio]" ).each(function(i,f) { $(f).click(function() { 
        $(f).parents(".question").removeClass("error"); 
    }); });
});

function step2(e) {

    // Check that the form has been filled out and if not, abort
    if (step2CheckErrors() == false) return false

    // Make images selectable
    $( "#images li" ).each(function (index,e) { $(e).click(function(event,li) { $(e).toggleClass("selected"); }) })

    // Fade out form and then fade in step2 and images
    $( ".step1" ).fadeOut("fast", function() {
        $( ".step2" ).fadeIn("fast");
        $( "#images" ).fadeIn("fast");
    });

    // Clear error messages
    $("#errorMsg").html("");

    return true;
}

function step3(e) {

    // Check that we have at least selected some images
    if ($(".selected").length < 4) {
        $("#errorMsg").append("You need to select more images<br/>");
        return false;
    }
    
    // Fade out not selected images
    $( "#images li" ).not(".selected").fadeOut("fast")
    $( ".step2" ).fadeOut("fast", function () { 
        $( ".step3" ).fadeIn("fast")
    })

    // Make the rest sortable
    $( "#images" ).sortable(); 

    // Clear error messages
    $("#errorMsg").html("");

    return false
}

function step4(e) {
    // Collect data

    return false
}

function step2CheckErrors() {

    // Verify that form fields have been filled out
    var groups = $.makeArray($("input:radio").map(function(i,e) { return $(e).attr("name"); })).unique();
    console.debug(groups)
    // For each group, check that there is a buttom that has been checked
    var tally = groups.map(function(n,i) { 
        var field = $("input[name=" + n + "]"); 
        var noError = true;
        if (!field.is(":checked")) { 
            field.parents(".question").addClass("error"); 
            $("#errorMsg").append("Error in question #" + (i+1) + "<br/>");
            noError = false;
        }
        return noError;
    })

    // If we have any fields where there were errors, don't proceed
    return tally.every(function(a) { return a });
}
