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
<div class="row clear song-selection">
    <form action="#">
        <label for="song-selection">Filter by songs: </label>
        <select id="song-selection" multiple='multiple' class='col-6'>
        </select>
    </form>
</div>
<div class="row clear song-selection">
    <form action="#">
        <label for="lineup-selection">Filter by band members: </label>
        <select id="lineup-selection" multiple='multiple' class='col-6'>
        </select>
    </form>
</div>

<em class="none show-mobile">Unfortunately this interactive visualization is not supported on mobile devices. Come check it out on your tablet or computer.</em>

<em class="ie-warning">This visualization might not work properly under your browser. Consider upgrading or getting a different browser.</em>

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

<script async type="text/javascript">

$(document).ready(function() {
  $("#song-selection").select2({
        data: satchmo_songs
  });
  $("#lineup-selection").select2({
        data: members
  });
});

// Helpers
function sizeOf(obj) {
    var count = 0;

    for(var prop in obj) {
        if(obj.hasOwnProperty(prop))
            ++count;
    }

    return count;
}

// Set the dimensions of the canvas / graph
var margin = {top: 40, right: 40, bottom: 40, left: 50};
var width = $('.post').width() - margin.left - margin.right;
var height = 600 - margin.top - margin.bottom;

$('.plot-clip').width(width)
                .height(height)
                .css({'left': margin.left, 'top': margin.top});


// Variables
var lowestOpacity = 0.01;
var lowerOpacity = 0.07;
var lowOpacity = 0.1;
var mediumOpacity = 0.3;
var highOpacity = 0.5;
var higherOpacity = 0.8;

// Date formater
var dateFormat = d3.time.format('%0d.%0m.%Y');

// Set scales
var minDate = dateFormat.parse('4.8.1901');
var maxDate = dateFormat.parse('6.7.1971');

var xScale = d3.time.scale()
            .range([0, width-10])
            .domain([minDate, maxDate]);

var cScale = d3.scale.ordinal()
            .range(["#8dd3c7","#d5d500","#bebada","#fb8072","#80b1d3","#fdb462","#b3de69","#fccde5","#d9d9d9","#bc80bd","#ccebc5","#ffed6f"])
            .domain(satchmo_data, function (d) { d.location_group; });

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
    // Don't use this if you don't have to. Very expensive...
    interval = 360;
    low = d3.time.day.offset(d, -(interval/2));
    high = d3.time.day.offset(d, interval/2);
    // low = d3.time.day.offset(d, -interval);
    // high = d;
    function isInInterval (value) {
        return ((dateFormat.parse(value.display_date) < high) && (dateFormat.parse(value.display_date) > low));
    };
    recordings = satchmo_data.filter(isInInterval);
    return recordings.length;
};

var yScale = d3.scale.linear()
                    .range([height, height/2])
                    .domain([-2, d3.max(satchmo_data, function(d) { return d.density; })]);
                    // .domain([0, 37]);

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
var yAxis = d3.svg.axis().scale(yScale).orient('left');


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


var dates = d3.time.day.range(new Date(1900,1,1), new Date(1971,7,8), 180);

// Add sessions
for (var i = satchmo_data.length - 1; i >= 0; i--) {
    satchmo_data[i].id = i;
};

var sessions = plotArea.selectAll('circle').data(satchmo_data).enter()
        .append('circle')
        .attr('class', 'session')
        .attr('r', 5)
        .attr('cx', function (d) { return xScale(dateFormat.parse(d.display_date)); })
        .attr('cy', 3*height/4)
        .attr('fill', 'gray')
        .attr('fill-opacity', 0.3);

var rect = plotArea.append("rect")
    .attr("width", width)
    .attr("height", height)
    .style("fill", "none")
    .style("pointer-events", "all");

// Add line
// var lineGraph = svg.append('path')
//                     .attr('d', lineFunction(dates))
//                     .attr('stroke', 'blue')
//                     .attr('stroke-width', 1)
//                     .attr('fill', 'none');



// Events

var source   = $("#event-template").html();
var eventTemplate = Handlebars.compile(source);

var importantEvents = [{
    title: '04 Aug 1901',
    body: "Armstrong was born into a very poor family in New Orleans, Louisiana, the grandson of slaves. He spent his youth in poverty, in a rough neighborhood, known as “the Battlefield”, which was part of the Storyville legal prostitution district.",
    date: '04.08.1901'
},
{
    title: 'Hello, Dolly!',
    body: 'Louis Armstrong records a song that would soon throw The Beatles of the first place on the charts!',
    date: '03.12.1963'
}
];
var importantEvents =[];


// Plot Events

