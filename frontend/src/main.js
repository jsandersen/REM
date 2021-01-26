import Vue from 'vue'
import VueI18n from 'vue-i18n'
import App from './App.vue'
import store from './store'
import vuetify from './plugins/vuetify';
import 'roboto-fontface/css/roboto/roboto-fontface.css'
import '@mdi/font/css/materialdesignicons.css'
import text from './i18n/text'

const messages = text.messages

Vue.config.productionTip = false
Vue.use(VueI18n)

const i18n = new VueI18n({
  locale: 'en', // change language {en, de}
  messages,
})

new Vue({
  i18n,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')