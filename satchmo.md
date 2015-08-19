---
layout: oo_post
title: Louis Armstrong Discography
comments: false
tags: Louis Armstrong Visualization
published: true
---

#### Louis Armstrong's lifework visualized

I'm always excited when I create something that combines my passion with my profession. This is one such project, and I am very happy to share it with you.  

Louis Armstrong doesn't get nearly as much attention as he deserves, given his vast and lasting impact on music. I talked about him more extensively [in my previous post]({% post_url 2014-11-16-The-One-And-Only-Louis-Armstrong %}), but this time I wanted to explore something else. I thought it would be interesting to see his career visualized. To get a closer look into how and when his music got captured on record. So this is my humble attempt at that.  

This is a visualization of all sessions that comprise Louis Armstrong's discography. Each session is represented as a circle. The size of the circle represents the size of the band at that session, and the color is related to the location. The height of each session is given by the quantity of recording dates in a year around that session. So when he was busier recording, the circles will be higher.  
The visualization is also interactive. You can zoom in closer to get a better look. By hovering over the sessions, you will be able to see the details about them. You can also highlight only specific recording dates; say you are interested in seeing all the recording dates with Jack Teagarden. You simply select his name in the form below and all the sessions with him present, will be highlighted. You could also search for something like "all the sessions with Jack Teagarden, when they played Blueberry Hill". Just input "Blueberry Hill" and "Jack Teagarden" and the sessions that fit that query will pop up. This means you can do some fun stuff with this visualization.  

I invite you to explore it and let me know what you think. Let me know what are some of the things you looked for.  

### Details about the visualizaton

