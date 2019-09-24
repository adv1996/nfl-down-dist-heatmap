<template>
  <v-card
    tile
    outlined
    class="pt-2"
  >
    <svg :id="playerId"/>
  </v-card>
</template>

<script>
  /* eslint-disable */
  import _ from 'lodash';
  import * as d3 from 'd3';
  import Players from '../data/playerData.json';

  export default {
    props: ['playerId', 'stats', 'sleeperId'],
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
            "outerRadius": 120
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
            "outerRadius": 120
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
            "outerRadius": 120
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
            "outerRadius": 120
          },
        },
        labelMapping: {
          "First": {
            "start_angle": -Math.PI / 2,
            "end_angle": -Math.PI / 4,
            "innerRadius": 120,
            "outerRadius": 140,
            "name": "1st"
          },
          "Second": {
            "start_angle": -Math.PI / 4,
            "end_angle": 0,
            "innerRadius": 120,
            "outerRadius": 140,
            "name": "2nd"
          },
          "Third": {
            "start_angle": 0,
            "end_angle": Math.PI / 4,
            "innerRadius": 120,
            "outerRadius": 140,
            "name": "3rd"
          },
          "Fourth": {
            "start_angle": Math.PI / 4,
            "end_angle": Math.PI / 2,
            "innerRadius": 120,
            "outerRadius": 140,
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
        let data = Object.keys(Players['players'][this.playerId]["down_dist"]);
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
        let legendColors = ['white','#ffffcc','#ffeda0','#fed976','#feb24c','#fd8d3c','#fc4e2a','#e31a1c']
        let xScale = d3.scaleLinear()
          .domain([0, this.heatMapColors.length])
          .range([0, 6 * width / 8])

        const g = svg.append('g')
          .attr('transform', "translate(" + horizontalCenter + "," + (verticalCenter / 2 + 30) + ")")
          .attr('class', 'main_group')

        g.selectAll('downs')
          .data(data)
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
          .attr('fill', (d) => {
            if (Players['players'][this.playerId]["down_dist"][d]['ATT'] == 0) {
              return 'white'
            }
            return colors(Players['players'][this.playerId]["down_dist"][d]['CMP%'])
          });
        
        g.selectAll('labels')
          .data(data)
          .enter().append('text')
          .attr('x', (d) => {
            let arc = d3.arc()
              .innerRadius(scale(this.dataMapping[d].innerRadius))
              .outerRadius(scale(this.dataMapping[d].outerRadius))
              .startAngle(this.dataMapping[d].start_angle)
              .endAngle(this.dataMapping[d].end_angle)
            let centroid = arc.centroid()
            return centroid[0] + horizontalCenter - 10
          })
          .attr('y', (d) => {
            let arc = d3.arc()
              .innerRadius(scale(this.dataMapping[d].innerRadius))
              .outerRadius(scale(this.dataMapping[d].outerRadius))
              .startAngle(this.dataMapping[d].start_angle)
              .endAngle(this.dataMapping[d].end_angle)
            let centroid = arc.centroid()
            return centroid[1] + verticalCenter / 2 + 5
          })
          .text((d) => {
            let completions = Players['players'][this.playerId]["down_dist"][d]['CMP']
            let attempts = Players['players'][this.playerId]["down_dist"][d]['ATT']
            return completions + "/" + attempts
          })
          .attr('class', 'attempts')

        g.append('image')
          .attr('xlink:href', (d) => {
            return 'https://sleepercdn.com/content/nfl/players/thumb/' + this.sleeperId + '.jpg'
          })
          .attr('width', 50)
          .attr('height', 50)
          .attr('x', (d) => width / 8 + 1)
          .attr('y', (d) => 24)
        let displayNames = this.playerId.split('-')
        let name = displayNames[0] + " " + displayNames[1]

        g.append('text')
          .attr('x', width / 4 + 5)
          .attr('y', -53)
          .attr('text-anchor', 'middle')
          .text(name.toLocaleUpperCase())
          .attr('class', 'title')
        
        let sl = ['Yards', 'Sacks', 'Completions', 'Attempts', 'Touchdowns', 'Interceptions']
        g.selectAll('stats')
          .data(this.stats)
          .enter()
          .append('text')
          .attr('x', (d,i) => {
            if (i % 2 == 0) {
              return -20
            }
            return width / 4 + 20
          })
          .attr('y', (d, i) => {
            if (i % 2 == 0) {
              return 20 + this.margin.top * 2 + i * 7
            }
            return 20 + this.margin.top * 2 + i * 7 - 7
          })
          .attr('text-anchor', 'start')
          .text((d, i) => sl[i] + ": " + d)
          .attr('class', 'attempts')
      },
    },
  }
</script>

<style>

.attempts {
  font-size: .55em
}
</style>