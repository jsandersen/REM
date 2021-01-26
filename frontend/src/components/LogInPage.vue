<!-- LOGIN PAGE -->

<template>
    <v-app>
            <v-container>
                <v-layout>
                    <v-flex>
                        <v-card style="max-width: 500px" class="pa-5">

                        <v-text-field
                            :label="$t('login_user')"
                            v-model="usr"
                            required
                        ></v-text-field>

                        <v-text-field
                            :append-icon="show3 ? 'mdi-eye' : 'mdi-eye-off'"
                            :type="show3 ? 'text' : 'password'"
                            name="input-10-2"
                            :label="$t('login_pwd')"
                            v-model="pwd"
                            class="input-group--focused"
                            @click:append="show3 = !show3">
                        </v-text-field>

                        <v-row class="pl-3 pr-3">
                        <v-btn 
                            class="mr-4" 
                            counter
                            @click="login_user"> 
                            {{ $t("login") }}
                        </v-btn>
                        <v-spacer></v-spacer>
                        <div class="pt-1" style="color:#FF0000">{{ msg }}</div>
                        </v-row>

                        </v-card>
                    </v-flex>

                </v-layout>
            </v-container>
    </v-app>
</template>


<script>

import { mapGetters, mapActions, mapMutations } from "vuex";

    export default {
    data () {
      return {
        show3: false,
        pwd: '',
        usr : '', 
        msg : '',
      }
    },
    methods: {
        ...mapMutations(['setToken', 'setRole']),
        ...mapActions(['login', 'fetchComments', 'fetchModerationControllData']),
        login_user() {
            this.msg = ''
            if(this.usr && this.pwd) {
                var res = this.login({'usr' : this.usr, 'pwd' : this.pwd})
                res.then((value) => {
                var token = value.data.token
                if(value.data.token) {
                    this.setToken(token)
                    this.setRole(value.data.role == 'admin')
                    this.fetchModerationControllData();
                } else 
                    this.msg = this.$t("login_fail_msg")
                })
            } else {
                this.msg = this.$t("login_fail_msg")
            }
        },
    }
  }
</script>