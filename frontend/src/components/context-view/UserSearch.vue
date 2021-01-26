<template>
  <div style="width: 13em;">
          <v-autocomplete
            outlined
            v-model="value"
            :items="getUserNames"
            :search-input.sync="search"
            dense
            clearable
            hide-no-data
            :label="$t('user_filter')"
            hide-details
          ></v-autocomplete>
          
  </div>
</template>

<script>
  import { mapGetters, mapActions, mapMutations } from 'vuex'

  export default {
    data: () => ({
      search: null,
	  }),
    computed: {
      ...mapGetters(['getSelectedUser', 'getUserNames']),
      value: {
          get() {
            return  this.getSelectedUser
          },
          set(value) {
            this.setSelectedUser(value)
          }
      },
    },
    methods: {
      ...mapActions(['fetchUsers']),
      ...mapMutations(['setSelectedUser']),
    },
    watch: {
      search (val) {
        if (val) {
          this.fetchUsers({ search:val })
        }
      },
    },
  }
</script>