var plotEvents = d3.select('#satchmo-container .plot-clip').selectAll('.important-event')
        .data(importantEvents)
        .enter()
        .append('div')
        .attr('class', 'important-event')
        // .style('clip-path', 'url(#plotAreaClip)')
        .style('left', function (d) { return xScale(dateFormat.parse(d.date)) + 'px'; })
        .style('top', 80 + 'px')
        .html(function (d) { return eventTemplate(d); });

var eventLines = plotArea.selectAll('line')
    .data(importantEvents)
    .enter()
    .append('line')
    .style("stroke-dasharray", "5,2")
    .style('stroke', '#aaaaaa')
    .attr('x1', function (d) { return xScale(dateFormat.parse(d.date)); })
    .attr('x2', function (d) { return xScale(dateFormat.parse(d.date)); })
    .attr('y1', 220)
    .attr('y2', height - 25);


// Interactivity

$('#song-selection').on('change', selectSongs);
$('#lineup-selection').on('change', selectSongs);
var selected = {};
function setSelected (selection, song_ids, member_ids) {
    var selectedSongs = {};
    var selectedMembers = {};
    if (song_ids) {
        selection.each(function (d) { return (d.song_id_list.some(function (el) { return song_ids.indexOf((el).toString()) > -1; })) ? (selectedSongs[d.id] = true) : (delete selectedSongs[d.id]); });
    } 
    if (member_ids) {
        selection.each(function (d) { return (d.member_id_list.some(function (el) { return member_ids.indexOf((el).toString()) > -1; })) ? (selectedMembers[d.id] = true) : (delete selectedMembers[d.id]); });        
    }
    if (typeof song_ids !== 'undefined' | typeof member_ids !== 'undefined') {
        selected = $.extend(selectedSongs, selectedMembers);
    } else {
        selected = {};
    }
}

function highlightSelected (selection, lowEnd, highEnd) {
    lowEnd = typeof lowEnd !== 'undefined' ? lowEnd : lowerOpacity;
    highEnd = typeof highEnd !== 'undefined' ? highEnd : lowerOpacity;
    selection.attr('fill-opacity', function (d) { return (d.id in selected) ? highEnd : lowEnd; });
}

function selectSongs () {
    var song_ids = $('#song-selection').val();
    var member_ids = $('#lineup-selection').val();
    sessions.call(setSelected, song_ids, member_ids)
    if (typeof song_ids !== 'undefined' | typeof member_ids !== 'undefined') {
        sessions.call(highlightSelected, lowestOpacity, higherOpacity);
    } else {
        sessions.attr('fill-opacity', mediumOpacity)
                .attr('stroke', 'none');
    }
};


var source   = $("#session-template").html();
var sessionTemplate = Handlebars.compile(source);
var sessionInfo = d3.select('#session-info');

bisectDate = d3.bisector(function(d) { return dateFormat.parse(d.display_date); }).left

rect.on("mouseover", mouseover)
      .on("mouseout", mouseout)
      .on("mousemove", mousemove);

function mouseover () {
    var lowEnd = (sizeOf(selected) > 0) ? lowestOpacity : lowerOpacity;
    sessions.call(highlightSelected, lowEnd, higherOpacity);
    sessionInfo.style('visibility', 'visible');
    plotEvents.style('opacity', lowOpacity);
    eventLines.attr('opacity', lowOpacity);
    d3.selectAll('.legend').attr('opacity', lowOpacity);
}
function mouseout () {
    if (sizeOf(selected) > 0) {
        sessions.call(highlightSelected, lowestOpacity, higherOpacity)
                .attr('stroke', 'none');
    } else {
        sessions.attr('fill-opacity', mediumOpacity)
                .attr('stroke', 'none');
    }

    sessionInfo.style('visibility', 'hidden');
    plotEvents.style('opacity', 1);
    eventLines.attr('opacity', 1);
    d3.selectAll('.legend').attr('opacity', 1);
}

function mousemove () {
    var x0 = xScale.invert(d3.mouse(this)[0]),
        i = bisectDate(satchmo_data, x0, 1),
        d0 = satchmo_data[i - 1],
        d1 = satchmo_data[i],
        da = x0 - dateFormat.parse(d0.display_date) > dateFormat.parse(d1.display_date) - x0 ? d1 : d0;

    sessions.filter(function (d) { return da == d; })
            .attr('fill-opacity', 1)
            .attr('stroke', 'black')
            .attr('stroke-dasharray', 'none')
            .attr('stroke-opacity', 1)
            .attr('stroke-width', 1)

    sessionInfo.html(sessionTemplate(da))
                .style('left', function (d) {
                    sessionInfoWidth = $(this).width();
                    xPosition = xScale(dateFormat.parse(da.display_date));
                    return xPosition  + sessionInfoWidth > width + margin.left ? (80 + xPosition - sessionInfoWidth + 'px') : (xPosition + 'px');
                })
                .style('top', margin.top  + 'px');

    var lowEnd = (sizeOf(selected) > 0) ? lowestOpacity : lowerOpacity;
    sessions.filter(function (d) { return da != d; })
            .call(highlightSelected, lowEnd, higherOpacity)
            .attr('stroke', function (d) { return cScale(d.location_group); })
            .attr('stroke-dasharray', '3,2')
            .attr('stroke-opacity', highOpacity)
            .attr('stroke-width', highOpacity);

}

