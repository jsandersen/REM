<template>
    <svg class='progress' width="300" height="50"></svg>
</template>


<script>
  import * as d3 from 'd3';
  import { mapGetters } from 'vuex'
  export default {
    data: () => ({
        color : ["#e15759", "#59a14f"],
    }),
    mounted() {
        this.init()
        this.updateData(this.getComments[this.getSelectedCommentId])
    },
    	computed: {
            ...mapGetters(['getComments', 'getSelectedCommentId']),
      comment() {
          if(this.getComments.length == 0) {
              return []
          } else {
            return this.getComments[this.getSelectedCommentId]
          }
        },
    },
    watch : {
        comment(newValue) {
            this.updateData(newValue)
        }
    },
    methods : {
        init() {
            this.svg = d3.select(".progress")
            var chartWidth = 300
            this.xScale = d3.scaleLinear().rangeRound([0, chartWidth]).domain([0, 100])
        },
        updateData(data) {
            
            if(data != null && data.ml != null)
                i =  Math.round(data.ml.p_blocked * 100)
            else
                i = Math.round(Math.random() * 100)

            var data = [
                {
                   'key' : 'offline',
                    'value' : i,
                },
                {
                    'key' : 'online',
                    'value' : 100 -i, 
                }
            ]

            for (var i = 0; i < data.length; i++) {
            if(i == 0)
                data[i]['x'] = 0
            else
                data[i]['x'] = data[i-1]['value']
            }

            var bar = this.svg
                .selectAll("rect")
                .data(data)

            var text = this.svg
                .selectAll("text")
                .data(data)

            bar
                .transition().delay(0).duration(200)
                .attr("x", d => this.xScale(d.x))
                .attr("width", d => this.xScale(d.value))

            bar
                .enter().append("rect")
                .attr("class", d => d.key )
                .attr("x", d => this.xScale(d.x))
                .attr("y", d => 15)
                .attr("width", d => this.xScale(d.value))
                .attr("height", "20px" )
                .attr("fill", (d, i) => this.color[i])

            text
                .transition().delay(0).duration(200)
                .attr("x", d => this.xScale(d.x + ( d.value / 2)) - 14)
                .text((d, i) => {
                    if(d.value > 8)
                        return d.value + '%'
                })
                

            text
                .enter().append("text")
                .attr("class", d => d.key )
                .attr("x", d => this.xScale(d.x + ( d.value / 2)) - 14)
                .attr("y", d => 30)
                .text((d, i) => {
                    if(d.value > 8)
                        return d.value + '%'
                })
        }
    }
  }
</script>

<style scoped>

</style>