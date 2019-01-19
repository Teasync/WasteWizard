$(document).ready(function(){

    sBar = $('#searchBar')
    sBut = $('#searchButton')

    sBut.on('click', function () {
        console.log('button clicked');
        update_results();
    });

    sBar.on('keypress', function(e) {
        if(e.which == 13) {
            e.preventDefault();
            update_results();
        }
    });

    sBar.on('keyup', function(e){
        if (sBar.val() == '') {
            $('#result_items').html('');
        }
    });

    function update_results() {
        console.log(sBar.val());
        $.get('search', {'q': sBar.val()}, function(d){
            $('#result_items').html(d);
        });
        // $.get('search', )
    }
});

