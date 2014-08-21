---
layout: post
title: Sun Ra Discography
comments: true
tags: Sun Ra Visualization
---
####Sun Ra's eclectic and prolific discography, visualized

<div id="sunra-container">
    <div id="sunra"></div>
    <div class="row text-center no-margin no-padding">
        <div class="button-container">
            <a href="#" class="button belleza" id="ratings-button">Show Allmusic Ratings</a>
        </div>
    </div>
    <div class="row clear">
        <div class="sunra-cover left breathe col-2"></div>
        <div class="sunra-content left col-6">
            Year: <h2 class="year"><span></span></h2>
            Title: <h3 class="title"><span></span></h3>
            Author: <h3 class="author"><span></span></h3>
        </div>
        <div class="sunra-content left col-3">
            Recorded in: <h3 class="dates"><span></span></h3>
            in <h3 class="locations"><span></span></h3>
        </div>
    </div>
    <div class="row clear review-content">
        <div class="col col-2">
            Review by: <h3 class="review-by"><span></span></h3> <br/>
            <a href="#" class="allmusic-link" target="_blank">Allmusic page</a>
        </div>
        <div class="col push-1 col-9"><blockquote class="review no-margin"></blockquote></div>
    </div>
</div>

<em class="none show-mobile">Unfortunately this interactive visualization is not supported on mobile devices. Come check it out on your tablet or computer.</em>

