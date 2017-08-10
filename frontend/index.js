var loc_to_circle = {};
var loc_to_ip = {};
var host = '192.241.169.138'
var width = 960,
    height = 500;

var projection = d3.geo.mercator()
    .center([0, 5 ])
    .scale(150)
    .rotate([-180,0]);

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

var path = d3.geo.path()
    .projection(projection);

var g = svg.append("g");


function addPoint(loc,ip){

  var color  = (ip==host ? "green" : "red");
  var size = (ip==host ? 4.8 : 1.2);
  lat = loc.split(',')[0]
  lon = loc.split(',')[1]
  //g.append('a')
  //.attr("href", "http://www.google.com/")
  var el = g.append("circle")
  .on("click",function(){
          window.open("http://ipinfo.io/"+ip, '_blank')})
  .attr("cx", projection([lon, lat])[0])
  .attr("cy", projection([lon, lat])[1])
  .attr("r", size)
  .style("fill", color);
  // .transition()
  // .duration(1000)
  // .style("opacity", 0.0)
  // .remove(); //remove after transitions are complete

  loc_to_circle[loc] = el;


}
function drawline(srcip,srclat,srclon,dstlat,dstlon){
    var color = (srcip==host ? "green" : "red");
    var time = 0;
    var dur = 750 ;
    if(srcip==host){time=250;dur-=250}
    setTimeout(function(){
  g.append("line")          // attach a line
    .style("stroke", color)  // colour the line
    .style("stroke-width" , String(1+Math.random()))
    .attr("x1", projection([srclon, srclat])[0])     // x position of the first end of the line
    .attr("y1", projection([srclon, srclat])[1])      // y position of the first end of the line
    .attr("x2", projection([dstlon, dstlat])[0])     // x position of the second end of the line
    .attr("y2", projection([dstlon, dstlat])[1])
    .transition()
    .duration(dur)
    .style("opacity", 0.0)
    .remove(); },time);
}
function handlePoint(srcloc,srcip,dstloc,dstip){
  srclat = srcloc.split(',')[0]
  srclon = srcloc.split(',')[1]
  dstlat = dstloc.split(',')[0]
  dstlon = dstloc.split(',')[1]
  //g.append('a')
  //.attr("href", "http://www.google.com/")

  if(!(srcloc in loc_to_circle)){
    addPoint(srcloc,srcip);
  }
  if(!(dstloc in loc_to_circle)){
    addPoint(dstloc,dstip);
  }

  drawline(srcip,srclat,srclon,dstlat,dstlon);


  // g.append("circle")
  // .on("click",function(){
  //         window.open("http://ipinfo.io/"+ip, '_blank')})
  // .attr("cx", projection([lon, lat])[0])
  // .attr("cy", projection([lon, lat])[1])
  // .attr("r", 8)
  // .style("fill", "red")
  // .transition()
  // .duration(time)
  // .attr("r", 2)
  // .remove(); //remove after transitions are complete
}


// load and display the World
d3.json("world-110m2.json", function(error, topology) {



    //draw the country borders
    g.selectAll("path")
      .data(topojson.feature(topology, topology.objects.countries).features)
      .enter()
      .append("path")
      .attr("d", path);


    //plot some cities
    // load and display the cities
    // d3.csv("cities.csv", function(error, data) {
    //     g.selectAll("circle")
    //        .data(data)
    //        .enter()
    //        .append("a")
    //           .attr("xlink:href", function(d) {
    //             return "https://www.google.com/search?q="+d.city;}
    //           )
    //        .append("circle")
    //        .attr("cx", function(d) {
    //                return projection([d.lon, d.lat])[0];
    //        })
    //        .attr("cy", function(d) {
    //                return projection([d.lon, d.lat])[1];
    //        })
    //        .attr("r", 5)
    //        .style("fill", "red");
    // });


});



var zoom = d3.behavior.zoom()
    .on("zoom",function() {
        g.attr("transform","translate("+ 
            d3.event.translate.join(",")+")scale("+d3.event.scale+")");
        g.selectAll("path")  
            .attr("d", path.projection(projection)); 
});

svg.call(zoom)




// var x;
// $.getJSON('http://ipinfo.io/75.102.136.100', function(data) {
//   console.log(data)
//   x=data  //data is the JSON string
// });



var connection = new WebSocket('ws://192.241.169.138:81');

// When the connection is open, send some data to the server
connection.onopen = function () {
  console.log("opened")
};

// Log errors
connection.onerror = function (error) {
  console.log('WebSocket Error ' + error);
};



// Log messages from the server
connection.onmessage = function (e) {
  //console.log(e);
  var reader = new FileReader();
  reader.onload = function() {
      json = JSON.parse(reader.result );

      
  //     var p = g.selectAll("circle").data(json)
  //     .enter()
  //     .append("circle")

  // .attr("cx", function(d,i){   
  //   lat = d.split(',')[0];
  // lon = d.split(',')[1];
  // return projection([lon, lat])[0];} ) 

  // .attr("cy", function(d,i){ 
  //     lat = d.split(',')[0]
  // lon = d.split(',')[1]
  // return projection([lon, lat])[1];} )

  // .attr("r", 2)
  // .style("fill", "red")
  // .transition()
  // .duration(1000)
  // .attr("r", 0)
  // .remove();


  //console.log(json);
     // json.forEach(function f(locip_obj){
      //  handlePoint(locip_obj.loc, locip_obj.ip);
      //})
  
handlePoint(json[0].loc, json[0].ip,json[1].loc, json[1].ip );
  }
  reader.readAsText(e.data);
  
};


 //connection.send('p');
setTimeout(function(){ connection.send('p'); }, 400);
