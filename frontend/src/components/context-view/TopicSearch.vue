<template>
  <div style="width: 13em;">
          <v-autocomplete
            outlined
            v-model="value"
            :items="getRootTopics"
            dense
            clearable 
            :label="getLabel"
            hide-details
          ></v-autocomplete>
  </div>
</template>

<script>
  import { mapGetters, mapActions, mapMutations } from 'vuex'

  export default {
    computed: {
      ...mapGetters(['getRootTopics','getSelectedRootTopic']),
      getLabel() {
        if (this.getSelectedRootTopic[0] == 'Topic')
          return this.$t('topic_filter')
        if (this.getSelectedRootTopic[0] == 'Article')
          return this.$t('active_filter')
      },
      value: {
        get() {
          return this.getSelectedRootTopic[1];
        },
        set(value) {
          this.setSelectedRootTopic([this.getSelectedRootTopic[0], value])
        }
      }
    },
    methods: {
      ...mapActions(['fetchRootTopics']),
      ...mapMutations(['setSelectedRootTopic'])
    },
    watch: {
      getSelectedRootTopic() {
        this.fetchRootTopics()
      }
    },
    created() {
      this.fetchRootTopics()
    }
  }
</script>