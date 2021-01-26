<template>
    <div>
      <v-progress-circular
        :rotate="360"
        :size="40"
        :width="10"
        :value="pro"
        color="white"
      >
      {{ value }}
    </v-progress-circular>
    </div>
</template>

<script>
import { mapActions } from 'vuex'

  export default {
    data: () => ({
       interval: {},
        value: 0,
        p : 0,
        time: 30,
    }),
    computed : {
        pro() {
            return Math.round(this.p)
        }
    },
    methods :{
         ...mapActions(['fetchTimechartData', 'fetchBarChartData', 'fetchBarChartData2']),
        onTimer() {
            console.log('Update')
            this.fetchTimechartData()
            this.fetchBarChartData({page:1})
            this.fetchBarChartData2({page:1})
        }
    },
    mounted () {
      this.interval = setInterval(() => {
        if (this.value === this.time) {
            this.p = 0
            this.onTimer()
          return (this.value = 0)
        }
        this.value += 1
        this.p += 3.33
      }, 1000)
    },
  }
</script>







