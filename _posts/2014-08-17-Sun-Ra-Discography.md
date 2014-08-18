---
layout: post
title: Sun Ra Discography
comments: true
tags: Sun Ra Visualization
---
####Sun Ra's eclectic and prolific discography, visualized

With over 1000 recorded songs and well over 100 albums, Sun Ra was one of the most prolific artists of the 20th century. I decided to make a little visualization of this enormous body of work. As I soon realized, this is no easy task. Sun Ra as a person and his whole life has been shrouded in mystery. His music was no different. For many albums, it is unknown where or when they were recorded. Often, they'll have a couple of different dates and personel stated.


<div id="sunra"></div>
<script type="text/javascript" src="{{ "/js/d3.min.js" | prepend: site.baseurl }}"></script>
<script type="text/javascript" src="{{ "/js/sunra_disco.js" | prepend: site.baseurl }}"></script>
<script type="text/javascript">
// Set the dimensions of the canvas / graph
var margin = {top: 30, right: 30, bottom: 30, left: 30};
var width = $('.post').width() - margin.left - margin.right;
var height = 500 - margin.top - margin.bottom;

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
                    .rangeBands([height/2, 0], 0, 0.1)
                    .domain(d3.range(0, maxPerYear));
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
    .style('fill', function(d) { return 'url(#' + d.title.replace(/\s+|\(|\)|\'/g, '-') + ')'; });

svg.append('g')
    .attr('class', 'x axis')
    .attr('transform', function(d) { return 'translate(0, ' + height/2 + ')'; })
    .call(xAxis);

// Interactivity
records.on('mouseover', function(d) {    
    d3.select(this)
        .transition()
        .duration(100)
        .attr('r', 25);
}).on('mouseout', function() {
    d3.select(this)
        .transition()
        .duration(200)
        .attr('r', xScale.rangeBand());
});

// Hover
// border glede na lokacijo
// Posamezni albumi clickable
// Razbij albume na recording sessions

</script>
