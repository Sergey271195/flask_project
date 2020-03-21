
    $(document).ready(function(){
    $("#routeBtn").click(function(){
        $("#RouteModal").modal("show");
        $.getJSON('/getData/', {info: 'currency'},
            function(data) {
            addCurrency(data, '#currency')});
    });

    $("#housingBtn").click(function(){
        $("#AccomodationModal").modal("show");
        $.getJSON('/getData/', {info: 'currency'},
            function(data) {
            addCurrency(data, '#currency_accomodation')});
    });

    $("#myBtn").click(function(){
        $("#RouteModal").modal("hide");
        $('#origin').empty().selectpicker('refresh');
        $('#destination').empty().selectpicker('refresh');
        $('#currency').empty().selectpicker('refresh');
    });

    $(document).on('keyup', '.origin .bs-searchbox input', function (e) {
        var searchData = e.target.value;
        $('#origin').empty().selectpicker('refresh');
            $.getJSON('/getData/', {info: 'city', data: searchData},
            function(data) {
            addOptions(data, '#origin')});
    });

    $(document).on('keyup', '.destination .bs-searchbox input', function (e) {
        var searchData = e.target.value;
        $('#destination').empty().selectpicker('refresh');
            $.getJSON('/getData/', {info: 'city', data: searchData},
            function(data) {
            addOptions(data, '#destination')});
    });

    $(document).on('keyup', '.country .bs-searchbox input', function (e) {
        var searchData = e.target.value;
        $('#country').empty().selectpicker('refresh');
            $.getJSON('/getData/', {info: 'country', data: searchData},
            function(data) {
            addOptions(data, '#country')});
    });

$('#searchInput').on('input', function() { 
    var value = $(this).val();
    var parentDiv = $('.parent-route');
    $('div .route-div').removeHighlight();
    $('div .route-div').highlight(value);
    if (value.length > 0) { 
        $(parentDiv).each( function (index, element) {
            text = '';
            $(this).find('.route-div').each(function (index, element) {
                text += $( this ).text();
            });
            if (text.toLowerCase().includes(value.toLowerCase()) == false) {
                $(this).hide();
            }
            else {
                $(this).show();
                }
            });
        }
    else {
        $(parentDiv).each(function (index, element) {
            $(this).show();
        });
    };
});

    $('#searchBtn').click(function() {
        var value = $('#searchInput').val();
        var parentDiv = $('.parent-route');
        $(parentDiv).each( function (index, element) {
            text = '';
            $(this).find('.route-div').each(function (index, element) {
                text += $( this ).text();
            });
            if (text.toLowerCase().includes(value.toLowerCase()) == false) {
                $(this).hide();
                }
            });
        });
    });
