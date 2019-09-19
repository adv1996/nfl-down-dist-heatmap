<template>
  <v-app>
    <v-app-bar app>
      <v-toolbar-title class="headline text-uppercase">
        <span>NFL Down and Distance HeatMap (Weeks 1 - 2)</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
    </v-app-bar>

    <v-content>
        <v-container fluid>
          <v-row
            no-gutters
            align="center"
            justify="center"
            class="grey lighten-5"
          >
            <v-col
              md="1"
            >
              <Legend/>
            </v-col>
            <v-col
              md="1"
              v-for="player in players"
              :key="player.name"
            >
              <heat-map :playerId="player.name" :stats="[player.yards, player.sacks, player.completions, player.attempts, player.tds, player.interceptions]" :sleeperId="player.sleeperId"/>
            </v-col>
          </v-row>
        </v-container>
    </v-content>
  </v-app>
</template>

<script>
import HeatMap from './components/HeatMap.vue';
import Legend from './components/Legend.vue'
import Players from './data/playerData.json';
import _ from 'lodash';

export default {
  name: 'App',
  components: {
    HeatMap,
    Legend,
  },
  data() {
    return {
      players: [],
      fields: [
        "1st and <=5",
        "2nd and <=5",
        "3rd and <=5",
        "4th and <=5",
        "1st and 6+",
        "2nd and 6+",
        "3rd and 6+",
        "4th and 6+"
      ]
    }
  },
  mounted () {
    this.players = Object.keys(Players["players"]);
    let sortedPlayers = _.map(_.orderBy(_.map(this.players, (d) => {
      return {
        name: d,
        yards: this.getTotals('YDS', d),
        tds: this.getTotals('TD', d),
        sacks: this.getTotals('SACK', d),
        attempts: this.getTotals('ATT', d),
        completions: this.getTotals('CMP', d),
        sleeperId: Players["players"][d]["sleeper_id"],
        interceptions: this.getTotals('INT', d),
      }
    }), ['yards'], ['desc']))
    this.players = sortedPlayers;
  },
  methods: {
    getTotals(stat, d) {
      let total = 0
      this.fields.forEach((f) => {
        if (Players["players"][d]["down_dist"][f]) {
          total = total + Players["players"][d]["down_dist"][f][stat]
        }
      })
      return total
    },
  },
};
</script>
