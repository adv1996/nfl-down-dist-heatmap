<template>
  <v-app>
    <v-app-bar app>
      <v-toolbar-title class="headline text-uppercase">
        <span>NFL Down and Distance HeatMap</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
    </v-app-bar>

    <v-content>
        <v-container>
          <v-row
            no-gutters
          >
            <v-col md="4">
              <heat-map playerId="aaronRodgers12345"/>
            </v-col>
            <v-col md="4">
              <heat-map playerId="aaronRodgers12346"/>
            </v-col>
          </v-row>
        </v-container>
    </v-content>
  </v-app>
</template>

<script>
import HeatMap from './components/HeatMap.vue';

export default {
  name: 'App',
  components: {
    HeatMap,
  },
  data: () => ({
    //
  }),
};
</script>
