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
          <v-btn value="online">
            {{ $t('online') }}
          </v-btn>

          <v-btn value="unsicher">
            {{ $t('uncertain') }}
          </v-btn>

          <v-btn value="offline">
            {{ $t('offline') }}
          </v-btn>

          <v-btn value="all">
            {{ $t('all') }}
          </v-btn>

        </v-btn-toggle>

  </div>

</template>

<script>
  import { mapGetters, mapMutations } from 'vuex'

  export default {
      data: () => ({
      }),
    computed: {
      ...mapGetters(['getSelectedCommentMode']),
      mode: {
        get() {
          return this.getSelectedCommentMode;
        },        
        set(value) {
          this.setSelectedCommentModel(value)
        }
      }
    },
    methods: {
      ...mapMutations(['setSelectedCommentModel'])
    },
  }
</script>