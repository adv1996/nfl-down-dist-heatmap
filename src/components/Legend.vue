<template>
  <v-card
    class="pt-2"
    tile
  >
    <svg id="legend"/>
  </v-card>
</template>

<script>
  // import _ from 'lodash';
  import * as d3 from 'd3';
  export default {
    data() {
      return {
        height: 0,
        width: 0,
        margin: {top: 30, right: 20, bottom: 20, left: 20},
        dataMapping: {
          "1st and <=5": {
            "start_angle": -Math.PI / 2,
            "end_angle": -Math.PI / 4,
            "innerRadius": 25,
            "outerRadius": 60
          },
          "1st and 6+": {
            "start_angle": -Math.PI / 2,
            "end_angle": -Math.PI / 4,
            "innerRadius": 60,
            "outerRadius": 110
          },
          "2nd and <=5": {
            "start_angle": -Math.PI / 4,
            "end_angle": 0,
            "innerRadius": 25,
            "outerRadius": 60
          },
          "2nd and 6+": {
            "start_angle": -Math.PI / 4,
            "end_angle": 0,
            "innerRadius": 60,
            "outerRadius": 110
          },
          "3rd and <=5": {
            "start_angle": 0,
            "end_angle": Math.PI / 4,
            "innerRadius": 25,
            "outerRadius": 60,
          },
          "3rd and 6+": {
            "start_angle": 0,
            "end_angle": Math.PI / 4,
            "innerRadius": 60,
            "outerRadius": 110
          },
          "4th and <=5": {
            "start_angle": Math.PI / 4,
            "end_angle": Math.PI / 2,
            "innerRadius": 25,
            "outerRadius": 60
          },
          "4th and 6+": {
            "start_angle": Math.PI / 4,
            "end_angle": Math.PI / 2,
            "innerRadius": 60,
            "outerRadius": 110
          },
        },
        labelMapping: {
          "First": {
            "start_angle": -Math.PI / 2,
            "end_angle": -Math.PI / 4,
            "innerRadius": 120,
            "outerRadius": 132,
            "name": "1st"
          },
          "Second": {
            "start_angle": -Math.PI / 4,
            "end_angle": 0,
            "innerRadius": 120,
            "outerRadius": 132,
            "name": "2nd"
          },
          "Third": {
            "start_angle": 0,
            "end_angle": Math.PI / 4,
            "innerRadius": 120,
            "outerRadius": 132,
            "name": "3rd Down"
          },
          "Fourth": {
            "start_angle": Math.PI / 4,
            "end_angle": Math.PI / 2,
            "innerRadius": 120,
            "outerRadius": 132,
            "name": "4th"
          },
        },
        heatMapColors: ['#f7fcf5','#e5f5e0','#c7e9c0','#a1d99b','#74c476','#41ab5d','#238b45']
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
        let scale = d3.scaleLinear()
          .domain([0, 130])
          .range([0, this.height / 2])

        let height = this.height
        let width = this.width
        let horizontalCenter = width / 4
        let verticalCenter = height / 2
        let svg = d3.select('#legend')
          .attr('width', width)
          .attr('height', height)
        let legendColors = ['white','#f7fcf5','#e5f5e0','#c7e9c0','#a1d99b','#74c476','#41ab5d','#238b45']
        let xScale = d3.scaleLinear()
          .domain([0, this.heatMapColors.length])
          .range([0, width - 60])
        let baseColors = 170

        svg.append('text')
          .attr('x', width / 2)
          .attr('y', baseColors)
          .text('Completion %')
          .attr('text-anchor', 'middle')
          .attr('class', 'attempts')

        svg.append('text')
          .attr('x', xScale(1))
          .attr('y', baseColors + 17)
          .text('0%')
          .attr('text-anchor', 'end')
          .attr('class', 'attempts')
        
        svg.append('text')
          .attr('x', width - 30)
          .attr('y', baseColors + 17)
          .text('100%')
          .attr('text-anchor', 'start')
          .attr('class', 'attempts')
        // create legend
        svg.append('g')
          .attr('class', 'legends')
          .selectAll('bars')
          .data(this.heatMapColors)
          .enter().append('rect')
            .attr('x', (d, i) => {
              return xScale(i) + width / 8
            })
            .attr('y', baseColors + 6)
            .attr('width', 23)
            .attr('height', 15)
            .attr('fill', (d) => {return d})
            .attr('stroke', 'black')

        const g = svg.append('g')
          .attr('transform', "translate(" + horizontalCenter + "," + (verticalCenter / 2 + 30) + ")")
          .attr('class', 'main_group')

        g.selectAll('legendDowns')
          .data(Object.keys(this.dataMapping))
          .enter().append('path')
          .attr("transform", "translate(" + horizontalCenter + ", " + verticalCenter / 2 + ")")
          .attr("d", d3.arc()
            .innerRadius((d) => {
              return scale(this.dataMapping[d].innerRadius)
            })
            .outerRadius((d) => {
              return scale(this.dataMapping[d].outerRadius)
            })
            .startAngle((d) => this.dataMapping[d].start_angle)
            .endAngle((d) => this.dataMapping[d].end_angle)
          )
          .attr('stroke', 'black')
          .attr('fill', (d,i) => legendColors[i]);

        g.selectAll('labelAreas')
          .data(Object.keys(this.labelMapping))
          .enter()
          .append('text')
            .attr('x', (d) => {
              let arc = d3.arc()
                .innerRadius(scale(this.labelMapping[d].innerRadius))
                .outerRadius(scale(this.labelMapping[d].outerRadius))
                .startAngle(this.labelMapping[d].start_angle)
                .endAngle(this.labelMapping[d].end_angle)
              return arc.centroid()[0] + horizontalCenter - 7
            })
            .attr('y', (d) => {
              let arc = d3.arc()
                .innerRadius(scale(this.labelMapping[d].innerRadius))
                .outerRadius(scale(this.labelMapping[d].outerRadius))
                .startAngle(this.labelMapping[d].start_angle)
                .endAngle(this.labelMapping[d].end_angle)
              return arc.centroid()[1] + verticalCenter / 2 + 8.5
            })
            .text((d) => this.labelMapping[d].name)
            .attr('class', 'attempts')

        g.append('text')
          .attr('x', 18)
          .attr('y', horizontalCenter + 12)
          .text('<=5')
          .attr('text-anchor', 'middle')
          .attr('class', 'attempts')
        
        g.append('text')
          .attr('x', -15)
          .attr('y', horizontalCenter + 12)
          .text('6+')
          .attr('text-anchor', 'middle')
          .attr('class', 'attempts')
        
        let baseShift = 87
        g.append('text')
          .attr('x', baseShift)
          .attr('y', horizontalCenter + 12)
          .text('<=5')
          .attr('text-anchor', 'middle')
          .attr('class', 'attempts')
        
        g.append('text')
          .attr('x', baseShift + 45)
          .attr('y', horizontalCenter + 12)
          .text('6+ yards')
          .attr('text-anchor', 'middle')
          .attr('class', 'attempts')
        
        g.append('text')
          .attr('x', width / 4 + 5)
          .attr('y', -53)
          .attr('text-anchor', 'middle')
          .text("LEGEND")
          .attr('class', 'title')
      },
    },
  }
</script>

<style lang="scss" scoped>

</style>