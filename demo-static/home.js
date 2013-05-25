(function($) {
    $(function() {
        function set_personalized(yes) {
            $('#suggestions').toggleClass('personalized', yes);
        }

        $('#query-pane').on('click', '.toggler', function() {
            $('body').toggleClass('show-pane');
        }).on('click', '.query-trigger', function(e) {
            e.preventDefault();
            set_personalized(true);
            $.post('/update', {
                query: $(this).text().trim()
            }).done(function(html) {
                $('#suggestions .personalized ul').html(html);
            });
        }).on('click', '.clear-query', function(e) {
            e.preventDefault();
            set_personalized(false);
        });
    });
})(jQuery);
