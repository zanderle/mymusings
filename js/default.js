/* ==========================================================
  Base Default JavaScript
  -- Table of Contents --
*/
$(document).ready(function() {
    $('#menu').on('click', function(e) {
        e.preventDefault();
        $('nav.site-nav').slideToggle(200);
    });

    var disqusPublicKey = "HUqw8lfxGW7tYNIJ883DE46T7sXUoxRBDGKRME2PLL8Vr2DI1uT2o68vDxYb7SbO";
    var disqusShortname = "mymusingsonmusic"; // Replace with your own shortname

    var urlArray = [];
    countComments = $('.count-disqus-comments');
    for (var i = 0; i < countComments.length; i++) {
        var url = $(countComments[i]).attr('data-disqus-url');
        urlArray.push('link:' + url);
    }

    if (urlArray.length > 0) {
        $.ajax({
            type: 'GET',
            url: "https://disqus.com/api/3.0/threads/set.jsonp",
            data: { api_key: disqusPublicKey, forum : disqusShortname, thread : urlArray },
            cache: false,
            dataType: 'jsonp',
            success: function (result) {

              for (var i in result.response) {

                var countText = " comments";
                var count = result.response[i].posts;

                if (count == 1)
                  countText = " comment";

                $('a[data-disqus-url="' + result.response[i].link + '"]').html(count + countText);

              }
            }
          });
    }
});