The main source of information for this visualization was [this online discography](http://michaelminn.net/discographies/armstrong/) by Michael Minn. Some recording dates or radio broadcasts have limited information about the dates, lineups and so on. This means that the uncertainty is also reflected in this visualization. Some sessions are excluded due to the lack of information. There are also some typos and other errors, which I am still cleaning up. If you find anything, let me know.  

And a few technical details, for those interested. I used [d3](http://d3js.org/) library for the actual visualization. I love it more and more, each time I use it. To get the data from the online discography, I used [import.io](http://import.io). And finally for parsing and cleaning up, Python was the way to go.


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
<div class="row clear song-selection hide-mobile">
    <form action="#">
        <label for="song-selection" class='col col-6 text-right'>Show sessions with these songs: </label>
        <select id="song-selection" multiple='multiple' class='col col-4'>
        </select>
</div>
<div class="row clear song-selection hide-mobile">
        <label for="lineup-selection" class='col col-6 text-right'>and these band members: </label>
        <select id="lineup-selection" multiple='multiple' class='col col-4'>
        </select>
    </form>
</div>

<em class="none show-mobile">Unfortunately this interactive visualization is not supported on mobile devices. Come check it out on your tablet or computer.</em>

<em class="ie-warning">This visualization might not work properly under your browser. Consider upgrading or getting a different browser.</em>


<script type="text/javascript" src="{{ "/js/d3.min.js" | prepend: site.baseurl }}"></script>
<script type="text/javascript" src="{{ "/js/louis_armstrong.js" | prepend: site.baseurl }}"></script>
<script type="text/javascript" src="{{ "/js/handlebars-v3.0.1.js" | prepend: site.baseurl }}"></script>
<script type="text/javascript" src="{{ "/js/underscore.min.js" | prepend: site.baseurl }}"></script>

<script id="event-template" type="text/x-handlebars-template">
{% raw %}
  <div class="entry">
    <h3>{{title}}</h3>
    <p>{{body}}</p>
  </div>
{% endraw %}
</script>
<script id="session-template" type="text/x-handlebars-template">
{% raw %}
<div class="row">
    <div class="col col-7 border-right">
        <h4 class="text-center">{{print_date}}<h4>
        <h3>{{name}}</h3>
        <h4>{{location}}</h4>
        <div class="first-section">
            <div class="inline-block no-split">
            {{#each members}}
                {{this}}{{#unless @last}}, {{/unless}} 
            {{/each}}
            </div>
            <div class="no-split inline-block">
            {{comments}}
            </div>
        </div>
    </div>
    <div class="col col-5 text-left">
        <div class="side-section inline-block text-left">
        <ul class="list-unstyled">
          {{#each song_list}}
            <li>
              <b>{{this}}</b>
            </li>
          {{/each}}
        </ul>
        </div>
    </div>
</div>
{% endraw %}
</script>

<script async type="text/javascript">
// Prepare the data
satchmo_songs = satchmo_data['songs'];
members = satchmo_data['members'];
satchmo_data = satchmo_data['sessions'];

// Filters
$(document).ready(function() {
  $("#song-selection").select2({
        data: satchmo_songs,
        placeholder: 'Start typing a song'
  });
  $("#lineup-selection").select2({
        data: members,
        placeholder: "Start typing a musician's name"
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
var margin = {top: 20, right: 40, bottom: 40, left: 50};
var width = $('.post').width() - margin.left - margin.right;
var height = 560 - margin.top - margin.bottom;

$('.plot-clip').width(width + 180)
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

var mScale = d3.scale.quantize()
                .range([0, 0.25, 0.75, 1])
                .domain([0, width]);

var hScale = d3.scale.quantize()
                .range([0, 0.25, 0.4])
                .domain([0, 1, 2]);

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

var rect = plotArea.append("rect")
    .attr("width", width)
    .attr("height", height)
    .style("fill", "none")
    .style("pointer-events", "all");

var sessions = plotArea.selectAll('circle').data(satchmo_data).enter()
        .append('circle')
        .attr('class', 'session')
        .attr('r', 5)
        .attr('cx', function (d) { return xScale(dateFormat.parse(d.display_date)); })
        .attr('cy', 3*height/4)
        .attr('fill', 'gray')
        .attr('fill-opacity', 0.3);


// Events

var source   = $("#event-template").html();
var eventTemplate = Handlebars.compile(source);

var importantEvents = [{
    title: 'August 4th, 1901',
    body: "Armstrong was born into a very poor family in New Orleans, Louisiana, the grandson of slaves. He spent his youth in poverty, in a rough neighborhood, known as “the Battlefield”, which was part of the Storyville legal prostitution district.",
    date: '04.12.1901',
    level: 3,
    yPosition: 0
},
{
    title: 'Little Louis is arrested',
    body: "Louis got arrested on New Year's Eve for shooting a revolver. He was sent to the Colored Waif's Home for Boys. It would be a turning point of his life.",
    date: '31.12.1912',
    level: 3,
    yPosition: 1
},
{
    title: 'Leaving home',
    body: "His old mentor, Joe King Oliver, called for him from Chicago. Louis wasn't going to leave New Orleans for anyone, except Joe King Oliver. So he went and joined the band.",
    date: '8.8.1922',
    level: 3,
    yPosition: 0
},
{
    title: 'Joe Glaser',
    body: "After returning from Europe Louis didn't have a band, recording contract, anything. He sought out Glaser. They struck a deal and it began a long-lasting business relationship.",
    date: '20.2.1935',
    level: 3,
    yPosition: 2
},
{
    title: 'Lucille Armstrong',
    body: "Louis and Lucille, his fourth and final wife, get married at Velma Middleton's home.",
    date: '12.10.1942',
    level: 2,
    yPosition: 2
},
{
    title: 'All Stars Band',
    body: "The famous Town Hall Concert where the All Stars Band was born. A band that would define the rest of his career.",
    date: '17.5.1947',
    level: 3,
    yPosition: 1
},
{
    title: 'Little Rock incident',
    body: "Armstrong stated publicly that Eisenhower was 'two-faced' and had 'no guts' as a response to the Little Rock incident.",
    date: '17.09.1957',
    level: 2,
    yPosition: 1
},
{
    title: 'Heart attack',
    body: "Armstrong's grueling touring schedule caught up with him in 1959, when he had a heart attack while traveling in Spoleto, Italy. After taking a few weeks off to recover, he was back on the road, performing 300 nights a year.",
    date: '23.06.1959',
    level: 3,
    yPosition: 0
},
{
    title: 'Hello, Dolly!',
    body: 'Louis records a song that would soon throw The Beatles of the first place on the charts!',
    date: '03.12.1963',
    level: 3,
    yPosition: 2
},
{
    title: 'What a Wonderful World',
    body: 'Armstrong records his last hit. A song that would remain loved to this day.',
    date: '08.10.1967',
    level: 3,
    yPosition: 1
}
];
// var importantEvents =[];


// Plot Events

var plotEvents = d3.select('#satchmo-container .plot-clip').selectAll('.important-event')
        .data(importantEvents)
        .enter()
        .append('div')
        .attr('class', 'important-event')
        .style('visibility', function (d) { return (isEventVisible(d)) ? 'visible' : 'hidden'})
        .attr('id', function (d, i) { return 'event-' + i; })
        .style('left', function (d) { return xScale(dateFormat.parse(d.date)) + 'px'; })
        .style('top', function (d) { return hScale(d.yPosition) * height + 30 + 'px'; })
        .html(function (d) { return eventTemplate(d); });

var eventLines = plotArea.selectAll('line')
    .data(importantEvents)
    .enter()
    .append('line')
    .style("stroke-dasharray", "5,2")
    .style('stroke', '#aaaaaa')
    .style('visibility', function (d, i) { return ($('#event-' + i).css('visibility') == 'hidden') ? 'hidden' : 'visible'; })
    .attr('x1', function (d) { return xScale(dateFormat.parse(d.date)); })
    .attr('x2', function (d) { return xScale(dateFormat.parse(d.date)); })
    .attr('y1', function (d, i) { return hScale(d.yPosition) * height + 30 + $('#event-' + i).height() + 'px'; })
    .attr('y2', height - 25)
    .style("pointer-events", "none");


// Interactivity

$('#song-selection').on('change', selectSongs);
$('#lineup-selection').on('change', selectSongs);
var selected = {};
function setSelected (selection, song_ids, member_ids) {
    var selectedSongs = {};
    var selectedMembers = {};
    if (song_ids !== null & typeof song_ids !== 'undefined') {
        selection.each(function (d) { return (d.song_id_list.some(function (el) { return song_ids.indexOf((el).toString()) > -1; })) ? (selectedSongs[d.id] = true) : (delete selectedSongs[d.id]); });
    } 
    if (member_ids !== null & typeof member_ids !== 'undefined') {
        selection.each(function (d) { return (d.member_id_list.some(function (el) { return member_ids.indexOf((el).toString()) > -1; })) ? (selectedMembers[d.id] = true) : (delete selectedMembers[d.id]); });        
    }
    if ((song_ids !== null & typeof song_ids !== 'undefined') | (member_ids !== null & typeof member_ids !== 'undefined')) {
        // console.log(selectedSongs);
        // console.log(selectedMembers);
        if (sizeOf(selectedMembers) == 0) {
            selected = selectedSongs;
        } else if (sizeOf(selectedSongs) == 0) {
            selected = selectedMembers;
        } else {
            selected = _.pick(selectedSongs, _.keys(selectedMembers));
        }
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
    sessions.call(setSelected, song_ids, member_ids);
    if ((song_ids !== null & typeof song_ids !== 'undefined') | (member_ids !== null & typeof member_ids !== 'undefined')) {
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

// rect.on("mouseover", mouseover)
//       .on("mouseout", mouseout)
//       .on("mousemove", mousemove);

// TODO Check if it's ok to use the same mouseover and mouseout functions
sessions.on("mouseover", mouseover)
        .on("mouseout", mouseout)
        .on('click', selectSession)
        .on('mousemove', mousemove);

function selectSession () {
    da = d3.select(this);
    session = da.data()[0];
    sessionInfo.style('visibility', 'visible');
    sessionInfo.html(sessionTemplate(session))
                .style('left', function (d) {
                    sessionInfoWidth = $(this).width();
                    xPosition = xScale(dateFormat.parse(session.display_date));
                    return xPosition - mScale(xPosition - margin.left) * sessionInfoWidth + 'px';
                })
                .style('top', margin.top  + 'px');

    var lowEnd = (sizeOf(selected) > 0) ? lowOpacity : 1;
    da.call(highlightSelected, lowEnd, 1)
        .attr('stroke', 'black')
        .attr('stroke-dasharray', 'none')
        .attr('stroke-opacity', 1)
        .attr('stroke-width', 1);
    var lowEnd = (sizeOf(selected) > 0) ? lowestOpacity : lowerOpacity;
    sessions.filter(function (d) { return session != d; })
            .call(highlightSelected, lowEnd, higherOpacity)
            .attr('stroke', function (d) { return cScale(d.location_group); })
            .attr('stroke-dasharray', '3,2')
            .attr('stroke-opacity', highOpacity)
            .attr('stroke-width', highOpacity);

}

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

    var lowEnd = (sizeOf(selected) > 0) ? lowOpacity : 1;
    sessions.filter(function (d) { return da == d; })
            .call(highlightSelected, lowEnd, 1)
            .attr('stroke', 'black')
            .attr('stroke-dasharray', 'none')
            .attr('stroke-opacity', 1)
            .attr('stroke-width', 1);

    sessionInfo.html(sessionTemplate(da))
                .style('left', function (d) {
                    sessionInfoWidth = $(this).width();
                    xPosition = xScale(dateFormat.parse(da.display_date));
                    return xPosition - mScale(xPosition - margin.left) * sessionInfoWidth + 'px';
                })
                .style('top', function (d) { return yScale(da.density) - 50 - $(this).height() + 'px'; });

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
    .text("Number of recording dates in a year");

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
        if ((windowHeight + $(this).scrollTop()) >= (containerPosition.top + containerHeight - 100)) {
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

function isEventVisible (da) {
    var x1 = xScale(dateFormat.parse(da.date));
    if (x1 > width) {
        return false;
    } else {
        // Is it overlapping with any Events of the same or higher level?
        x2 = x1 + 190;
        // For each event
        var overlapping = importantEvents.filter(function (d) {
            // Are they on the same height?
            if (d.yPosition != da.yPosition) {
                return false;
            } else if (da.level > d.level) {
                return false;
            } else {
                var a1 = xScale(dateFormat.parse(d.date));
                var a2 = a1 + 180;
                if (a1 > x1 & a1 < x2) {
                    return true;
                } else if (a1 < x1 & a2 > x1) {
                    return true;
                } else {
                    return false;
                }
            }
        });
        return overlapping.length == 0;
    }
}

function redrawChart() {
    svg.select('.x.axis').call(xAxis);
    sessions.attr('cx', function (d) { return xScale(dateFormat.parse(d.display_date)); });
    plotEvents.style('left', function (d) { return xScale(dateFormat.parse(d.date)) + 'px'; })
                .style('visibility', function (d) { return (isEventVisible(d)) ? 'visible' : 'hidden'});
    eventLines.attr('x1', function (d) { return xScale(dateFormat.parse(d.date)); })
                .attr('x2', function (d) { return xScale(dateFormat.parse(d.date)); })
                .style('visibility', function (d, i) { return ($('#event-' + i).css('visibility') == 'hidden') ? 'hidden' : 'visible'; });
}

</script>
