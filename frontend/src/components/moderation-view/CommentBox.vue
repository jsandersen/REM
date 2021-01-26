<template>
    <div>
        <v-card column class="mt-3 mr-3 mb-3" height="387">
            <v-toolbar dense elevation="0" style="background:white;">
                <v-toolbar-title>{{ $t('moderation_box_tiltle') }}</v-toolbar-title>
                <v-spacer></v-spacer>
                        <div class="pa-0"> 
                            <v-btn dense icon>
                                <v-icon v-if="sort_asc" @click="sort(false)" medium>mdi-arrow-up</v-icon>
                                <v-icon v-if="!sort_asc" @click="sort(true)" medium>mdi-arrow-down</v-icon>
                            </v-btn>
                        </div>
                        <div class="mt-6">
                            <v-flex style="width: 10em;">
                                <v-select
                                outlined
                                :items="items"
                                v-model="mode"
                                dense
                                :label="$t('sort')"
                                ></v-select>
                            </v-flex >
                        </div>
                        <v-spacer></v-spacer>
                            <v-switch
                            v-model="human_annotations"
                            color="blue darken-3"
                            hide-details
                            ></v-switch>
                            <v-icon v-if="human_annotations">mdi-account</v-icon>
                            <v-icon v-if="!human_annotations">mdi-account-off</v-icon>

                            
                    <v-spacer></v-spacer>
                <ButtonGroup2/>
            </v-toolbar>
            <v-list-item one-line>
                <v-list-item-content v-if="getSelectedArticle != null" class='mt-0 pt-0'>
                    <div class="overline"><small>{{ $t('article') }}</small>: {{getSelectedArticle.title}}  </div>
                    <v-list-item>{{getSelectedArticle.kicker}} - {{getSelectedArticle.summary}}</v-list-item>
                </v-list-item-content>
            </v-list-item>
            <v-list-item three-line>
                <v-list-item-content v-if="getComments.length > 0" class='mt-0 pt-0'>
                    <div class="overline"> 
                        
                        <!--
                        <v-menu v-model="dialog2" :close-on-content-click="false">
                            
                        
                                <v-card width="900" max-height="900" class="scroll">
                                        <v-subheader><h2>Diskussionsstrang</h2></v-subheader>
                                <v-timeline align-top dense>
                            <v-timeline-item
                            v-for="item in parentComments"
                            :key="item.id"
                            small
                            :color="getColour(item)"
                            >
                            
                            <div>
                                <div class="font-weight-normal">
                                <strong>{{ item.user_name }}</strong>
                                </div>
                                <div>{{ item.text_history[0] }}</div>

                            </div>
                                    <v-btn v-if="item.i != (parentComments.length -1)" x-small color="#e15759" @click="labeln(1, item.id, item.i)" :disabled='item.ml != null && item.ml.blocked == 1' >Blockieren</v-btn>
                                    <v-btn v-if="item.i != (parentComments.length -1)" x-small color="#59a14f" @click="labeln(0, item.id, item.i)" :disabled='item.ml != null && item.ml.blocked == 0 && item.ml.uncertainty < getSelectedModerationControllSetting.unc'>Billigen</v-btn>
                            
                            </v-timeline-item>
                        </v-timeline>
                        </v-card>
                        </v-menu>
                        -->

                        <small>{{ $t('user') }}:</small> {{comment.user_name}} - <small>{{ $t('likes') }}</small> : {{ comment.recommendations }}  <small>Id:</small> {{comment.id}} <!-- <small v-if="comment.parent_id">Diskussion:</small> <sec v-if="comment.parent_id" v-for="item in parentComments" :key="item.id"> {{ item.i }}</sec> <v-btn @click="dialog2 = true" x-small fab v-if="comment.parent_id"><v-icon>mdi-comment-text-outline</v-icon></v-btn>-->
                    </div>
                        <v-container class="view pl-0">
                            <v-list-item >{{comment.text_history[0]}}</v-list-item>
                        </v-container>
                        
                        
                </v-list-item-content>
            </v-list-item>

            <v-list-item one-line v-if="getComments.length == 0">
                <v-list-item-content  class='mt-0 pt-0'>
                        <div class="overline">
                            <v-list-item>{{ $t('empty_selection') }}</v-list-item>
                        </div>
                </v-list-item-content>
            </v-list-item>

            <v-toolbar dense elevation="5" v-if="comment.ml != null">
                <v-spacer></v-spacer>
                <v-btn :disabled="comment.ml.blocked == 1 && sm(comment.ml.uncertainty) && comment.ml.human" :color="comment.ml.blocked == 1 && sm(comment.ml.uncertainty) ? 'red lighten-4' : '#e15759'" @click="labeln(1, null, null)" > {{ comment.ml.blocked == 1 && sm(comment.ml.uncertainty) ? this.$t('agree') : this.$t('block') }} </v-btn>
                <v-spacer></v-spacer>
                <ProgressBar v-if="!comment.ml.human"/>
                <div v-if="comment.ml.human">
                     <svg class='spacer' width="300" height="50"></svg>
                </div>
                <v-spacer></v-spacer>
                <v-btn :disabled="comment.ml.blocked == 0 && sm(comment.ml.uncertainty) && comment.ml.human" :color="comment.ml.blocked == 0 && sm(comment.ml.uncertainty) ? 'green lighten-4' : '#59a14f'" @click="labeln(0, null, null)">{{ comment.ml.blocked == 0 && sm(comment.ml.uncertainty) ? this.$t('agree') : this.$t('acept')  }}</v-btn>
                <v-spacer></v-spacer>
            </v-toolbar>

