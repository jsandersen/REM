<template>
	<div id="linechartdiv">
  </div>
</template>

<script>
  import * as d3 from 'd3';
  import { mapGetters, mapActions, mapMutations } from 'vuex'

  export default {
	props: ['mode'],
    data: () => ({
      old_setting: '',
      tmp_settig: '',
	}),
	computed: {
      ...mapGetters(['getModerationControllData', 'getSelectedModerationControllSetting']),
    },
  watch: {
    getSelectedModerationControllSetting(newValue) {
        this.updateSelectedStrategy(newValue)
    }
  },
	methods : {
		onResize () {
        this.windowSize = { x: window.innerWidth, y: window.innerHeight }
      },
    updateSelectedStrategy(selectedData) {

                    this.focusCircleKneesel
                    .transition().duration(200)
                    .attr("cx", this.x(selectedData.load))
                    .attr("cy", this.y(selectedData.acc))
                    .style("opacity", 1)
                    this.focusLineKneeselgselX
                    .transition().duration(200)
                    .attr("x1", this.x(selectedData.load))
                    .attr("y1", this.height)
                    .attr("x2", this.x(selectedData.load))
                    .attr("y2", this.y(selectedData.acc))
                    .style("opacity", 1)

                    this.focusLineKneeselgselY
                    .transition().duration(200)
                    .attr("x1", 0)
                    .style("opacity", 1)
                    .attr("y1", this.y(selectedData.acc))
                    .attr("x2", this.x(selectedData.load))
                    .attr("y2", this.y(selectedData.acc))

    },
		...mapActions(['fetchModerationControllData']),
		...mapMutations(['setSelectedTimeSlice']),
		init(newValue) {
            var margin = {top: 10, right: 80, bottom: 40, left: 50},
            width = 460 - margin.left - margin.right,
            height = 390 - margin.top - margin.bottom;
            this.height = height

            this.svg = d3.select("#linechartdiv")
              .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
              .append("g")
                .attr("transform",
                    "translate(" + margin.left + "," + margin.top + ")")

            this.x = d3.scaleLinear()
                .domain([0,100])
                .range([ 0, width ]);
            this.svg.append("g")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(this.x));

            this.y = d3.scaleLinear()
                .domain([80, 100])
                .range([ height, 0 ]);
            this.svg.append("g")
                .call(d3.axisLeft(this.y));

            this.svg.append("rect")
                .attr("class", "shading")
                .attr("x", this.x(newValue.knee_point.load))
                .attr("width", width - this.x(newValue.knee_point.load))
                .attr("height", height)
                .attr("fill", "lightgrey")
                .style("cursor", "pointer")

            var bisect = d3.bisector(function(d) { return d.x; }).left;
            var bisectY = d3.bisector(function(d) { return d.y; }).left;

            var data = [] 
            for (var i = 0; i < newValue.model["load"].length; i++) {
                data.push({"x": newValue.model["load"][i], "y": newValue.model["acc"][i], 'eff': newValue.model["eff"][i], 'unc': newValue.model["unc"][i]})
            }

              // Add the line
            this.svg
                .append("path")
                .datum(data)
                .attr("fill", "none")
                .attr("stroke", "steelblue")
                .attr("stroke-width", 1.5)
                .attr("d", d3.line()
                .x(d => this.x(d.x) )
                .y(d => this.y(d.y) )
                )

              // Create the circle that travels along the curve of chart
            var focusCircleHover = this.svg
                .append('g')
                .append('circle')
                .style("fill", "none") //"none"
                .attr("stroke", "green")
                .attr('r', 5)
                .style("opacity", 0)
            
            var g = this.svg
                .append('g')

            var focusCircleKnee = g.append('circle')
                .style("fill", "orange") //"none"
                .attr("stroke", "orange")
                .attr('r', 5)
                .style("opacity", 1)
                .attr("cx", this.x(newValue.knee_point.load))
                .attr("cy", this.y(newValue.knee_point.acc))
                
                g.append('line')
                .style("opacity", 1)
                .style("stroke", "orange")
                .attr("x1", this.x(newValue.knee_point.load))
                .attr("y1", this.y(newValue.knee_point.acc))
                .attr("x2", this.x(newValue.knee_point.load))
                .attr("y2", height)
                
                g.append('line')
                .style("opacity", 1)
                .style("stroke", "orange")
                .attr("x1", 0)
                .attr("y1", this.y(newValue.knee_point.acc))
                .attr("x2", this.x(newValue.knee_point.load))
                .attr("y2", this.y(newValue.knee_point.acc))

            		this.svg.append("text")
                .attr("text-anchor", "end")
                .attr("y", -45)
                .attr("x", 0)
                .attr("dy", ".75em")
                .attr("transform", "rotate(-90)")
                .text(this.$t('expected') + " " + this.$t('acc') + " (%)");

                this.svg.append("text")             
                  .attr("transform", "translate(" + (width) + " ," + (height + margin.top + 25) + ")")
                  .style("text-anchor", "end")
                  .text(this.$t("effort") + " (%)");



            var gTmp = this.svg
              .append('g')

            var focusCircleTmp = gTmp
              .append('circle')
              .style("fill", "green") //"none"
              .attr("stroke", "green")
              .attr('r', 5)
              .style("opacity", 0)

            var focusLineXTmp = gTmp
                .append('line')
                .style("opacity", 0)
                .style("stroke", "green")

            var focusLineYTmp = gTmp
             .append('line')
             .style("opacity", 0)
             .style("stroke", "green")
            
            
            var focusText = this.svg
              .append('g')
              .append('text')
              .style("opacity", 0)
              .attr("text-anchor", "left")
              .attr("alignment-baseline", "middle")

            var focusLineX = this.svg
              .append('line')
              .style("opacity", 0)
              .style("stroke", "green")
              .style("stroke-dasharray", "5,5")

            var focusLineY = this.svg
                .append('line')
                .style("opacity", 0)
                .style("stroke", "green")
                .style("stroke-dasharray", "5,5")

                var gsel = this.svg
                    .append('g')

                this.focusCircleKneesel = gsel.append('circle')
                .style("fill", "blue") //"none"
                .attr("stroke", "blue")
                .attr('r', 5)
                .style("opacity", 1)
                .attr("cx", this.x(newValue.current_point.load))
                .attr("cy", this.y(newValue.current_point.acc))
                
               this.focusLineKneeselgselX = gsel.append('line') 
                .style("opacity", 1)
                .style("stroke", "blue")
                .attr("x1", this.x(newValue.current_point.load))
                .attr("y1", this.y(newValue.current_point.acc))
                .attr("x2", this.x(newValue.current_point.load))
                .attr("y2", height)
                
                this.focusLineKneeselgselY =gsel.append('line')
                .style("opacity", 1)
                .style("stroke", "blue")
                .attr("x1", 0)
                .attr("y1", this.y(newValue.current_point.acc))
                .attr("x2", this.x(newValue.current_point.load))
                .attr("y2", this.y(newValue.current_point.acc))

                var x = this.x
                var y = this.y

                function mouseover() {
                    focusCircleHover.style("opacity", 1)
                    focusText.style("opacity",1)
                    focusLineX.style("opacity",1)
                    focusLineY.style("opacity",1)
                }

                let mousemove = () => {
                    var thiss = this.rect['_groups'][0][0]

                    var x0 = x.invert(d3.mouse(thiss)[0]);
                    var y0 = y.invert(d3.mouse(thiss)[1]);
                    
                    var i = bisect(data, x0, 1);
                    var j = bisectY(data, y0, 1);
                    var selectedData = data[Math.max(i, j)]

                    this.tmp_settig = selectedData

                    this.$emit('tmp_settig', {'load': selectedData.x, 'acc': Math.round(selectedData.y * 1000) / 1000, 'name' : 'Benutzerdefiniert', 'eff' : selectedData.eff})

                    focusCircleHover
                    .attr("cx", x(selectedData.x))
                    .attr("cy", y(selectedData.y))
                    //focusText
                    //.html("Aufwand:" + selectedData.x + " - " + "Genaigkeit:" + Math.round(selectedData.y * 1000) / 1000)
                    //.attr("x", x(selectedData.x)+15)
                    //.attr("y", y(selectedData.y))
                    focusLineX
                    .attr("x1", x(selectedData.x))
                    .attr("y1", height)
                    .attr("x2", x(selectedData.x))
                    .attr("y2", y(selectedData.y)+5)
                    focusLineY
                    .attr("x1", 0)
                    .attr("y1", y(selectedData.y))
                    .attr("x2", x(selectedData.x)-5)
                    .attr("y2", y(selectedData.y))
                    }

                let mouseout = () => {
                    focusCircleHover.style("opacity", 0)
                    focusText.style("opacity", 0)
                    focusLineX.style("opacity", 0)
                    focusLineY.style("opacity", 0)

                    this.$emit('tmp_settig', {})
                }

                let click = () => {
                    var thiss = this.rect['_groups'][0][0]
                    var x0 = x.invert(d3.mouse(thiss)[0]);
                    var y0 = y.invert(d3.mouse(thiss)[1]);
                    var i = bisect(data, x0, 1);
                    var j = bisectY(data, y0, 1);
                    var selectedData = data[Math.max(i, j)]
                    
                    this.old_setting = selectedData

                    this.$emit('old_setting', {'load': selectedData.x, 'acc': Math.round(selectedData.y * 1000) / 1000, 'name' : 'Benutzerdefiniert', 'eff' : selectedData.eff, 'unc' : selectedData.unc})

                    focusCircleTmp
                    //.transition().duration(200)
                    .attr("cx", x(selectedData.x))
                    .attr("cy", y(selectedData.y))
                    .style("opacity", 1)
                    focusLineXTmp
                    //.transition().duration(200)
                    .attr("x1", x(selectedData.x))
                    .attr("y1", height)
                    .attr("x2", x(selectedData.x))
                    .attr("y2", y(selectedData.y))
                    .style("opacity", 1)
                    focusLineYTmp
                    //.transition().duration(200)
                    .attr("x1", 0)
                    .style("opacity", 1)
                    .attr("y1", y(selectedData.y))
                    .attr("x2", x(selectedData.x))
                    .attr("y2", y(selectedData.y))
                }

             this.svg.on("click", click);
            this.rect = this.svg
                .append('rect')
                .attr('class', 'linechartrect')
                .style("fill", "none")
                .style("pointer-events", "all")
                .attr('width', width)
                .attr('height', height)
                .on('mouseover', mouseover)
                .on('mousemove', mousemove)
                .on('mouseout', mouseout);
		},
		

	},
	mounted() {
    this.init(this.getModerationControllData)
    },
  }

</script>


<style>

.bar:hover {
  fill: brown;
}

.axis--x path {
  display: none;
}

#not_selected_1 {
  opacity: 0.4;
}
.bar-Offline:hover {
  cursor: pointer;
}
.bar-Online:hover {
  cursor: pointer;
}
.bar-Unsicher:hover {
  cursor: pointer;
}

.svg-container {
    display: inline-block;
    position: relative;
    width: 100%;
    padding-bottom: 100%; /* aspect ratio */
    vertical-align: top;
    overflow: hidden;
}
.svg-content-responsive {
    display: inline-block;
    position: absolute;
    top: 10px;
    left: 0;
}

</style>
