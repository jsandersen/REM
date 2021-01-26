<template>
  <div >
    <v-list class="pt-0" style="max-height: 410px" >
      <v-slide-y-transition class="py-0" group tag="v-list">
        <v-card style="height:6em;background=blue;"  @click.native="cardClick(index, comment.id)" :id="index" class="mt-1 mr-3" :style="{ 'background-color': getColour(comment), 'border': getBorder(index) }" fluid v-for="(comment, index) in getComments" v-bind:key="(comment, index)">    
          <v-list-item three-line >
            <v-list-item-content class='mt-0 pt-0 mb-0 ob-0'>
              <div class="overline">
                <small>{{ $t('topic') }}:</small> <big class="topic" @click="selectTopic(comment.topic_root)" >{{comment.topic_root}}</big> - <small>{{ $t('user') }}:</small> <big class="user" @click="selectUser(comment.user_name)">{{comment.user_name}}</big> - <small>{{ $t('likes') }}</small>: <big>{{ comment.recommendations }}</big> 
              </div>
              <v-list-item-subtitle>{{comment.text_history[0]}}</v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-avatar class="mt-2 mr-0" tile  width="100" height="70">
              <D3PieChart v-if="!comment.ml.human" :id="'chart'+comment.id.toString()" :p_block="comment.ml.p_blocked" />
              <div v-if="comment.ml.human">
                <v-icon class="ml-7" x-large>
                mdi-account
                </v-icon>
              </div>        
            </v-list-item-avatar>
          </v-list-item>
        </v-card>
      </v-slide-y-transition>
    </v-list>
    <v-pagination
      v-model="currentPage"
      :length="numberOfPages"
      circle
      :total-visible="5"
    ></v-pagination>
  </div>
</template>

<script>
  import { mapGetters, mapActions, mapMutations } from 'vuex'
  import D3PieChart from './D3PieChart'
  export default {
    components: {
      D3PieChart
    },
    data () {
      return {
        focus:0,
        focus_cid:null,
        currentPage: 1,
        perPage: 4,
        perPageOptions: [4,6],
        data2: [],
        numberOfPages : 1,
      }
    },
    methods: {
        ...mapActions(['fetchComments', 'fetchCommentCount']),
        ...mapMutations(['setSelectedCommentId', 'setSelectedRootTopic', 'setSelectedUser', 'setCommentListSettings']),
        setPage(n) {
            this.currentPage = n;
            if (n > this.numberOfPages) {
                this.currentPage = this.numberOfPages;
            }
            this.fetchComments({offset:this.offset, limit:this.limit})
        
        },
        setNumberOfPages() {
          var result = this.fetchCommentCount()
          result.then((value) => {
            this.numberOfPages = Math.ceil(value.data.count / this.perPage)
          })

        },
        selectTopic(topic) {
          this.setSelectedRootTopic(topic)
        },
        selectUser(user) {
          this.setSelectedUser(user)
        },
        getColour(comment) {
          if(comment.ml == null) {
            return "#59a14f" // TODO
          }
// "#59a14f", "#bab0ac", "#e15759"
          if(comment.ml.uncertainty >= this.getSelectedModerationControllSetting.unc) {
            return '#bab0ac' // '#bab0ac' //
          } else if(comment.ml.blocked == 1) {
            return 'lightcoral' // "#e15759"
          } else if(comment.ml.blocked == 0) {
            return 'lightgreen' // "#59a14f" //
          }
        },
        getBorder(index) {
          if(this.getSelectedCommentId == index) {
            return '5px solid blue'
          } else {
            return '5px solid transparent'
          }
        },
        cardClick(id, cid) {
          this.setSelectedCommentId(id)
          this.focus_cid = cid
        }
  },
  watch : {
    getComments(newVal) {
      if (newVal.length == 0) {
        this.focus_cid = null
      } else {
        this.focus_cid = newVal[0].id
      } 
    },
    currentPage(newVal) {
       this.setPage(newVal)
    },
    getSelectedCommentMode() {
      this.currentPage = 1
      this.fetchComments({offset:this.offset, limit:this.limit})
      this.setNumberOfPages()
    },
    getSelectedRootTopic() {
      this.currentPage = 1
      this.fetchComments({offset:this.offset, limit:this.limit})
      this.setNumberOfPages()
    },
    getSelectedUser() {
      this.currentPage = 1
      this.fetchComments({offset:this.offset, limit:this.limit})
      this.setNumberOfPages()
    },
    getSelectedTimeSlice() {
      this.currentPage = 1
      this.fetchComments({offset:this.offset, limit:this.limit})
      this.setNumberOfPages()
    },
    getSelectedTime() {
      this.currentPage = 1
      this.fetchComments({offset:this.offset, limit:this.limit})
      this.setNumberOfPages()
    },
    getFetchCommentsModel() {
      this.currentPage = 1
      this.fetchComments({offset:this.offset, limit:this.limit})
      this.setNumberOfPages()
    }
  },
  mounted() {
    window.addEventListener("keydown", e => {
      // up
    	if (e.keyCode == '38' && this.getSelectedCommentId > 0) {
        this.setSelectedCommentId(this.getSelectedCommentId -1 )
        this.focus_cid = this.getComments[this.focus].id
      }
      // down
      if (e.keyCode == '40' && this.getSelectedCommentId < (this.perPage - 1)) {
        this.setSelectedCommentId(this.getSelectedCommentId + 1)
        this.focus_cid = this.getComments[this.getSelectedCommentId].id

      }

    });
  },
  computed: {
    ...mapGetters(['getComments', 'getFetchCommentsModel', 'getSelectedTime', 'getSelectedCommentId', 'getSelectedModerationControllSetting', 'getSelectedCommentMode', 'getSelectedRootTopic', 'getSelectedUser', 'getSelectedTimeSlice']),
  	offset() {
      var offset = ((this.currentPage - 1) * this.perPage);
      this.setCommentListSettings({offset:offset})
      console.log('offset')
    	return offset
    },
    limit() {
    	return (this.perPage);
    },
    numOfPages() {
    	return Math.ceil(10 / this.perPage);
    },
  },
    created() {
      this.fetchComments({offset:0, limit:this.perPage})
      this.setNumberOfPages()
      
    }
  }
</script>

 <style>
.class2 {
  background-color : blue;
}

.topic:hover {
  color: rgb(60, 22, 165);
  cursor: pointer;
}

.user:hover {
  color: rgb(60, 22, 165);
  cursor: pointer;
}

 </style>