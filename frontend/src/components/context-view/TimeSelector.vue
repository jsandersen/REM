<template>
          <div class="mt-7">
          <v-flex style="width: 10em;">
                <v-select 
                    outlined
                    :items="items"
                    v-model="mode"
                    dense
                    :label="$t('group')"
                ></v-select>
              </v-flex>
          </div>
</template>

<script>
import { mapGetters, mapMutations, mapActions } from 'vuex'

  export default {
    data: () => ({
            items : [
                {text: 'Minutes', value: 'min', disabled: true}, 
                {text: 'Hours', value: 's', disabled: true}, 
                {text: 'Days', value: 't', disabled: false}, 
                //{text: 'Monaten', value: 'm', disabled: false},
                //{text: 'Jahren', value: 'y', disabled: false}
            ]
    }),
    computed: {
      ...mapGetters(['getSelectedTimeFrame', 'getSelectedTime']),
      mode: {
        get() {
          return this.getSelectedTimeFrame;
        },        
        set(value) {
          this.setSelectedTimeFrame(value)
        }
      }
    },
	methods : {
    		...mapActions(['fetchTimechartData']),
        ...mapMutations(['setSelectedTimeFrame', 'setSelectedTime']),
    },
    watch : {
        getSelectedTime(value) {
            var old_ = this.getSelectedTimeFrame

            switch (value) {
                case '1Std':
                    this.items[0].disabled = false
                    this.items[1].disabled = true
                    this.items[2].disabled = true
                    //this.items[3].disabled = true
                    //this.items[4].disabled = true

                    this.setSelectedTimeFrame(this.items[0].value)
                    break;
                case '4Std':
                    this.items[0].disabled = false
                    this.items[1].disabled = false
                    this.items[2].disabled = true
                    //this.items[3].disabled = true
                    //this.items[4].disabled = true

                    this.setSelectedTimeFrame(this.items[0].value)
                    break;
                case '24Std':
                    this.items[0].disabled = true
                    this.items[1].disabled = false
                    this.items[2].disabled = false
                    //this.items[3].disabled = true
                    //this.items[4].disabled = true

                    this.setSelectedTimeFrame(this.items[1].value)
                    break;
                case '72Std':
                    this.items[0].disabled = true
                    this.items[1].disabled = false
                    this.items[2].disabled = false
                    //this.items[3].disabled = true
                    //this.items[4].disabled = true

                    this.setSelectedTimeFrame(this.items[1].value)
                    break;
                case '1Woche':
                    this.items[0].disabled = true
                    this.items[1].disabled = true
                    this.items[2].disabled = false
                    //this.items[3].disabled = true
                    //this.items[4].disabled = true

                    this.setSelectedTimeFrame(this.items[2].value)
                    break;
                case 'all':
                    this.items[0].disabled = true
                    this.items[1].disabled = true
                    this.items[2].disabled = false
                    //this.items[3].disabled = false
                    //this.items[4].disabled = false

                    this.setSelectedTimeFrame(this.items[2].value)
                    break;
                default:
                     this.items[0].disabled = true
                     this.items[1].disabled = true
                     this.items[2].disabled = true
                     //this.items[3].disabled = true
                     //this.items[4].disabled = true                 
            }

            var new_ = this.getSelectedTimeFrame

            if (old_.text == new_.text) {
                this.fetchTimechartData()
            }
        }
    }
  }
</script>