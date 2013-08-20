$(function() {

    // Go to step 2 when button is clicked
    $( "#step1" ).click(step2)
    $( "#step2" ).click(step3)
    $( "#step3" ).click(step4)
});

function step2(e) {

    // Make images selectable
    $( "#images li" ).each(function (index,e) { $(e).click(function(event,li) { $(e).toggleClass("selected"); }) })

    // Fade out form and then fade in step2 and images
    $( ".step1" ).fadeOut("fast", function() {
        $( ".step2" ).fadeIn("fast");
        $( "#images" ).fadeIn("fast");
    });

}

function step3(e) {
    // Fade out not selected images
    $( "#images li" ).not(".selected").fadeOut("fast")
    $( ".step2" ).fadeOut("fast", function () { 
        $( ".step3" ).fadeIn("fast")
    })

    // Make the rest sortable
    $( "#images" ).sortable(); 

    return false
}