// Add legend

var legend = svg.append('g')
    .attr('class', 'legend')
    .attr('transform', function (d) { return 'translate(60, ' + (height - 60) + ')'; })

legend.append('text')
    .attr('fill', 'black')
    .attr('text-anchor', 'middle')
    .attr('x', 0)
    .attr('y', -rScale.range()[1] - 10)
    .text('Band size');

legend.append('circle')
    .attr('r', rScale.range()[1])
    .attr('cx', 0)
    .attr('cy', 0)
    .attr('fill', 'none')
    .attr('stroke-width', 1)
    .attr('stroke-dasharray', '2,2')
    .attr('stroke', '#555');

legend.append('circle')
    .attr('r', rScale.range()[0])
    .attr('cx', 0)
    .attr('cy', rScale.range()[1] - rScale.range()[0])
    .attr('fill', 'none')
    .attr('stroke-width', 1)
    .attr('stroke-dasharray', '2,2')
    .attr('stroke', '#555');

legend.append('text')
    .text(rScale.domain()[1])
    .attr('fill', '#555')
    .attr('font-size', 12)
    .attr('text-anchor', 'left')
    .attr('dy', 4)
    .attr('x', rScale.range()[1] + 13);

legend.append('line')
    .attr('stroke-width', 1)
    .attr('stroke', '#555')
    .attr('x1', rScale.range()[1] + 2)
    .attr('x2', rScale.range()[1] + 10)
    .attr('y1', 0)
    .attr('y2', 0);

legend.append('text')
    .text('2')
    .attr('fill', '#555')
    .attr('font-size', 12)
    .attr('text-anchor', 'left')
    .attr('dy', 4)
    .attr('x', rScale.range()[1] + 13)
    .attr('y', rScale.range()[1] - rScale.range()[0]);

legend.append('line')
    .attr('stroke-width', 1)
    .attr('stroke', '#555')
    .attr('x1', rScale.range()[0] + 2)
    .attr('x2', rScale.range()[1] + 10)
    .attr('y1', rScale.range()[1] - rScale.range()[0])
    .attr('y2', rScale.range()[1] - rScale.range()[0]);

// Add axis

svg.append('g')
    .attr('class', 'x axis')
    .attr('transform', function (d) { return 'translate(0, ' + height + ')'; })
    .call(xAxis);

svg.append('g')
    .attr('transform', function (d) { return 'translate(0, 0)'; })
    .attr('class', 'y axis')
    .call(yAxis);

// now add titles to the axes
svg.append("text")
    .attr('class', 'axis-label')
    .attr("text-anchor", "middle")  // this makes it easy to centre the text as the transform is applied to the anchor
    .attr("transform", "translate(-"+ (margin.left - 7)+","+(2*height/3)+")rotate(90)")  // text is drawn off the screen top left, move down and out and rotate
    .text("Number of recordings in a year");

svg.append("text")
    .attr('class', 'axis-label')
    .attr("text-anchor", "middle")  // this makes it easy to centre the text as the transform is applied to the anchor
    .attr("transform", "translate("+ (width/2) +","+(height+margin.bottom)+")")  // centre below axis
    .text("Date");


// Initial transition

n = satchmo_data.length;
duration = 1500;

containerPosition = $('#satchmo-container').position();
containerHeight = $('#satchmo-container').height();
windowHeight = $(window).height();
notFired = true;

$(window).scroll(function () {
    if (notFired) {
        if ((windowHeight + $(this).scrollTop()) >= (containerPosition.top + containerHeight)) {
            notFired = false;
            setTimeout(transitionSessions, 1);
        }
    }
});
function transitionSessions() {
    sessions.transition()
        .delay(function(d, i) { return 50 + i / n * duration; })
        // .attr('fill-opacity', 0.3)
        // .transition()
        // .delay(function(d, i) { return duration + i / n * duration / 3; })
        .attr('r', function (d) { return rScale(d.members.length); })
        .attr('fill', function (d) { return cScale(d.location_group); })
        .attr('cy', function (d) { return yScale(d.density); });
}

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
    plotEvents.style('left', function (d) { return xScale(dateFormat.parse(d.date)) + 'px'; });
    eventLines.attr('x1', function (d) { return xScale(dateFormat.parse(d.date)); })
                .attr('x2', function (d) { return xScale(dateFormat.parse(d.date)); });
}

</script>
