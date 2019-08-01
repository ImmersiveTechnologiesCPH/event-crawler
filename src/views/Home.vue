<template>
  <v-container grid-list-xl fluid>
    <v-layout justify-center>
      <v-flex xs12 sm6 md4>
        <v-autocomplete
          v-model="selected"
          :items="items"
          label="Location"
          persistent-hint
          prepend-icon="search"
          color="grey darken-3"
        ></v-autocomplete>
      </v-flex>
    </v-layout>
    <v-layout justify-center v-if="loading">
      <v-progress-circular
        :size="70"
        :width="7"
        color="grey darken-3"
        indeterminate
      ></v-progress-circular>
    </v-layout>
    <v-layout v-if="events != null" row wrap>
      <v-flex xs12>
        <div class="text-xs-center">
          <v-chip label>{{ pagination.object_count }} events found</v-chip>
          <v-chip label> Page {{ pagination.page_number }} | {{ pagination.page_count }}</v-chip>
          <v-chip @click="payingFilter = !payingFilter" label>{{ payingFilter ? 'Only paying' : 'All' }}</v-chip>
        </div>
      </v-flex>
      <v-flex v-for="(event, index) in (payingFilter ? events.filter(e => !isFree(e)) : events)" :key="index" xs12 md8 offset-md2>
        <v-card :dark="isFree(event)">
          <v-card-title primary-title>
            <div>
              <h3 class="headline mb-0">{{ event.name.text }}</h3>
              <p>
                {{ moment(event.start.local, 'YYYY-MM-DDTh:mm:ss').format('Do MMM YYYY - hh:mma') }}<br>
                {{ moment(event.end.local, 'YYYY-MM-DDTh:mm:ss').format('Do MMM YYYY - hh:mma') }}
              </p>
              <span v-for="(pricing, index) in event.ticket_classes.filter( p => p.category == 'admission' )" :key="index">
                <h4>{{ pricing.name }}<v-btn style="cursor: default;" small :color="colorTable[pricing.on_sale_status]">{{ pricing.on_sale_status.split('_').join(' ') }}</v-btn></h4> 
                <p>{{ pricing.free ? "Free" : (pricing.cost != undefined ? pricing.cost.display : 'Price not available')}}</p>
              </span>
            </div>
          </v-card-title>
          <v-card-actions>
            <v-btn dark :href="event.url" target="_blank" color="indigo lighten-1">Go to event page</v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
      <v-flex xs12>
        <div class="text-xs-center">
          <v-chip label> Page {{ pagination.page_number }} | {{ pagination.page_count }}</v-chip>
          <br>
          <v-btn v-if="pagination.page_number > 1" @click="get_events(selected, pagination.page_number - 1)" fab dark medium color="indigo lighten-1"><v-icon dark>keyboard_arrow_left</v-icon></v-btn>
          <v-btn v-if="pagination.page_number < pagination.page_count" @click="get_events(selected, pagination.page_number + 1)" fab dark  medium color="indigo lighten-1"><v-icon dark>keyboard_arrow_right</v-icon></v-btn>
        </div>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import axios from 'axios'
import moment from 'moment'
export default {
  name: 'Home',
  data() {
    return {
      items: ['Amsterdam', 'Barcelone', 'Berlin', 'Brussels', 'Copenhagen', 'Dublin', 'Edinburgh', 'Helsinki', 'London', 'Madrid', 'Oslo', 'Paris', 'Stockholm'],
      colorTable: {
        'UNAVAILABLE': 'warning',
        'AVAILABLE': 'success',
        'SOLD_OUT': 'error',
        'NOT_YET_ON_SALE': 'info'
      },
      selected: null,
      events: null,
      pagination: null,
      loading: false,
      payingFilter: false
    }
  },
  watch: {
    selected() {
      this.get_events(this.selected, 1)
    }
  },
  methods: {
    get_events(location, page) {
      // Send a request to backend to get events data from the Eventbrite API
      this.events = null
      this.loading = true
      axios
      .get('http://127.0.0.1:5000/events/' + location.toLowerCase() + '/' + page)
      .then(response => {
        this.loading = false
        // this.events = response.data.events
        this.pagination = response.data.pagination
        this.events = response.data.events.sort((e1, e2) => moment(e1.start.local, 'YYYY-MM-DDTh:mm:ss').isAfter(moment(e2.start.local, 'YYYY-MM-DDTh:mm:ss')) ? 1 : -1)
      })
    },
    isFree(event) {
      // Return whether this event sells paying ticket
      return event.ticket_classes.filter( p => !p.free ).length == 0
    }
  }
}
</script>

<style>

</style>
