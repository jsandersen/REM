<template>
    <div>
      <v-toolbar dense elevation="0" style="background:white;">
        <v-toolbar-title>{{ $t('bar_chart1_title')}}</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-select
            class="mt-6"
            :items="items2"
            v-model="selectedTopic"
            style="width: 7em; font-size: 19px"
          ></v-select>

      </v-toolbar>

      <v-toolbar dense elevation="0" style="background:white;">
        <TopicSearch/>
        <v-spacer></v-spacer>

        <div class="mt-6">
          <v-flex style="width: 12em;">
            <v-select
              outlined
              :items="items"
              v-model="mode"
              dense
              :label="$t('sort')"
            ></v-select>
          </v-flex >
        </div>
      </v-toolbar>

		  <svg class="groupedBarChart" width="200" height="350"> <!-- viewBox="0 0 450 360" preserveAspectRatio="none"> -->

      </svg>

      <v-pagination
        v-model="currentPage"
        :length="currentLength"
        circle
        :total-visible="5"
        ></v-pagination>
        

	</div>	
</template>

<script type="text/javascript">
import TopicSearch from './TopicSearch'
  import * as d3 from 'd3';
   import { mapGetters, mapActions, mapMutations } from 'vuex'

  export default {
    components: {
    TopicSearch
    },
    data: () => ({
      items : [
        {text: 'Valid', value: 'online',},
        {text: 'Uncertain', value: 'unsicher',}, 
        {text: 'Blocked', value: 'offline',}, 
        {text: 'Total', value: 'summe',},
      ],
      mode : 'unsicher',
      currentLength : 1, // (getRootTopics.length / 5) -1
      items2 : ['Topic', 'Article'],
      selectedTopic : 'Topic'
	}),
	computed: {
      ...mapGetters(['getBarChartData', 'getSelectedRootTopic', 'getSelectedUser', 'getBarChartCurrentPage', 'getRootTopics', 'getSelectedTimeSlice', 'getSelectedTime']),
  currentPage: {
        get() {
          return this.getBarChartCurrentPage;
        },        
        set(value) {
          this.fetchBarChartData()
          this.setBarChartCurrentPage(value)
        }
    },
        },
	methods : {
    ...mapActions(['fetchBarChartData', 'fetchDistinctTopics', 'fetchDistinctArticles']),
    ...mapMutations(['setBarChartMode', 'setBarChartData', 'sortBarChart', 'setSelectedRootTopic', 'setBarChartCurrentPage']),
    setPagination() {
          if (this.selectedTopic == 'Topic')
            var res = this.fetchDistinctTopics()
          else
            var res = this.fetchDistinctArticles()
          res.then((value) => {
            this.currentLength = this.getSelectedRootTopic[1] ? Math.ceil((value.data.data-1) / 4) : Math.ceil(value.data.data / 5)
          })
    },
    init() {
            this.chartWidth = 300
            this.barHeight = 20
            this.groupHeight = this.barHeight * 3
            this.gapBetweenGroups = 10
            this.spaceForLabels = 110
            this.spaceForLegend = 150

            // Color scale
            this.color = d3.scaleOrdinal().range(["#59a14f", "#bab0ac", "#e15759"]);
            this.chartHeight = this.barHeight * 5 + this.gapBetweenGroups * 3;

            // scale
            this.x = d3.scaleLinear().range([0, this.chartWidth]);
            this.y = d3.scaleLinear().range([this.chartHeight + this.gapBetweenGroups, 0]);

            // axis
            this.yAxis = d3.axisLeft(this.y).tickFormat('').tickSize(0)
            this.xAxis = d3.axisBottom(this.x)

            // Specify the chart area and dimensions
            this.svg = d3.select(".groupedBarChart")
                .attr("width", this.spaceForLabels + this.chartWidth + this.spaceForLegend)

            this.g = this.svg.append("g")

            this.bars = this.svg.append("g")
                .attr("class", "bars")

		},
		updateData(data, labels) {
            var max = d3.max(data)
            var svg = d3.select(".groupedBarChart")

            this.x.domain([0, max])
            
            var bar = this.bars.selectAll(".bar").data(data, (d, i) => i)
	          var text = this.bars.selectAll(".value").data(data, (d, i) => i)
	          var label = this.bars.selectAll(".label").data(data)
            
            bar
                .transition().delay(200).duration(400)
                .attr("width", d => this.x(d))

            bar
                .exit().remove()

            bar
                .enter().append("rect")
                .attr("fill", (d,i) => this.color(i % 3))
                .attr("class", "bar")
                .attr("height", this.barHeight - 1)
                .attr("x", this.spaceForLabels)
                .attr("y", (d, i) => (i * this.barHeight + this.gapBetweenGroups * (0.5 + Math.floor(i/3))))
                .attr('row', (d, i) => Math.floor(i / 3))
                .attr("id", function() {
                    var other = svg.selectAll("#not_selected")
                    if(other.empty())
                        return 'selected'
                    else
                        return 'not_selected'
                }).on('click', function(d) {
                    var row = d3.select(this)
                    var old_id = row.attr('id')
                    var other = svg.selectAll("#not_selected")
                    
                    svg.selectAll("rect").attr('id', 'not_selected')
                    if (!other.empty() && old_id == 'selected')
                        svg.selectAll("rect").attr('id', 'selected')
                    else
                        svg.selectAll("rect[row='" + row.attr('row') + "']").attr('id', 'selected')
                })
                .transition().delay(200).duration(400)
                .attr("width", d => this.x(d))
                
            text
                .transition().delay(200).duration(400)
                .attr("x", d => {
                  if(d / max < 0.1)
                    return this.spaceForLabels + this.x(d) + this.gapBetweenGroups
                  else
                    return this.spaceForLabels + this.x(d) - this.gapBetweenGroups
                })
                .text(function(d) { return d; })
                .style("fill", (d, i) => d / max < 0.1 ? ( i % 3 == 0 ? '#59a14f' :  i % 3 == 1 ? '#bab0ac' : '#e15759' ) : 'white')

            text
                .exit().remove()
                
            text.enter().append("text")
                .attr("class", "value")
                .attr("x", d => {
                  if(d / max < 0.1)
                    return this.spaceForLabels + this.x(d) + this.gapBetweenGroups
                  else
                    return this.spaceForLabels + this.x(d) - this.gapBetweenGroups
                })
                .style("fill", (d, i) => d / max < 0.1 ? ( i % 3 == 0 ? '#59a14f' :  i % 3 == 1 ? '#bab0ac' : '#e15759' ) : 'white')
                .attr("y", (d, i) => 9 + (i * this.barHeight + this.gapBetweenGroups * (0.5 + Math.floor(i/3))))
                .attr("dy", ".35em")
                .transition().delay(200).duration(400)
                .text(d => d)
            
            label
                .exit().remove()

            label
                .text((d, i) => {
                    if (i % 3 == 1)
                        return labels[Math.floor(i / 3)]
                    else 
                        'no'
                })
                .on('click', (d, i) => {
                  if (i % 3 == 1) {
                    var l = labels[Math.floor(i / 3)]
                    this.setSelectedRootTopic([this.selectedTopic, l])
                  }
                })


            label
                .enter().append("text")
                .attr("class", "label")
                .text((d, i) => {
                    if (i % 3 == 1)
                        return labels[Math.floor(i / 3)]
                    else 
                        'no'
                })
                .attr("x", d => this.spaceForLabels - 10 )
                .attr("y", (d, i) => 15 + (i * this.barHeight + this.gapBetweenGroups * (0.5 + Math.floor(i/3))))
                .on('click', (d, i) => {
                  if (i % 3 == 1) {
                    var l = labels[Math.floor(i / 3)]
                    this.setSelectedRootTopic([this.selectedTopic, l])
                  }
                })

		}
	},
	mounted() {
    this.fetchBarChartData({})
    this.init()
    this.setPagination()
	},
	watch : {
		getBarChartData(newValue) {

        var initData = {
          labels: newValue.categories,
          series: newValue.series
        };

		    this.updateData(initData.series, initData.labels)
    },
      selectedTopic(newValue) {
        this.setSelectedRootTopic([this.selectedTopic, null])
      },
      mode(newValue) {
        this.setBarChartMode(newValue)
        this.fetchBarChartData()
      },
      getSelectedTime() {
        this.fetchBarChartData()
        this.setPagination()
      },
      getSelectedRootTopic(newValue, oldValue) {
        newValue = newValue[1]
        oldValue = oldValue[1]
        this.fetchBarChartData()

        if(!oldValue || !newValue) 
          this.setPagination()
        var chart = d3.select(".groupedBarChart")
        if(newValue != null) {
          chart.selectAll("rect").attr('id', 'not_selected')
          chart.selectAll("rect[row='" + 0 + "']").attr('id', 'selected')
        } else {
          chart.selectAll("rect").attr('id', 'selected')
        } 

    },
    getSelectedUser() {
        this.fetchBarChartData()
        this.setPagination()
      }
      ,
      getSelectedTimeSlice() {
        this.fetchBarChartData()
        this.setPagination()
      }
	  }
  }

</script>


<style>


.bar:hover {
  fill: rgb(60, 22, 165);
}

.axis--x path {
  display: none;
}

#not_selected {
  opacity: 0.4;
}

.value {
  fill: white;
  font: 12px sans-serif;
  text-anchor: end;
}

.label {
  fill: black;
  font: 14px sans-serif;
  text-anchor: start;
  cursor: pointer;
}

.label:hover {
  fill: rgb(60, 22, 165);
}
</style>
