<template>
  <v-app>
    <v-app-bar app>
      <v-toolbar-title class="headline text-uppercase">
        <span>NFL Down and Distance HeatMap</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
    </v-app-bar>

    <v-content>
        <v-container fluid>
          <v-row
            no-gutters
          >
            <v-col
              md="2"
              v-for="player in players"
              :key="player"
            >
              <heat-map :playerId="player"/>
            </v-col>
          </v-row>
        </v-container>
    </v-content>
  </v-app>
</template>

<script>
import HeatMap from './components/HeatMap.vue';
import Players from './data/playerData.json';

export default {
  name: 'App',
  components: {
    HeatMap,
  },
  data() {
    return {
      players: Object.keys(Players["players"])
    }
  },
  mounted () {
    this.players = Object.keys(Players["players"]);
  },
};
</script>
