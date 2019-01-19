$(document).ready(function(){

    $.get('fav', function (d) {
        $('#fav_items').html(d);
    });

    sBar = $('#searchBar')
    sBut = $('#searchButton')

    sBut.on('click', function () {
        update_results();
        $.get('fav', function (d) {
            $('#fav_items').html(d);
        });
    });

    sBar.on('keypress', function(e) {
        if(e.which == 13) {
            e.preventDefault();
            update_results();
        }
        $.get('fav', function (d) {
            $('#fav_items').html(d);
        });
    });

    sBar.on('keyup', function(e){
        if (sBar.val() == '') {
            $('#result_items').html('');
            $.get('fav', function (d) {
                $('#fav_items').html(d);
            });
        }
    });

    function update_results() {
        $.get('search', {'q': sBar.val()}, function(d){
            $('#result_items').html(d);
        });
        update_favs()
        // $.get('search', )
    }

    function update_favs() {
        $.get('fav', function (d) {
            $('#fav_items').html(d);
        });
        // $.get('search', )
    }
});

