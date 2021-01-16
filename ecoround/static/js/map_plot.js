function display_kills(playerId, kills) {

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

    //var x = d3.scaleLinear()
        //.domain([6300, -8250])
        //.range([ 0, width ]);

    var x = function(coord) {
        var translatedX = (0.000072 * coord + 0.460214)
        console.log("x: " + coord + " " + translatedX)
        return translatedX;
    }

    var y = function(coord) {
        return (-0.000072 * coord +	0.304687) * height;
    }

    //var y = d3.scaleLinear()
        //.domain([10000, -4500])
        //.range([ 0, height ]);

    svg = d3.select("#plot")

    svg.attr("width", width)
       .attr("height", height)

    console.log(playerId)
    kills.forEach(function(json) {
        console.log(json)
        kills = json["kills"]
        playerLocations = kills[0]["playerLocations"]
        player_kills = []
        player_deaths = []
        kills.forEach(function(kill) {
            //if (kill["victim"] === playerId) //defense
                //player_deaths.push(kill)
            if (kill["killer"] === playerId && kill)
                player_kills.push(kill)
        })
        svg.append('g').selectAll("dot")
           .data(player_kills)
           .enter()
           .append("circle")
           .attr("cx", function (d) {
               player = d["playerLocations"].find(element => element["subject"] === playerId)
               return x(player["location"]["x"]);
           })
           .attr("cy", function (d) {
               player = d["playerLocations"].find(element => element["subject"] === playerId)
               return y(player["location"]["y"]);
           })
           .attr("r", 7)
           .attr("fill", "green")
           .on("mouseover", function(ev, d) {
               console.log(d)
                svg.append("circle")
                   .attr("cx", function () {
                       return x(d["victimLocation"]["x"])-125;
                   })
                   .attr("cy", function () {
                       return y(d["victimLocation"]["y"])-125;
                   })
                   .attr("r", 7)
                   .attr("fill", "yellow")
                   .attr("class", "victim")
            })
            .on("mouseout", function(ev, d) {
                d3.select(".victim").remove()
            })
        svg.append('g').selectAll("dot")
           .data(player_deaths)
           .enter()
           .append("circle")
           .attr("cx", function (d) {return x(d["victimLocation"]["x"])-125})
           .attr("cy", function (d) {return y(d["victimLocation"]["y"])-125})
           .attr("r", 7)
           .attr("fill", "red")
           .on("mouseover", function(ev, d) {console.log(d)})
    })
}