<!--
            <v-toolbar dense elevation="5" v-if="getComments.length > 0 && comment.ml == null">
                <v-spacer></v-spacer>
                <v-btn color="#e15759" @click="labeln(1, null, null)" >{{ this.getlabel(1, 0, 0) }}</v-btn>
                <v-spacer></v-spacer>
                <ProgressBar v-if="!comment.ml.human"/>
                <div v-if="comment.ml.human">
                    <svg class='spacer' width="300" height="50"></svg>
                </div>
                <v-spacer></v-spacer>
                <v-btn color="#59a14f" @click="labeln(0, null, null)">Billigen</v-btn>
                <v-spacer></v-spacer>
            </v-toolbar>
-->
        </v-card>
    </div>
</template>


<script>
import { mapGetters, mapActions, mapMutations } from 'vuex'
import ButtonGroup2 from './ButtonGroup2'
import ProgressBar from './ProgressBar'

  export default {
    components: {
      ButtonGroup2,
      ProgressBar
    },
    data: () => ({
      items : ['Date', 'Uncertainty', 'Likes'], // TODO i18n
      mode : 'Date',
      sort_asc : true,
      dialog2 : false,
      parentComments : [],
    }),
     computed: {
      ...mapGetters(['getComments', 'getFetchCommentsModel', 'getSelectedModerationControllSetting', 'getSelectedCommentId', 'getSelectedArticle', 'getSelectedCommentMode', 'getSortCommentsSettingMode', 'getSortCommentsSettingKey', 'getFetchCommentsModel']),
      comment() {
          if(this.getComments.length == 0) {
              return []
          } else {
            return this.getComments[this.getSelectedCommentId]
          }
      },
      human_annotations : {
        get() {
          return this.getFetchCommentsModel;
        },        
        set(value) {
          this.setFetchCommentsModel(value)
        }
      }
     },
     methods : {
         ...mapActions(['fetchArticle', 'labelInctance', 'fetchComments', 'fetchOneComment', 'fetchParentComments']),
         ...mapMutations(['setSortCommentsSettingKey', 'setSortCommentsSettingMode', 'setFetchCommentsModel']),
         sm(value) {
             return value < this.getSelectedModerationControllSetting.unc
         },
         labeln(blockieren, id, index) {
             if(id && index != (this.parentComments.length -1)) {
                 var res = this.labelInctance({id:id, blocked:blockieren})
                
                 this.parentComments[index].ml.blocked = blockieren
                 this.parentComments[index].ml.human = 1
                 this.parentComments[index].ml.uncertainty_old = this.getComments[this.getSelectedCommentId].ml.uncertainty
                 this.parentComments[index].ml.uncertainty = -1 
                                
             } else {
                var res = this.labelInctance({id:this.comment.id, blocked:blockieren})
                if ((this.getSelectedCommentMode != 'all' || this.getFetchCommentsModel == 0) && !(this.getFetchCommentsModel != 0 && blockieren == this.getComments[this.getSelectedCommentId].ml.blocked && this.sm(this.getComments[this.getSelectedCommentId].ml.uncertainty ))) {
                    this.getComments.splice(this.getSelectedCommentId, 1);
                    this.fetchOneComment()
                } else {
                    this.getComments[this.getSelectedCommentId].ml.blocked = blockieren
                    this.getComments[this.getSelectedCommentId].ml.human = 1
                    this.getComments[this.getSelectedCommentId].ml.uncertainty_old = this.getComments[this.getSelectedCommentId].ml.uncertainty
                    this.getComments[this.getSelectedCommentId].ml.uncertainty = -1
                }
             }
         },
         getColour(comment) {
        if(comment.ml == null) {
            return "grey lighten-5" // TODO
          }// "#59a14f", "#bab0ac", "#e15759"
          if(comment.ml.uncertainty >= this.getSelectedModerationControllSetting.unc) {
            return 'grey lighten-1' // '#bab0ac' //
          } else if(comment.ml.blocked == 1) {
            return 'red darken-2' // "#e15759"
          } else if(comment.ml.blocked == 0) {
            return 'green darken-2' // "#59a14f" //
          }
         },
         sort(bool) {
             this.sort_asc = bool
             this.setSortCommentsSettingMode(bool ? -1 : 1)
             this.fetchComments({offset:0, limit:4})
         },
         setPartents() {
            //var parents = this.fetchParentComments({id: this.comment.id})
            //parents.then((value) => this.parentComments = value.data.data) // 
         }

     },
     watch : {
         dialog2() {
            this.setPartents()
         },
         comment() {
             if(this.getSelectedArticle == null || (this.comment.article != this.getSelectedArticle.url)) // TODO
                this.fetchArticle({url:this.comment.article})
                this.dialog2 = false
                this.setPartents()
         },
         mode(newValue) {
             this.setSortCommentsSettingKey(this.items.findIndex((_) => _ == newValue))
             this.fetchComments({offset:0, limit:4})
         }
     }
  }
</script>

<style scoped>

.view{
  height:150px;
  overflow-y:auto
}

.scroll {
   overflow-y: scroll
}

</style>