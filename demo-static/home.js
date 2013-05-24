(function($) {
    $(function() {
        $(document).on('click', '.query-trigger', function(e) {
            e.preventDefault();
            $.post('/update', {
                query: $(this).text().trim()
            }).done(function(html) {
                $('#suggestions').html(html);
            });
        });
    });
})(jQuery);
