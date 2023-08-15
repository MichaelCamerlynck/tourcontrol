// toggles navbar when scrolled
$(document).on('scroll', function () {
    if (!isMobile()) {
        if (window.scrollY >= 100) {
            hideFullNav()
        } else {
            showFullNav()
        }
    }
})

function showFullNav() {
    $("#navA").show()
    $("#navA").removeClass("opacity-0")
    $("#navA").addClass("opacity-100")

    $("#navB").hide()
    $("#navB").addClass("opacity-0")
    $("#navB").removeClass("opacity-100")

    $("#navModal").addClass('lg:translate-x-[-40vw]')
    $(this).data("status", "open")
    $("#line1").removeClass("-rotate-45").addClass("-translate-y-[0.3rem]")
    $("#line2").removeClass("rotate-45").addClass("translate-y-[0.3rem]")
}

function hideFullNav() {
    $("#navB").show()
    $("#navB").removeClass("opacity-0")
    $("#navB").addClass("opacity-100")

    $("#navA").hide()
    $("#navA").addClass("opacity-0")
    $("#navA").removeClass("opacity-100")
}

// toggles expanding navbar
$("#navB").click(function () {
    if (isMobile()) {
        $("#navModal").toggleClass('translate-x-[-60vw]')
    } else {
        $("#navModal").toggleClass('lg:translate-x-[-40vw] translate-x-[-60vw]')
    }

    if ($(this).data("status") === "open") {
        $(this).data("status", "closed")
        $("#line1").removeClass("-translate-y-[0.3rem]").addClass("-rotate-45")
        $("#line2").removeClass("translate-y-[0.3rem]").addClass("rotate-45")
    } else {
        $(this).data("status", "open")
        $("#line1").removeClass("-rotate-45").addClass("-translate-y-[0.3rem]")
        $("#line2").removeClass("rotate-45").addClass("translate-y-[0.3rem]")
    }
})

let mouseOnFooter = false
$("#mainFooter").mouseenter(function () {
    mouseOnFooter = true
    $("#secondaryFooter").show().removeClass("translate-x-[4rem] opacity-0")
})

$("#mainFooter").mouseleave(function () {
    mouseOnFooter = false
    if (!isNearBottom()) {
        $("#secondaryFooter").addClass("translate-x-[4rem] opacity-0")
        setTimeout(function () {
            if (!mouseOnFooter && !isNearBottom()) {
                $("#secondaryFooter").hide()
            }
        }, 500)
    }
})

function isNearBottom() {
    const windowHeight = $(window).height(); // Height of the viewport
    const documentHeight = $(document).height(); // Total height of the document
    const scrollTop = $(window).scrollTop(); // Current scroll position

    const thresholdPercentage = 0.1;

    const distanceFromBottom = documentHeight - (scrollTop + windowHeight);

    // Check if the user is within the threshold percentage from the bottom
    return (distanceFromBottom / documentHeight) < thresholdPercentage;
}

function isMobile() {
    return window.innerWidth <= 768
}

if (isNearBottom() && window.location.href.indexOf("contact") === -1) {
    $("#secondaryFooter").show().removeClass("translate-x-[4rem] opacity-0")
}

if (isMobile()) {
    hideFullNav()
}

$(window).scroll(function () {
    if (isNearBottom() && window.location.href.indexOf("contact") === -1) {
        $("#secondaryFooter").show().removeClass("translate-x-[4rem] opacity-0")
    } else {
        $("#secondaryFooter").addClass("translate-x-[4rem] opacity-0")
        setTimeout(function () {
            if (!isNearBottom()) {
                $("#secondaryFooter").hide()
            }
        }, 500)
    }
})

$(".button-desc").click(function () {
    $(".text").hide()
    $(".text").addClass("opacity-0")
    $(`#${$(this).data("text")}`).show()
    $(`#${$(this).data("text")}`).removeClass("opacity-0")

    $(".fa-arrow-right").hide()
    $(".fa-chevron-right").show()
    $(this).find(".fa-arrow-right").show()
    $(this).find(".fa-chevron-right").hide()
    $(".transition-transform").removeClass("translate-x-6")
    $(this).find(".transition-transform").addClass("translate-x-6")
})

$("#contactUs").mouseenter(function () {
    $("#circleContact").addClass("scale-[2.9]")
    $("#arrowContact").removeClass("opacity-0")
})

$("#contactUs").mouseleave(function () {
    $("#circleContact").removeClass("scale-[2.9]")
    $("#arrowContact").addClass("opacity-0")
})
