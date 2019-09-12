<template>
  <v-card :height="height">
    <svg :id="playerId"/>
  </v-card>
</template>

<script>
  /* eslint-disable */
  import _ from 'lodash';
  import * as d3 from 'd3';
  import Players from '../data/sample.json';

  export default {
    props: ['playerId'],
    data() {
      return {
        height: 0,
        width: 0,
        margin: {top: 20, right: 20, bottom: 20, left: 20},
        dataMapping: {
          "1st and <=5": {
            "start_angle": -Math.PI / 2,
            "end_angle": -Math.PI / 4
          },
          "1st and 6+": {
            "start_angle": -Math.PI / 2,
            "end_angle": -Math.PI / 4
          },
          "2nd and <=5": {
            "start_angle": -Math.PI / 4,
            "end_angle": 0
          },
          "2nd and 6+": {
            "start_angle": -Math.PI / 4,
            "end_angle": 0
          },
          "3rd and <=5": {
            "start_angle": 0,
            "end_angle": Math.PI / 4
          },
          "3rd and 6+": {
            "start_angle": 0,
            "end_angle": Math.PI / 4
          },
          "4th and <=5": {
            "start_angle": Math.PI / 4,
            "end_angle": Math.PI / 2
          },
          "4th and 6+": {
            "start_angle": Math.PI / 4,
            "end_angle": Math.PI / 2
          },
        },
        heatMapColors: ['#ffffcc','#ffeda0','#fed976','#feb24c','#fd8d3c','#fc4e2a','#e31a1c','#b10026']
      }
    },
    mounted () {
      this.setDimensions()
      this.initGraph()
    },
    methods: {
      setDimensions() {
        this.width = this.$el.offsetWidth
        this.height = this.$el.offsetWidth
      },
      initGraph() {
        let data = Object.keys(Players['players'][this.playerId]);
        let scale = d3.scaleLinear()
          .domain([0, 130])
          .range([0, this.height / 2])

        let colors = d3.scaleQuantize([0, 100], this.heatMapColors)
        let height = this.height
        let width = this.width
        let horizontalCenter = width / 4
        let verticalCenter = height / 2
        let svg = d3.select('#' + this.playerId)
          .attr('width', width)
          .attr('height', height)
        const g = svg.append('g')
          .attr('transform', "translate(" + horizontalCenter + "," + verticalCenter + ")")
          .attr('class', 'main_group')

        g.selectAll('downs')
          .data(data)
          .enter().append('path')
          .attr("transform", "translate(" + horizontalCenter + ", " + verticalCenter / 2 + ")")
          .attr("d", d3.arc()
            .innerRadius((d) => {
              return scale(this.getInnerDistance(d))
            })
            .outerRadius((d) => {
              return scale(this.getOuterDistance(d))
            })
            .startAngle((d) => this.dataMapping[d].start_angle)
            .endAngle((d) => this.dataMapping[d].end_angle)
          )
          .attr('stroke', 'black')
          .attr('fill', (d) => colors(Players['players'][this.playerId][d]['completionPercentage']));
      },
      getInnerDistance(downDist) {
        let base = 25  // make base size responsive
        let superbase = 60
        if (downDist.includes("5")) {
          return base
        } else {
          let yards = Players['players'][this.playerId][downDist]['previousYards']
          // return base + yards
          return superbase
        }
      },
      getOuterDistance(downDist) {
        let base = 25
        let superbase = 60
        let supersuperbase = 120
        let yards = Players['players'][this.playerId][downDist]['yards']
        let previousYards = Players['players'][this.playerId][downDist]['previousYards']
        if (downDist.includes("5")) {
          // return base + yards
          return superbase
        } else {
          // return base + yards + previousYards
          return supersuperbase
        }
      }
    },
  }
</script>

<style lang="scss" scoped>

</style>