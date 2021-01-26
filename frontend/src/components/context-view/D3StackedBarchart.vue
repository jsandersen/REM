<template>
	<div v-resize="onResize">
			<svg class="stackedBarChart" width="100%" height="280" viewBox="0 0 960 280" preserveAspectRatio="none"></svg>	
	</div>
</template>

<script>
  import * as d3 from 'd3';
  import { mapGetters, mapActions, mapMutations } from 'vuex'

  export default {
	props: ['mode'],
    data: () => ({
		windowSize: {
        x: 0,
        y: 0,
      }
	}),
	computed: {
      ...mapGetters(['getTimeChartData', 'getSelectedRootTopic', 'getSelectedUser', 'getSelectedTimeFrame', 'getSelectedTimeSlice']),
    },
	methods : {
		onResize () {
        this.windowSize = { x: window.innerWidth, y: window.innerHeight }
      },
		...mapActions(['fetchTimechartData']),
		...mapMutations(['setSelectedTimeSlice']),
		init() {

			var xOffset = 60
			var xGapFactor = .1
			var yOffset = 10

			var chartHight = 250
			var chartWidth = 800

			this.xScale = d3.scaleBand().rangeRound([0, chartWidth]).padding(0.1)
			this.yScale = d3.scaleLinear().rangeRound([chartHight, 0])

			this.xAxis = d3.axisBottom(this.xScale)
			this.yAxis = d3.axisLeft(this.yScale)//.tickValues(d3.range(0, max+1, 10));

			this.zColors = d3.scaleOrdinal()
				.range(["#e15759", "#bab0ac", "#59a14f"]);

			this.svg = d3.select(".stackedBarChart")

			this.rect = this.svg.append("rect")
				.attr("x", xOffset)
				.attr("y", yOffset)
				.attr("width", chartWidth)
				.attr("height", chartHight)
				.attr("fill", "white")
				.on('click', () => {
					this.setSelectedTimeSlice(null)
				})

			this.g = this.svg.append("g").attr("transform", "translate(" + xOffset + "," + yOffset + ")");

			this.x = this.g.append("g")
				.attr("class", "axis axis--x")
				.attr("transform", "translate(0," + chartHight + ")")

			this.y = this.g.append("g")
				.attr("class", "axis axis--y")

			this.bars = this.g.append("g")
				.attr("class", "bars")

			this.group = this.svg.append("g")
					.attr("transform", "translate(" + xOffset + "," + yOffset + ")")

			this.svg.append("text")
				.attr("text-anchor", "end")
				.attr("y", 6)
				.attr("x", -7)

				.attr("dy", ".75em")
				.attr("transform", "rotate(-90)")
				.text(this.$t('time_chart_y_label'));
				
		},
		updateData(data, keys) {

			var max = d3.max(data, d => d.total)
			
			var svg = d3.select(".stackedBarChart") 

			this.xScale.domain(data.map(d => d.key))
			this.yScale.domain([0, max]).nice();
			this.zColors.domain(keys);

			this.xAxis.tickValues(this.xScale.domain().filter(function(d,i){ return !(i%7)}));

			this.x.transition().delay(200).duration(400).call(this.xAxis);
			this.y.transition().delay(200).duration(400).call(this.yAxis)

			keys.forEach((key, index) => {
				
				var stack = d3.stack().keys(keys)(data)[index]
				var bar = this.group
					.selectAll(".bar-" + key)
					.data(stack, d => d.data.key + "-" + key )
				
				bar.exit()
					.remove()

				bar.transition().duration(200)
					.attr("x", d => this.xScale(d.data.key) )
					.attr("y", d => this.yScale(d[1]) )
					.attr("height", d => this.yScale(d[0]) - this.yScale(d[1]) )
					.attr("width", this.xScale.bandwidth() )

				bar.enter().append("rect")
					.attr("class", "bar-" + key )
					.attr("x", d => this.xScale(d.data.key) )
					.attr("y", d => this.yScale(0) )
					.attr("width", this.xScale.bandwidth() )
					.attr("fill", d => this.zColors(key) )
					.attr("row",  function(d, i) {return d.data.key;})
					.attr("id", function() {
						var other = svg.selectAll("#not_selected_1")
						if(other.empty()) {
							return 'selected_1'
						} else {
							return 'not_selected_1'
						}
					} )
					.on('click', (d, i) => {
						var row = d3.select("rect[row='" + d.data.key + "']")
						var old_id = row.attr('id')
						var other = svg.selectAll("#not_selected_1")
								
						svg.selectAll("rect").attr('id', 'not_selected_1')
							if (!other.empty() && old_id == 'selected_1') {
								svg.selectAll("rect").attr('id', 'selected_1')
								this.setSelectedTimeSlice(null)
							} else {
								svg.selectAll("rect[row='" + row.attr('row') + "']").attr('id', 'selected_1')
								this.setSelectedTimeSlice(d.data.key)
							}
						
						})
					.transition().delay(0).duration(400)
						.attr("height", d => this.yScale(d[0]) - this.yScale(d[1]) )
						.attr("y", d => this.yScale(d[1]) )
			})

		}
	},
	mounted() {
		this.init() 
		  this.fetchTimechartData()
		  this.onResize()
    },
	watch: {
		getSelectedTimeFrame() {
			this.setSelectedTimeSlice(null)
        	this.fetchTimechartData()
		},
		getSelectedRootTopic() {
			this.fetchTimechartData()
		},
		getTimeChartData(newValue) {
			var initData = newValue.series
			var keys = [];
			for (var key in initData[0]){
				if (key != "key" && key != "total")
				keys.push(key);
			}

			this.updateData(initData, keys)

		},
		getSelectedUser() {
			this.fetchTimechartData()
		},
		getSelectedTimeSlice(newVal) {
			if(newVal == null) {
				this.svg.selectAll("rect").attr('id', 'selected_1')
			}
		}
	}
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
