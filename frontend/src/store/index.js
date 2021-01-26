import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios';

Vue.use(Vuex)

const VUE_APP_API_URL = 'http://localhost:5050/'

const state = {
  token: null,
  role: 'user',

  init: false,
  selected_root_topic : ['Topic', null],
  selected_time : '24Std',
  selected_comment_lid : 0,
  selectedArticle: {},
  selectedCommentsMode: 'all',
  selectedUser: null,
  selectedTimeSlice: null,
  selectedTimeFrame: 's',
  
  commentsInList : [],
  commentListSettings : {offset : 0 },

  root_topics : [],
  userNames : [],
  
  timeChart : {
    data : [],
  },
  barChart : {
    data : [],
    data2 : [],
    mode : 'unsicher',
    mode2 :  'unsicher',
    currentPage: 1,
    currentPage2: 1,
  },
  moderationControllData : {},
  selectedModerationControllSetting : {},

  sortCommentsSettingKey: 0,
  sortCommentsSettingMode : -1,
  fetchCommentsModel: false
}

const getters = {
  getToken: (state) => state.token,
  getRole: (state) => state.role,

  getInit: (state) => state.init,

  getRootTopics: (state) => state.root_topics,
  getSelectedRootTopic: (state) => state.selected_root_topic,
  getSelectedTime: (state) => state.selected_time,
  getSelectedCommentId: (state) => state.selected_comment_lid,
  getSelectedArticle: (state) => state.selectedArticle,
  getSelectedCommentMode: (state) => state.selectedCommentsMode,
  getSelectedUser: (state) => state.selectedUser,
  getSelectedTimeSlice: (state) => state.selectedTimeSlice,
  getSelectedTimeFrame: (state) => state.selectedTimeFrame,
  
  getModerationControllData: (state) => state.moderationControllData,
  getSelectedModerationControllSetting: (state) => state.selectedModerationControllSetting,

  getCommentListSettings: (state) => state.commentListSettings,

  getUserNames: (state) => state.userNames,
  getComments: (state) => state.commentsInList,

  getSortCommentsSettingMode: (state) => state.sortCommentsSettingMode,
  getSortCommentsSettingKey: (state) => state.sortCommentsSettingKey,

  getTimeChartData: (state) => state.timeChart.data,
  getBarChartData: (state) => state.barChart.data,
  getBarChartMode: (state) => state.barChart.mode,
  getBarChartData2: (state) => state.barChart.data2,
  getBarChartMode2: (state) => state.barChart.mode2,
  getBarChartCurrentPage: (state) => state.barChart.currentPage,
  getBarChartCurrentPage2: (state) => state.barChart.currentPage2,
  getFetchCommentsModel: (state) => state.fetchCommentsModel,
}

