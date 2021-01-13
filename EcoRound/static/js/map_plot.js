$(function() {

    var width = 1075
    var height = 1075

    d3.select(".map").attr("width", width).attr("height", height)

    // 450 -682
    // ->
    // 310, 660
    //
    // 2815, 808
    // ->
    // 135, 550

    var x = d3.scaleLinear()
        .domain([6300, -8250])
        .range([ 0, width ]);

    var y = d3.scaleLinear()
        .domain([10000, -4500])
        .range([ 0, height ]);

    svg = d3.select("#plot")

    svg.attr("width", width)
       .attr("height", height)

    kills.forEach(function(file) {
        d3.json("data/" + player_id + "/" + file).then(function(json) {
            if (json["matchInfo"]["mapId"] !== "/Game/Maps/Port/Port") {
                return
            }
            console.log(file)
            kills = json["kills"]
            playerLocations = kills[0]["playerLocations"]
            player_kills = []
            player_deaths = []
            kills.forEach(function(kill) {
                //if (kill["victim"] === player_id) //defense
                    //player_deaths.push(kill)
                if (kill["killer"] === player_id && kill)
                    player_kills.push(kill)
            })
            svg.append('g').selectAll("dot")
               .data(player_kills)
               .enter()
               .append("circle")
               .attr("cx", function (d) {
                   player = d["playerLocations"].find(element => element["subject"] === player_id)
                   return x(player["location"]["x"])-125;
               })
               .attr("cy", function (d) {
                   player = d["playerLocations"].find(element => element["subject"] === player_id)
                   return y(player["location"]["y"])-125;
               })
               .attr("r", 7)
               .attr("fill", "green")
               .on("mouseover", function(ev, d) {console.log(d)})
            svg.append('g').selectAll("dot")
               .data(player_deaths)
               .enter()
               .append("circle")
               .attr("cx", function (d) {return x(d["victimLocation"]["x"])-125})
               .attr("cy", function (d) {return y(d["victimLocation"]["y"])-125})
               .attr("r", 7)
               .attr("fill", "red")
               .on("mouseover", function(ev, d) {console.log(d)})
        });
    })
});
