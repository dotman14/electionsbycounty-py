
$(document).ready(function () {
    //Tabbed Menu
    $(".tabs-menu a").click(function (event) {
        event.preventDefault();
        $(this).parent().addClass("current");
        $(this).parent().siblings().removeClass("current");
        var tab = $(this).attr("href");
        $(".tab-content").not(tab).css("display", "none");
        $(tab).fadeIn();
    });


    //Timeline display
    let timelineBlocks = $('.cd-timeline-block'),
    offset = 0.8;

    //hide timeline blocks which are outside the viewport
    hideBlocks(timelineBlocks, offset);

    //on scrolling, show/animate timeline blocks when enter the viewport
    $(window).on("scroll", function () {
        (!window.requestAnimationFrame)
            ? setTimeout(function () { showBlocks(timelineBlocks, offset); }, 100)
            : window.requestAnimationFrame(function () { showBlocks(timelineBlocks, offset); });
    });

    function hideBlocks(blocks, offset) {
        blocks.each(function () {
            ($(this).offset().top > $(window).scrollTop() + $(window).height() * offset) && $(this).find(".cd-timeline-img, .cd-timeline-content").addClass('is-hidden');
        });
    }

    function showBlocks(blocks, offset) {
        blocks.each(function () {
            ($(this).offset().top <= $(window).scrollTop() + $(window).height() * offset && $(this).find('.cd-timeline-img').hasClass('is-hidden')) && $(this).find('.cd-timeline-img, .cd-timeline-content').removeClass('is-hidden').addClass('bounce-in');
        });
    }

    //Auto complete. Homepage and API Generate page.
    $("#County, #HomeViewModel_County").autocomplete({
        source: function (request, response) {
            $.ajax({
                url: "https://electionsbycounty.com",
                //url: document.origin,
                //url: "https://localhost/Elections"
                type: "POST",
                dataType: "json",
                scroll: true,
                data: { prefix: request.term },
                success: function (data) {
                    response($.map(data, function (item) {
                        return { label: item.AreaName + "-" + item.State, value: item.AreaName + "-" + item.State };
                    }));
                }
            });
        }
    });


    //Insert selected text from text box and drop down into span
    $("#type").change(function () {
        var value = $("#type option:selected").text();
        $("#inserttype").text(value);
    }).keyup();

    $('#HomeViewModel_County').on('autocompleteselect', function (e, ui) {
        var countyState = ui.item.value;
        $('#insertstate').text(countyState.substr(countyState.length - 2, 2));
        $('#insertcounty').text(countyState.substr(0, countyState.length - 3));
    });


    //Hook up account drop down with Bootstrap.
    $(".dropdown-toggle").dropdown();

    //Download image from result page.
    $(".embedIcon")
     .click(function () {
         html2canvas($(this).parent(), {
             onrendered: function (canvas) {
                 var myImage = canvas.toDataURL("image/png", 1);
                 window.open(myImage);
             }
         });
     });

    //Smooth Scrolling
    $('a[href^="#"]').on('click', function (e) {
        e.preventDefault();

        var target = this.hash;
        var $target = $(target);

        $('html, body').stop().animate({
            'scrollTop': $target.offset().top - 175 //Offset for fixed headers
        }, 900, 'swing');
    });

    //To include anchor fragments in URL when year is clicked
    //$('html, body').stop().animate({
    //    'scrollTop': $target.offset().top - 137
    //}, 900, 'swing', function () {
    //    window.location.hash = target;
    //});
});