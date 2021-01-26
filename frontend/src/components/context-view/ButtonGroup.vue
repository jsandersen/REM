<template>
  <div class="text-center">
      <v-btn-toggle
          outlined
          v-model="mode"
          tile
          group
          mandatory
          dense
        >
        <v-btn v-for="val in values" :key="val.text" :value="val.value">
          {{ val.text }}
        </v-btn>


        </v-btn-toggle>

  </div>

</template>

<script>
  import { mapGetters, mapMutations } from 'vuex'

  export default {
      data: () => ({
        values : [
                {text: '1 H', value: '1Std',}, 
                {text: '4 H', value: '4Std',}, 
                {text: '24 H', value: '24Std'},
                {text: '72 H', value: '72Std'}, 
             //   {text: '1 W', value: '1Woche'},
             //   {text: 'Gesamtheit', value: 'all'}
        ]
      }),
    computed: {
      ...mapGetters(['getSelectedTime']),
      mode: {
        get() {
          return this.getSelectedTime;
        },        
        set(value) {
          this.setSelectedTime(value)
        }
      }
    },
    methods: {
      ...mapMutations(['setSelectedTime'])
    },
  }
</script>