const actions = {
  async fetchRootTopics({ getters, commit }) {
    var token = getters.getToken
    var selection = getters.getSelectedRootTopic[0]
    var flag  = 0
    
    var url = VUE_APP_API_URL + '/db/articles/topics/root?'
    
    if(selection != 'Topic')
      flag  = 1
    url += "&flag=" + flag
    
    const response = await axios.get(url, { headers: { "x-access-token": `${token}` } });
    commit('setRootTopics', response.data.data)
  },
  async fetchModerationControllData({commit, getters}) {
    var token = getters.getToken
    const response = await axios.get(VUE_APP_API_URL + '/db/models/test', { headers: { "x-access-token": `${token}` } });
    commit('setModerationControllData', response.data.data)
    commit('setSelectedModerationControllSetting', response.data.data.current_point)
    commit('setInit', true)
  },
  async fetchSelectedModerationControllSetting({getters, commit}) {
    var token = getters.getToken
    const response = await axios.get(VUE_APP_API_URL + '/db/models/strategy/test', { headers: { "x-access-token": `${token}` } });
    commit('setSelectedModerationControllSetting', response.data.data.current_point)
  },
  setModerationStrategy({ getters }) {
    var token = getters.getToken
    var strategy = getters.getSelectedModerationControllSetting
    var url = VUE_APP_API_URL + '/db/models/strategy'
    var payload = {'name': 'test', 'load': strategy.load, 'acc': strategy.acc, 'eff': strategy.eff, 'unc':strategy.unc, 's_name' : strategy.name}
    const request = axios.post(url, payload, { headers: { "x-access-token": `${token}` } })
    return request
  },
  labelInctance({getters}, {id, blocked}) {
    var token = getters.getToken
    var url = VUE_APP_API_URL + '/db/labelling/label'
    var payload = {'id': id, 'blocked' : blocked}
    const request = axios.post(url, payload, { headers: { "x-access-token": `${token}` } })
    return request
  },
  login({getters}, {usr, pwd}) {
    var token = getters.getToken
    var url = VUE_APP_API_URL + '/db/auth/'
    var payload = {'usr': usr,  'pwd': pwd}
    const request = axios.post(url, payload, { headers: { "x-access-token": `${token}` } })
    return request
  },
  fetchModerationDiff({getters}, {unc_old, unc_new}) {
    var token = getters.getToken
    var url = VUE_APP_API_URL + '/db/comments/change?unc_old=' + unc_old + '&unc_new=' + unc_new
    const request = axios.get(url, { headers: { "x-access-token": `${token}` } })
    return request
  },
  fetchDistinctTopics({getters}) {
    var token = getters.getToken
    var time_slice = getters.getSelectedTimeSlice
    var timeGap = getters.getSelectedTime

    var url = VUE_APP_API_URL + '/db/comments/topics/count/distinct?'

    if (time_slice != null)
      url += "&time_slice=" + time_slice
    if(timeGap != 'all')
      url += "&time=" + timeGap

    const request = axios.get(url, { headers: { "x-access-token": `${token}` } })
    return request
  },
  fetchParentComments({getters}, {id}) {
    var token = getters.getToken

    var url = VUE_APP_API_URL + '/db/comments/parents/' + id
    const request = axios.get(url, { headers: { "x-access-token": `${token}` } })
    return request
  },
  fetchDistinctUsers({getters}) {
    var token = getters.getToken
    var time_slice = getters.getSelectedTimeSlice
    var timeGap = getters.getSelectedTime

    var url = VUE_APP_API_URL + '/db/comments/user/count/distinct?'

    if (time_slice != null)
      url += "&time_slice=" + time_slice
    if(timeGap != 'all')
      url += "&time=" + timeGap

    const request = axios.get(url, { headers: { "x-access-token": `${token}` } })
    return request
  },
  fetchDistinctArticles({getters}) {
    var token = getters.getToken
    var time_slice = getters.getSelectedTimeSlice
    var timeGap = getters.getSelectedTime

    var url = VUE_APP_API_URL + '/db/comments/article/count/distinct?'

    if (time_slice != null)
      url += "&time_slice=" + time_slice
    if(timeGap != 'all')
      url += "&time=" + timeGap

    const request = axios.get(url, { headers: { "x-access-token": `${token}` } })
    return request
  },
  fetchCommentCount({ getters } ) {
    var token = getters.getToken
    var selection = getters.getSelectedRootTopic[0]
    var topic = getters.getSelectedRootTopic[1]
    var mode = getters.getSelectedCommentMode
    var user = getters.getSelectedUser
    var time_slice = getters.getSelectedTimeSlice
    var timeGap = getters.getSelectedTime
    var unc = getters.getSelectedModerationControllSetting.unc
    var humanMode = getters.getFetchCommentsModel

    var url = VUE_APP_API_URL + '/db/comments/count?'
    switch (mode) {
      case 'unsicher':
        url += '&uncertain=1'
        break;
      case 'online':
        url += '&blocked=0&uncertain=0'
        break;
      case 'offline':
        url += '&blocked=1&uncertain=0'
        break;
    }
    if(topic !=   null)
      url += ('&topic_root=' + topic)
    if(user !=   null)
      url += ('&user_name=' + user)
    if (time_slice != null)
      url += "&time_slice=" + time_slice
    if(timeGap != 'all')
      url += "&time=" + timeGap

    var flag  = 0
    if(selection != 'Topic')
      flag  = 1
      
    url += "&flag=" + flag
    url += "&unc=" + unc
    url += "&human_mode=" + (humanMode ? 1 : 0)

    const response = axios.get(url, { headers: { "x-access-token": `${token}` } });
    return response
  },
  fetchOneComment({ getters }) {
    var token = getters.getToken
    var offset = getters.getCommentListSettings.offset
    var mode = getters.getSelectedCommentMode
    var selection = getters.getSelectedRootTopic[0]
    var topic = getters.getSelectedRootTopic[1]
    var user = getters.getSelectedUser
    var time_slice = getters.getSelectedTimeSlice
    var timeGap = getters.getSelectedTime
    var unc = getters.getSelectedModerationControllSetting.unc
    var sortKey = getters.getSortCommentsSettingKey
    var sortMode = getters.getSortCommentsSettingMode
    var humanMode = getters.getFetchCommentsModel

    var url = VUE_APP_API_URL + '/db/comments/?limit=' + 1 + '&skip=' + (offset + 3)
    switch (mode) {
      case 'unsicher':
        url += '&uncertain=1'
        break;
      case 'online':
        url += '&blocked=0&uncertain=0'
        break;
      case 'offline':
        url += '&blocked=1&uncertain=0'
        break;
    }
    if(topic !=   null)
      url += ('&topic_root=' + topic)
    if(user !=   null)
      url += ('&user_name=' + user)
    if (time_slice != null)
      url += "&time_slice=" + time_slice
    if(timeGap != 'all')
      url += "&time=" + timeGap

    var flag  = 0
    if(selection != 'Topic')
      flag  = 1
      
    url += "&flag=" + flag
    url += "&unc=" + unc
    url += "&sort_mode=" + sortMode
    url += "&sort_key=" + sortKey
    url += "&human_mode=" + (humanMode ? 1 : 0)

    const response = axios.get(url, { headers: { "x-access-token": `${token}` } });
    response.then((val) => {
        console.log(val.data.data)
        if(val.data.data.length > 0) {
          getters.getComments.push(val.data.data[0])
        }
    })

  },
  async fetchComments({ commit, getters }, {offset, limit}) {
    var token = getters.getToken
    var mode = getters.getSelectedCommentMode
    var selection = getters.getSelectedRootTopic[0]
    var topic = getters.getSelectedRootTopic[1]
    var user = getters.getSelectedUser
    var time_slice = getters.getSelectedTimeSlice
    var timeGap = getters.getSelectedTime
    var unc = getters.getSelectedModerationControllSetting.unc
    var sortKey = getters.getSortCommentsSettingKey
    var sortMode = getters.getSortCommentsSettingMode
    var humanMode = getters.getFetchCommentsModel

    var url = VUE_APP_API_URL + '/db/comments/?limit=' + limit + '&skip=' + offset
    switch (mode) {
      case 'unsicher':
        url += '&uncertain=1'
        break;
      case 'online':
        url += '&blocked=0&uncertain=0'
        break;
      case 'offline':
        url += '&blocked=1&uncertain=0'
        break;
    }
    if(topic !=   null)
      url += ('&topic_root=' + topic)
    if(user !=   null)
      url += ('&user_name=' + user)
    if (time_slice != null)
      url += "&time_slice=" + time_slice
    if(timeGap != 'all')
      url += "&time=" + timeGap
      
    var flag  = 0
    if(selection != 'Topic')
      flag  = 1
      
    url += "&flag=" + flag
    url += "&unc=" + unc
    url += "&sort_mode=" + sortMode
    url += "&sort_key=" + sortKey
    url += "&human_mode=" + (humanMode ? 1 : 0)

    const response = await axios.get(url, { headers: { "x-access-token": `${token}` } });
    commit('setComments', response.data.data)
  },
  async fetchBarChartData({ commit, getters }) {
    var page = getters.getBarChartCurrentPage
    var token = getters.getToken
    var user_name = getters.getSelectedUser
    var selection = getters.getSelectedRootTopic[0]
    var topic = getters.getSelectedRootTopic[1]
    var time_slice = getters.getSelectedTimeSlice
    var timeGap = getters.getSelectedTime
    var unc = getters.getSelectedModerationControllSetting.unc
    var mode = getters.getBarChartMode

    var url = VUE_APP_API_URL + '/db/comments/topics/root/count?sort=' + mode

    if (user_name != null)
      url += "&user_name=" + user_name
    if (topic != null)
      url += "&selected_topic=" + topic
    if (page != null)
      url += "&page=" + page
    if (time_slice != null)
      url += "&time_slice=" + time_slice
    if(timeGap != 'all')
      url += "&time=" + timeGap
    
    var flag  = 0
    if(selection != 'Topic')
      flag  = 1

    url += "&flag=" + flag
    url += "&unc=" + unc

    const response = await axios.get(url, { headers: { "x-access-token": `${token}` } });
    commit('setBarChartData', response.data.data)
  },
  async fetchBarChartData2({ commit, getters }) {
    var page = getters.getBarChartCurrentPage2
    var token = getters.getToken
    var selection = getters.getSelectedRootTopic[0]
    var topic = getters.getSelectedRootTopic[1]
    var user_name = getters.getSelectedUser
    var time_slice = getters.getSelectedTimeSlice
    var timeGap = getters.getSelectedTime
    var unc = getters.getSelectedModerationControllSetting.unc
    var mode = getters.getBarChartMode2

    var url = VUE_APP_API_URL + '/db/comments/user/count/?sort=' + mode
    if (topic != null)
      url += "&topic_root=" + topic
    if (user_name != null)
      url += "&selected_user=" + user_name
    if (page != null)
      url += "&page=" + page
    if (time_slice != null)
      url += "&time_slice=" + time_slice
    if(timeGap != 'all')
      url += "&time=" + timeGap

    var flag  = 0
    if(selection != 'Topic')
       flag  = 1
      
    url += "&flag=" + flag
    url += "&unc=" + unc
    
    const response = await axios.get(url, { headers: { "x-access-token": `${token}` } });
    commit('setBarChartData2', response.data.data)
  },
  async fetchArticle({ getters, commit }, { url }) {
    var token = getters.getToken
    const response = await axios.get(VUE_APP_API_URL + '/db/articles/?url=' + url, { headers: { "x-access-token": `${token}` } });
    commit('setSelectedArticle', response.data.data)
  },
  async fetchUsers({ getters, commit }, { search }) {
    var token = getters.getToken
    if (search.length > 2) {
      const response = await axios.get(VUE_APP_API_URL + '/db/users/names/' + search, { headers: { "x-access-token": `${token}` } });
      commit('setUserNames', response.data.data)
    } else 
    commit('setUserNames', [])
  },
  async fetchTimechartData({ commit, getters }) {
    var token = getters.getToken
    var topic = getters.getSelectedRootTopic[1]
    var selection = getters.getSelectedRootTopic[0]
    var user_name = getters.getSelectedUser
    var mode = getters.getSelectedTimeFrame
    var timeGap = getters.getSelectedTime
    var unc = getters.getSelectedModerationControllSetting.unc
    var url = null
    switch (mode) {
      case 'min':
        url = VUE_APP_API_URL + '/db/comments/group/min?time=' +timeGap
        break;
      case 's':
        url = VUE_APP_API_URL + '/db/comments/group/hour?time=' +timeGap
        break;
      case 't':
        url = VUE_APP_API_URL + '/db/comments/group/day?time=' +timeGap
        break;
      case 'm':
        url = VUE_APP_API_URL + '/db/comments/group/month?time=' +timeGap
        break;
      case 'y':
        url = VUE_APP_API_URL + '/db/comments/group/year?time=' +timeGap
        break;
      default:
        url = VUE_APP_API_URL + '/db/comments/group/year?time=' +timeGap
    }

    var flag  = 0
    if(selection != 'Topic')
      flag  = 1

    url += "&flag=" + flag
    url += "&unc=" + unc

    if (topic != null) {
      url += "&root_topic=" + topic
    }

    if (user_name != null) {
      url += "&user_name=" + user_name
    }

    const response = await axios.get(url, { headers: { "x-access-token": `${token}` } });
    commit('setTimeChartData', response.data.data)
  }
}

