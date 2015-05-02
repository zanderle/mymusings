---
layout: oo_post
title: Louis Armstrong Discography
comments: false
tags: Louis Armstrong Visualization
published: true
---
####Louis Armstrong's lifework visualized

<div id="satchmo-container">
    <div class="plot-clip">
    </div>
    <div id="satchmo" style="width: 100%; overflow: auto;"></div>
    <div class="tooltip">
        <div class="gig"></div>
        <div class="date-and-location"></div>
        <div class="songs"></div>
        <div class="lineup"></div>
        <div class="comments"></div>
    </div>
    <div id="session-info"></div>
</div>

<em class="none show-mobile">Unfortunately this interactive visualization is not supported on mobile devices. Come check it out on your tablet or computer.</em>
  

<span class="font-small">A few technical details, for those interested. I used [d3](http://d3js.org/) library for the actual visualization. To get the data from the website I mentioned earlier, I used [import.io](http://import.io) (which was a joy to use, if I may add). And finally for parsing and cleaning up, Python was the way to go.</span>


<script type="text/javascript" src="{{ "/js/d3.min.js" | prepend: site.baseurl }}"></script>
<script type="text/javascript" src="{{ "/js/louis_armstrong.js" | prepend: site.baseurl }}"></script>
<script type="text/javascript" src="{{ "/js/handlebars-v3.0.1.js" | prepend: site.baseurl }}"></script>

<script id="event-template" type="text/x-handlebars-template">
{% raw %}
  <div class="entry">
    <h3>{{title}}</h3>
    <p>
      {{body}}
    </p>
  </div>
{% endraw %}
</script>
<script id="session-template" type="text/x-handlebars-template">
{% raw %}
<h3>{{name}}</h3>
<h4>{{display_date}} - {{location}}</h4>
<div class="first-section">
<div class="inline-block left split">
{{lineup}}
</div>
<div class="inline-block left split">
  {{{songs}}}
</div>
</div>
<br/>
<br/>
<div class="no-split block">
{{comments}}
</div>
{% endraw %}
</script>

<script type="text/javascript">
// Set the dimensions of the canvas / graph
var margin = {top: 40, right: 40, bottom: 40, left: 40};
var width = $('.post').width() - margin.left - margin.right;
var height = 600 - margin.top - margin.bottom;

$('.plot-clip').width(width)
                .height(height)
                .css({'left': margin.left, 'top': margin.top});


// Other variables

// Date formater
var dateFormat = d3.time.format('%0d.%0m.%Y');

// Set scales
var minDate = dateFormat.parse('4.8.1901');
var maxDate = dateFormat.parse('6.7.1971');

var xScale = d3.time.scale()
            .range([0, width])
            .domain([minDate, maxDate]);

var cScale = d3.scale.ordinal()
            .range(["#a6cee3","#1f78b4","#b2df8a","#555","#fb9a99","#e31a1c","#fdbf6f","#ff7f00","#cab2d6","#6a3d9a","#ffff99","#b15928", "#8dd3c7","#ffffb3","#bebada","#fb8072","#80b1d3","#fdb462","#b3de69","#fccde5","#d9d9d9","#bc80bd","#ccebc5","#ffed6f"])
            .domain(satchmo_data, function (d) { d.location; });

var rScale = d3.scale.linear()
            .range([5, 18])
            .domain(d3.extent(satchmo_data, function (d) { return d.members.length; }));

// Zoom

var zoom = d3.behavior.zoom()
    .x(xScale)
    .scaleExtent([1,100])
    .on('zoom', zoomed);

// Moving average

var yValue = function(d) {
    interval = 360;
    low = d3.time.day.offset(d, -(interval/2));
    high = d3.time.day.offset(d, interval/2);
    // low = d3.time.day.offset(d, -interval);
    // high = d;
    function isInInterval (value) {
        return ((dateFormat.parse(value.display_date) < high) && (dateFormat.parse(value.display_date) > low));
    };
    recordings = satchmo_data.filter(isInInterval);
    return recordings.length/interval;
};

var yScale = d3.scale.linear()
                    .range([5*height/6, height/2])
                    .domain([0, d3.max(satchmo_data, function(d) { return yValue(dateFormat.parse(d.display_date)); })]);

var lineFunction = d3.svg.line()
                        .x(function (d) { return xScale(d); })
                        .y(function (d) { return yScale(yValue(d)); })
                        .interpolate('basis');

// var xScale = d3.scale.ordinal()
//                     .rangeBands([0, width], 0.52, 0.05)
//                     .domain(d3.range(d3.min(data, function(d) { return d.release_date - 1; }), d3.max(data, function(d) { return d.release_date + 1; })));
// var yScale = d3.scale.ordinal()
//                     .rangeBands([height, 0], 0, 0.1)
//                     .domain(d3.range(0, maxPerYear));
// var cScale = d3.scale.ordinal()
//                 .range(["#a6cee3","#1f78b4","#b2df8a","#555","#fb9a99","#e31a1c","#fdbf6f","#ff7f00","#cab2d6","#6a3d9a","#ffff99","#b15928", "#8dd3c7","#ffffb3","#bebada","#fb8072","#80b1d3","#fdb462","#b3de69","#fccde5","#d9d9d9","#bc80bd","#ccebc5","#ffed6f"])
//                 .domain(data, function(d) { return d.recording_locations.join(' or '); });
// var oScale = d3.scale.linear()
//                 .range([0.2, 1.0])
//                 .domain([0, 10]);
// var rScale = d3.scale.linear()
//                 .range([xScale.rangeBand()*0.7, xScale.rangeBand()*1.5])
//                 .domain([0, 10]);

// Set xAxis
var xAxis = d3.svg.axis().scale(xScale).orient('bottom');

// Add svg canvas
var svg = d3.select("#satchmo").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr('class', 'main')
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var plotArea = svg.append('g')
    .attr('clip-path', 'url(#plotAreaClip)')
    .call(zoom);

plotArea.append('clipPath')
    .attr('id', 'plotAreaClip')
    .append('rect')
    .attr('width', width)
    .attr('height',height);

var rect = plotArea.append("rect")
    .attr("width", width)
    .attr("height", height)
    .style("fill", "none")
    .style("pointer-events", "all");

var dates = d3.time.day.range(new Date(1900,1,1), new Date(1971,7,8), 180);

// Add sessions
var sessions = plotArea.selectAll('circle').data(satchmo_data).enter()
        .append('circle')
        .attr('class', 'session')
        .attr('r', function (d) { return rScale(d.members.length); })
        .attr('cx', function (d) { return xScale(dateFormat.parse(d.display_date)); })
        .attr('cy', function (d) { return yScale(yValue(dateFormat.parse(d.display_date))); })
        .attr('fill', function (d) { return cScale(d.location); })
        .attr('fill-opacity', 0.3);

// Add line
// var lineGraph = svg.append('path')
//                     .attr('d', lineFunction(dates))
//                     .attr('stroke', 'blue')
//                     .attr('stroke-width', 1)
//                     .attr('fill', 'none');


// Interactivity

var source   = $("#session-template").html();
var sessionTemplate = Handlebars.compile(source);
var sessionInfo = d3.select('#session-info');

sessions.on('mouseover', function (d) {
    sessionInfo.html(sessionTemplate(d))
                .style('left', (margin.left + xScale(dateFormat.parse(d.display_date))) + 'px')
                .style('top', margin.top + height/4 + 50 + 'px');
});

// Events

var source   = $("#event-template").html();
var eventTemplate = Handlebars.compile(source);

var importantEvents = [{
    title: 'Birth',
    body: "Armstrong was born into a very poor family in New Orleans, Louisiana, the grandson of slaves. He spent his youth in poverty, in a rough neighborhood, known as “the Battlefield”, which was part of the Storyville legal prostitution district.",
    date: '04.08.1901'
}];


// Plot Events

var plotEvents = d3.select('#satchmo-container .plot-clip').selectAll('.important-event')
        .data(importantEvents)
        .enter()
        .append('div')
        .attr('class', 'important-event')
        // .style('clip-path', 'url(#plotAreaClip)')
        .style('left', function (d) { return (margin.left + xScale(dateFormat.parse(d.date)) + 'px'); })
        .style('top', 80 + 'px')
        .html(function (d) { return eventTemplate(d); });

plotArea.selectAll('line')
    .data(importantEvents)
    .enter()
    .append('line')
    .style("stroke-dasharray", "5,2")
    .style('stroke', '#aaaaaa')
    .attr('x1', function (d) { return xScale(dateFormat.parse(d.date)); })
    .attr('x2', function (d) { return xScale(dateFormat.parse(d.date)); })
    .attr('y1', 180)
    .attr('y2', height - 25);

// Add axis

svg.append('g')
    .attr('class', 'x axis')
    .attr('transform', function (d) { return 'translate(0, ' + height + ')'; })
    .call(xAxis);

// Zoom functions

function zoomed() {
    if (xScale.domain()[0] < minDate) {
        var x = zoom.translate()[0] - xScale(minDate) + xScale.range()[0];
        zoom.translate([x, 0]);
    } else if (xScale.domain()[1] > maxDate) {
        var x = zoom.translate()[0] - xScale(maxDate) + xScale.range()[1];
        zoom.translate([x, 0]);
    }
    redrawChart();
}

function redrawChart() {
    svg.select('.x.axis').call(xAxis);
    sessions.attr('cx', function (d) { return xScale(dateFormat.parse(d.display_date)); });
    plotEvents.style('left', function (d) { return (margin.left + xScale(dateFormat.parse(d.date)) + 'px'); })
}

</script>