[EDIT] Since I first posted this, I updated the visualization with some additional data from [allmusic](http://www.allmusic.com/artist/sun-ra-mn0000924232/discography).

With over 1000 recorded songs spanned over more than 100 albums, Sun Ra was one of the most prolific artists of the 20th century. I decided to make a simple visualization of this enormous body of work. I soon realized, this is no easy task. For one, the discography data is confusing to say the least. For a lot of albums, it is unclear who was in the band or where or when it was recorded. The band members themselves often gave conflicting reports regarding these things. I did my best with the data I could find in the [discography online](http://www.the-temple.net/sunradisco/list.php).  
After that confusion, I had to make a decision about which data to show. I eventually decided I am only going to visualize full-length albums (so excluding singles and records where Sun Ra appeared as guest).  

  
So here it is - a simple timeline of Sun Ra's recorded work. The albums are positioned on the timeline based on the year they were released (or if they have not been released - when they were recorded). The colors represent the whereabouts of recording sessions. If you hover over specific works, additional information will show up.
I might eventually expand it with some more features, but that's it for now. I hope you like it :).  
  

Let me know what you think!
  


<span class="font-small">A few technical details, for those interested. I used [d3](http://d3js.org/) library for the actual visualization. To get the data from the website I mentioned earlier, I used [import.io](http://import.io) (which was a joy to use, if I may add). And finally for parsing and cleaning up, Python was the way to go.</span>


<script type="text/javascript" src="{{ "/js/d3.min.js" | prepend: site.baseurl }}"></script>
<script type="text/javascript" src="{{ "/js/sunra_disco.js" | prepend: site.baseurl }}"></script>
<script type="text/javascript">
// Set the dimensions of the canvas / graph
var margin = {top: 30, right: 30, bottom: 30, left: 30};
var width = $('.post').width() - margin.left - margin.right;
var height = 270 - margin.top - margin.bottom;

// Other variables

// Prepare data
var yearlyData = d3.nest()
                    .key(function(d) { return d.release_date; })
                    .sortKeys(d3.ascending)
                    .entries(data);
var maxPerYear = d3.max(yearlyData, function(d) { return d.values.length; });

// Set scales
var xScale = d3.scale.ordinal()
                    .rangeBands([0, width], 0.52, 0.05)
                    .domain(d3.range(d3.min(data, function(d) { return d.release_date - 1; }), d3.max(data, function(d) { return d.release_date + 1; })));
var yScale = d3.scale.ordinal()
                    .rangeBands([height, 0], 0, 0.1)
                    .domain(d3.range(0, maxPerYear));
var cScale = d3.scale.ordinal()
                .range(["#a6cee3","#1f78b4","#b2df8a","#555","#fb9a99","#e31a1c","#fdbf6f","#ff7f00","#cab2d6","#6a3d9a","#ffff99","#b15928", "#8dd3c7","#ffffb3","#bebada","#fb8072","#80b1d3","#fdb462","#b3de69","#fccde5","#d9d9d9","#bc80bd","#ccebc5","#ffed6f"])
                .domain(data, function(d) { return d.recording_locations.join(' or '); });
var oScale = d3.scale.linear()
                .range([0.2, 1.0])
                .domain([0, 10]);
var rScale = d3.scale.linear()
                .range([xScale.rangeBand()*0.7, xScale.rangeBand()*1.5])
                .domain([0, 10]);

// Scale helper
var centered = function(i) {
// Function that starts from the center of the interval and spreads out
    return Math.floor(maxPerYear/2) - (i - Math.floor(i/2))*Math.pow(-1, i);
};

// Set axis
var xAxis = d3.svg.axis().scale(xScale).orient('bottom').tickValues(['1956', '1960', '1970', '1980', '1990', '1998']);

// Add svg canvas
var svg = d3.select("#sunra").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Add covers
var defs = svg.append('defs');
defs.selectAll('pattern')
    .data(data)
    .enter()
    .append('pattern')
    .attr('id', function(d) { return d.title.replace(/\s+|\(|\)|\'/g, '-'); })
    .attr('x', 0)
    .attr('y', 0)
    .attr('height', 1)
    .attr('width', 1)
    .attr('viewBox', '0 0 100 100')
    .attr('preserveAspectRatio', 'none')
    .append('image')
    .attr('x', 0)
    .attr('y', 0)
    .attr('height', 100)
    .attr('width', 100)
    .attr('preserveAspectRatio', 'none')
    .attr('xlink:href', function(d) { return d.cover; });

// Add albums
var g = svg.selectAll('g').data(yearlyData).enter()
        .append('g')
        .attr('transform', function(d) { return 'translate(' + xScale(d.key) + ', 0)'; });
var records = g.selectAll('circle')
    .data(function(d) { return d.values; })
    .enter()
    .append('circle')
    .attr('class', 'record')
    .attr('r', xScale.rangeBand())
    .attr('cy', function(d, i) { return yScale(centered(i)); })
    .style('fill', function(d) { return 'url(#' + d.title.replace(/\s+|\(|\)|\'/g, '-') + ')'; })
    .style('stroke', function(d) { return cScale(d.recording_locations); });

// Add axis
svg.append('g')
    .attr('class', 'x axis')
    .attr('transform', function(d) { return 'translate(0, ' + height + ')'; })
    .call(xAxis);

// Interactivity
var lock = false;
records.on('mouseover', function(d) {
    if (!lock) {
        d3.select(this)
            .transition()
            .duration(100)
            .attr('r', 25)
            .style('stroke-width', 4);
        d3.select('.sunra-cover')
            .style('background-image', function() { return 'url("' + d.cover + '")'; });
        $('.sunra-content').show();
        $('.sunra-content .year span').html(d.release_date);
        $('.sunra-content .title span').html(d.title);
        $('.sunra-content .author span').html(d.author);
        $('.sunra-content .dates span').html(d.recording_dates.join(', '));
        $('.sunra-content .locations span').html(d.recording_locations.join(', '));
        if (d.review != "") {
            $('.review-content').fadeIn(200);
            $('.review-content .review').html(d.review)
                                        .attr('cite', d.allmusic_url);
            $('.review-content .review-by span').html(d.review_by);
            $('.review-content .allmusic-link').attr('href', d.allmusic_url);
        }
        else {
            $('.review-content').fadeOut(400);
        }
    }
}).on('click', function() {
    if (lock) {
        d3.select(this)
            .transition()
            .duration(100)
            .attr('r', 25)
            .style('stroke-width', 4);
        lock = false;
    } else {
        d3.select(this)
            .transition()
            .duration(100)
            .attr('r', 30)
            .style('stroke-width', 5);
        lock = true;
    }
}).on('mouseout', function() {
    if (!lock) {
        if ($('#ratings-button').hasClass('active')) {
            d3.select(this)
                .transition()
                .duration(200)
                .attr('r', function(d) { return rScale(d.allmusic_rating); })
                .style('stroke-width', 2);
        } else {
            d3.select(this)
                .transition()
                .duration(200)
                .attr('r', xScale.rangeBand())
                .style('stroke-width', 2);
        }
    }
});

$('#ratings-button').on('click', function(e) {
    lock = false;
    e.preventDefault();
    var button = $('#ratings-button');
    button.toggleClass('active');
    if (button.hasClass('active')) {
        records.transition()
                .duration(200)
                .style('opacity', function(d) { return oScale(d.allmusic_rating); })
                .style('stroke-width', 2)
                .attr('r', function(d) { return rScale(d.allmusic_rating); });
    } else {
        records.transition()
                .duration(200)
                .style('opacity', 1)
                .style('stroke-width', 2)
                .attr('r', xScale.rangeBand());
    }
})

// Razbij albume na recording sessions
// Več informacij za posamezen album

</script>
