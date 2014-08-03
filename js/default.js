/* ==========================================================
  Base Default JavaScript
  -- Table of Contents --
*/
$(document).ready(function() {
    $('#menu').on('click', function(e) {
        e.preventDefault();
        $('nav.site-nav').slideToggle(200);
    });
});