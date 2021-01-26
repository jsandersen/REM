<template>
        <svg :id="id"></svg>
</template>

<script>
  import * as d3 from 'd3';
  export default {
    props: ['id', 'p_block'],
    data: () => ({
        class : 'hugo'
    }),
    methods : {
        init() {            
            this.pieChart = d3.pie().sort(null)
            this.newArc = d3.arc().innerRadius(19).outerRadius(34)

            this.fillScale = d3.scaleOrdinal(["#59a14f", "#e15759"]);

            this.svg = d3.select("#" + this.id)
                .append("g")
                .attr("transform", "translate(65, 35)")
        },
        updateData() {
            if(this.p_block != null) {
                var p = Math.round(this.p_block * 100)
                var pieData = this.pieChart([100 - p, p])
            } else {
                var pieData = this.pieChart([50, 50])
            }
            
            var path = this.svg.selectAll("path").data(pieData)
            
            path.transition().delay(0).duration(0)
                .attr("d", this.newArc)

            path.enter()
                .append("path")
                .attr("d", this.newArc)
                .style("fill", (d, i) => this.fillScale(i))
                .style("stroke", "black")
                .style("stroke-width", "1px")
        }
    },
    mounted() {
        this.init()
        this.updateData()
    },
    watch : {
        p_block () {
            this.updateData()
        }
    }
  }
</script>