const mutations = {
  setToken: (state, token) => (state.token = token),
  setRole: (state, role) => (state.role = role),
  setInit: (state, newValue) => (state.init = newValue),

  // data for menu
  setRootTopics: (state, topics) => (state.root_topics = topics),
  setUserNames: (state, users) => (state.userNames = users),

  // filter
  setSelectedRootTopic: (state, topic) => (state.selected_root_topic = topic),
  setSelectedTime: (state, time) => (state.selected_time = time),
  setSelectedCommentId: (state, id) => (state.selected_comment_lid = id),
  setSelectedArticle: (state, article) => (state.selectedArticle = article),
  setSelectedCommentModel: (state, mode) => (state.selectedCommentsMode = mode),
  setSelectedUser: (state, user) => (state.selectedUser = user),
  setSelectedTimeSlice: (state, slice) => (state.selectedTimeSlice = slice),
  setSelectedTimeFrame: (state, time) => (state.selectedTimeFrame = time),
  setFetchCommentsModel: (state, mode) => (state.fetchCommentsModel = mode),

  // moderation controll
  setModerationControllData: (state, data) => (state.moderationControllData = data),
  setSelectedModerationControllSetting: (state, data) => (state.selectedModerationControllSetting = data),
  // vis
  setComments: (state, comments) => (state.commentsInList = comments),
  setTimeChartData: (state, data) => (state.timeChart.data = data),
  setBarChartData: (state, data) => (state.barChart.data = data),
  setBarChartMode: (state, mode) => (state.barChart.mode = mode),
  setBarChartData2: (state, data) => (state.barChart.data2 = data),
  setBarChartMode2: (state, mode) => (state.barChart.mode2 = mode),
  setBarChartCurrentPage: (state, page) => (state.barChart.currentPage = page),
  setBarChartCurrentPage2: (state, page) => (state.barChart.currentPage2 = page),
  setCommentListSettings: (state, settings) => (state.commentListSettings = settings),

  setSortCommentsSettingKey: (state, data) => (state.sortCommentsSettingKey = data), 
  setSortCommentsSettingMode: (state, data) => (state.sortCommentsSettingMode = data), 

  sortBarChart: function( state, key) {
    var series = state.barChart.data.series
    var categories = state.barChart.data.categories
    var list = [];

    for (var j = 0; j < series[0].data.length; j++) 
        list.push({'Online': series[0].data[j], 'Unsicher': series[1].data[j], 'Offline': series[2].data[j], 'categories': categories[j]});

    list.sort(function(a, b) {
      return ((a[key] > b[key]) ? -1 : ((a[key] == b[key]) ? 0 : 1));
    });

    for (var k = 0; k < list.length; k++) {
        series[0].data[k] = list[k].Online;
        series[1].data[k] = list[k].Unsicher;
        series[2].data[k] = list[k].Offline;
        categories[k] = list[k].categories
    }
    state.barChart.data.categories = categories
    state.barChart.data.series = [series[0], series[1], series[2]]
    

  }
}

const modules = {
  
}

//const vuexLocalStorage = new VuexPersist({
//  key: 'vuex',
//  storage: window.localStorage,
//  reducer: state => ({ token: state.token }),
//});

export default new Vuex.Store({
  state,
  getters,
  mutations,
  actions,
  modules,
//  plugins: [vuexLocalStorage.plugin]
})