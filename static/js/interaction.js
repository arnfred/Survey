$(function() {

    // Get init timestamp
    var timestamps = [];
    var currentStep = ["intro1"]
    addTimeStamp(timestamps, currentStep[0])

    // Show first intro text
    $( "." + currentStep[0] ).fadeIn("fast");

    // Go to next section when we click on nav button
    $( ".next" ).on("click", function () {
        return next($(this).attr("id"), timestamps, currentStep);
    });

    // Make images selectable
    images()

    // Remove error box when we click on a radio field
    $( "input[type=radio]" ).each(function(i,f) { $(f).on("click", function() {
        $(f).parents(".question").removeClass("error");
    }); });
});


function next(step, timestamps, currentStep) {

    // Add timestamp
    addTimeStamp(timestamps, currentStep[0])

    // Check that the form is filled out properly
    if (step == "step1" && !formCheckErrors()) {
        return false;
    }

    // Check that enough images have been selected
    if (step == "step2") {
        if (!ImagesCheckErrors()) {
            return false;
        }
        else {
            ImagesMakeSortable();
        }
    }

    // Save data and furnish code
    if (step == "done") {
        if (!sortingCheckErrors()) {
            return false;
        }
        furnishData(timestamps)
    }

    // Hide old
    $(".section").has(":visible").fadeOut("fast");

    // Show new
    $("." + step).fadeIn("fast");

    // Update currentStep
    currentStep[0] = step

    // Cancel normal click event
    return false;

}


function images() {

    // Make images selectable
    $( "#images li" ).each(function (index,e) { $(e).on("click",function(event,li) { $(e).toggleClass("selected"); }) })

    // Preselect distractors (ONLY APPLICAPLE IF MARK_DISTRACTORS IS SET IN SURVEY.PY)
    $( "#images li img.distract" ).parent().toggleClass("selected");

    // Make bigger image appear
    $("li").each(function(i, li) { $(li).mouseover(function(e) {
        $("div#zoom img").attr('src',$(li).children("img").attr("src").replaceLast("/","/large/"));
    }); });
}


function addTimeStamp(timestamps, eventname) {
    timestamps.push({ "name" : eventname, "time" : Math.round(new Date().getTime() / 1000) });
}


function ImagesCheckErrors() {

    // Clear error messages
    $("#errorMsg").html("");

    // Check that we have at least selected some images
    if ($(".selected").length < 4) {
        $("#errorMsg").append("You need to select more images<br/>");
        return false;
    }
    else if ($("#question_pick").val() == "") {
        $("#errorMsg").append("You need to add text in the text area<br/>");
        return false;
    }
    else {
	return true
    }
}

function sortingCheckErrors() {
    // Clear error messages
    $("#errorMsg").html("");

    // Check that we have some text in the box
    if ($("#question_order").val() == "") {
        $("#errorMsg").append("You need to add text in the text area<br/>");
        return false;
    }
    else {
        return true
    }
}

function ImagesMakeSortable() {
    // Store how many clicks
    clicks = 0 // Yes, it's global. Sorry.
    // Make images sortable
    $( "#images ol" ).sortable({ tolerance: "pointer", items: ".item" });
    // Fade out not selected images
    $( "#images li" ).not(".selected, .endings").remove();
    // remove border
    $( "#images li" ).removeClass("selected")
    // remove click event
    $( "#images li" ).each(function (index,e) { $(e).off() });
    // count clicks
    $( "#images li" ).each(function (index,e) { $(e).on("mousedown", function() {
        clicks += 1;
    }) });
    // Set width to full page
    $( "#images ol" ).css("width","90%");
    // Resize all images to half size
    //$( "#images li" ).css("width", "150px");
    $( "li.item img" ).each(function(i, img) {
        //$(img).css("width", $(img).width()/2.0);
        $(img).css("cursor","move");
    });
    // increasing margin

    // Show start and end list items
    $( ".endings" ).fadeIn("fast");

}


function furnishData(timestamps) {

    // Collect data from questions
    var groups = $.makeArray($("input:radio").map(function(i,e) { return $(e).attr("name"); })).unique();
    questions = groups.map(function(n,i) { return { "name" : n, "value" : $("input[name=" + n + "]:checked").val() } });

    // Collect order of photos and collection name
    path_len = $("li.item img").filter(":visible").attr("src").split('/').length
    photos = $.makeArray($("li img").filter(":visible").map(function(i,im) { return $(im).attr("src").split('/')[path_len - 1]; }))
    collection = $("li.item img").filter(":visible").attr("src").split('/')[path_len - 2];

    // Collect timestamps
    time_diffs = timestamps.map(function(t,i) { if (i == 0) return { "name" : t.name, "time" : 0 }; else return { "name" : t.name, "time" : t.time - timestamps[i-1].time }; } );

    // Assemble data
    survey_data = {
        "questions" : questions,
        "photo_order" : photos,
        "collection" : collection,
        "time_diffs" : time_diffs,
        "clicks" : clicks, // global variable defined in makeImagesSortable
        //"begin_time" : timestamps[0],
        "question_pick" : $("#question_pick").val(),
        "question_order" : $("#question_order").val(),
        "window_x" : $(window).width(),
        "window_y" : $(window).height(),
        "mw_id" : getParameterByName("mw_id")

    }

    // Send data to server
    promise = $.post( "/", JSON.stringify(survey_data), function(data, textStatus, jqXHR) {
        //console.debug(data)
    }, "json");

    // Wait for response to show step5
    promise.complete(showVoucher)
}


function showVoucher(data) {

    // Fade out the waiting text
    $("#waiting").fadeOut("fast");

    // If the result was positive
    if (data.status == 200) {

        // Show voucher
        $("#voucher").html(data.responseText);
        $("#success").fadeIn("fast");
    }
    // If the result was a failure
    else {
        $("#failure").fadeIn("fast");
    }

}





function formCheckErrors() {

    // Clear the error messages from last run
    $("#errorMsg").html("");

    // Verify that form fields have been filled out
    var groups = $.makeArray($("input:radio").map(function(i,e) { return $(e).attr("name"); })).unique();
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



// Thanks to dextOr at
// http://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript
function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}
