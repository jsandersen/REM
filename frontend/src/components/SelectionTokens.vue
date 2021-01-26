<template>

  <div style="margin-left: 0.5em;">
    <i v-if="!chip_topic && !chip_time_span && !chip_user && !chip_time_slice">
      {{ $t('none') }}
    </i>
    <v-chip
      v-if="chip_time_span"
      class="ma-2 time_span"
      close
      dense
      @click:close="chip_time_span = false"
    >
    {{ getSelectedTime.replace(/\D/g,'') + ' ' + $t('abv_hour') }}
    </v-chip>

    <v-chip
      v-if="chip_topic"
      class="ma-2 root_topic"
      close
      dense
      @click:close="chip_topic = false"
    >
    {{ getSelectedRootTopic[1] }}
    </v-chip>

    <v-chip
      v-if="chip_user"
      class="ma-2 user"
      close
      dense
      @click:close="chip_user = false"
    >
    {{ getSelectedUser }}
    </v-chip>

    <v-chip
      v-if="chip_time_slice"
      class="ma-2 time_slice"
      close
      dense
      @click:close="chip_time_slice = null"
    >
    {{ getSelectedTimeSlice }}
    </v-chip>

  </div>

</template>

<script>
  import { mapGetters, mapMutations } from 'vuex'

  export default {
    computed: {
      ...mapGetters(['getSelectedRootTopic', 'getSelectedTime', 'getSelectedUser', 'getSelectedTimeSlice']),
      chip_topic: {
        get() {
          return this.getSelectedRootTopic[1] != null;
        },        
        set(value) {
          this.setSelectedRootTopic([this.getSelectedRootTopic[0], null])
        }
      },
      chip_time_span: {
        get() {
          return this.getSelectedTime != '72Std';
        },        
        set(value) {
          this.setSelectedTime('72Std')
        }
      },
      chip_user : {
        get() {
          return this.getSelectedUser != null;
        },        
        set(value) {
          this.setSelectedUser(null)
        }
      },
      chip_time_slice : {
          get() {
          return this.getSelectedTimeSlice != null;
        },        
        set(value) {
          this.setSelectedTimeSlice(null)
        }
      }
    },
    methods: {
      ...mapMutations(['setSelectedRootTopic', 'setSelectedTime', 'setSelectedUser', 'setSelectedTimeSlice', 'setArticle'])
    },
  }
</script>