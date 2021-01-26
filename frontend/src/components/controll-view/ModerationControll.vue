<template>
  <div class="text-center">
    <v-dialog v-model="dialog" width="1200">
      <template v-slot:activator="{ on, attrs }">
        <v-btn class="mr-4" outlined  v-bind="attrs" v-on="on">Moderation-Strategy</v-btn>
      </template>
      <v-card>
        <v-card-title
          class="headline grey lighten-2"
        >{{ $t('controll_view_title')}}</v-card-title>
        <v-container style="max-width: 1150px;">
          <v-row no-gutter>
            <v-col style="max-width: 450px;">
              <!--<LineChart @tmp_settig="tmpsettig" @old_setting="oldsetting" />-->
              <v-list two-line header>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title>{{ $t('moderation_vis_title') }}</v-list-item-title>
                    <D3LineChart @tmp_settig="tmpsettig" @old_setting="oldsetting" />
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-col>
            <v-col>
              <div class="fixhight">
                <v-col>
                  <v-row>
                    <v-list two-line header>
                      <v-list-item>
                        <v-list-item-content>
                          <v-list-item-title>{{ $t('curr_strategy') }}</v-list-item-title>
                          <v-col>
                            <table>
                              <tr>
                                <th style="width:200px" colspan="2">{{ $t('strategy') }}</th>
                                <th >
                                  {{ $t('expected') }} {{ $t('acc') }}
                                </th>
                                <th style="width:200px">
                                  {{ $t('effort') }}
                                </th>
                              </tr>
                              <tr>
                                <td>
                                  <svg height="10" width="10">
                                    <circle cx="5" cy="5" r="5" fill="blue" />
                                  </svg>
                                </td>
                                <td>{{ getSelectedModerationControllSetting.name }}</td>
                                <td>{{ getSelectedModerationControllSetting.acc }}%</td>
                                <td>{{ getSelectedModerationControllSetting.load }}% <br>(~{{ getSelectedModerationControllSetting.load * 90 }} {{ $t('per_day') }})</td>
                              
                              </tr>
                            </table>
                          </v-col>
                        </v-list-item-content>
                      </v-list-item>
                    </v-list>
                  </v-row>

                  <v-row>
                    <v-list two-line header class="fixhight">
                      <v-list-item>
                        <v-list-item-content>
                          <v-list-item-title v-if="!this.inSubmission">{{ $t('change_strategy') }}</v-list-item-title>
                          <v-list-item-subtitle v-if="!this.inSubmission">({{ $t('info_text') }})</v-list-item-subtitle>
                            <v-list-item-title v-if="oldAndNew != null">{{ $t('submit_selection') }}</v-list-item-title>
                            <v-list-item-subtitle v-if="oldAndNew != null">{{ $t('submit_info_text') }}</v-list-item-subtitle>

                          <v-col style="min-height: 210px;">
                            <div v-if="!this.inSubmission">
                              <table>
                                <tr>
                                  <th style="width:50px">{{ $t('select') }}</th>
                                  <th colspan="2">{{ $t('strategy') }}</th>
                                  <th>
                                  {{ $t('expected') }}
                                   {{ $t('acc') }}
                                  </th>
                                  <th>
                                    {{ $t('effort') }}
                                  </th>
                                </tr>
                                <tr v-if="getSelectedModerationControllSetting.load != getModerationControllData.knee_point.load">
                                  <td>
                                    <v-btn
                                      @click="submit(getModerationControllData.knee_point)"
                                      x-small
                                    >{{ $t('apply') }}</v-btn>
                                  </td>
                                  <td>
                                    <svg height="10" width="10">
                                      <circle cx="5" cy="5" r="5" fill="orange" />
                                    </svg>
                                  </td>
                                  <td>
                                    {{ $t('recommendation') }}
                                    <br />({{ $t('recommendation_text') }})
                                  </td>
                                  <td>{{ getModerationControllData.knee_point.acc }}%</td>
                                  <td>{{ getModerationControllData.knee_point.load }}% <br>(~{{ getModerationControllData.knee_point.load * 90 }} {{ $t('per_day') }})</td>
                      
                                </tr>

                                <tr>
                                  <td>
                                    <v-btn
                                      @click="submit(old_setting)"
                                      x-small
                                      v-show="old_setting.acc != this.$t('empty_selection')"
                                    >{{ $t('apply') }}</v-btn>
                                  </td>
                                  <td>
                                    <svg height="10" width="10">
                                      <circle cx="5" cy="5" r="5" fill="green" />
                                    </svg>
                                  </td>
                                  <td>{{ $t('custom') }}</td>
                                  <td if>{{ old_setting.acc != this.$t('empty_selection') ? old_setting.acc + '%' : 'None'}}</td>
                                  <td>{{ old_setting.acc != this.$t('empty_selection') ? old_setting.load + '%' : 'None' }} <br>{{ old_setting.acc != this.$t('empty_selection') ? '(~' + old_setting.load * 90 + ' ' + $t('per_day') + ')' : '' }}</td>
                            
                                </tr>
                                <tr v-show="tmp_settig.acc">
                                  <td></td>
                                  <td>
                                    <svg height="10" width="10">
                                      <circle
                                        cx="5"
                                        cy="5"
                                        r="4"
                                        stroke="green"
                                        stroke-width="1"
                                        fill="none"
                                      />
                                    </svg>
                                  </td>
                                  <td>{{ $t('quick_selection')}}</td>
                                  <td>{{ tmp_settig.acc }}%</td>
                                  <td>{{ tmp_settig.load }}% <br>(~{{ tmp_settig.load * 90 }} {{ $t('per_day') }})</td>
   
                                </tr>
                              </table>
                            </div>

                            <div v-if="oldAndNew != null">
                              <table>
                                <tr>
                                  <th>{{ $t('category') }}</th>
                                  <th>{{ $t('before') }}</th>
                                  <th>{{ $t('later') }}</th>
                                  <th>{{ $t('difference') }}</th>
                                </tr>
                                <tr style="background-color: #59a14f">
                                  <td>{{ $t('online') }}</td>
                                  <td>{{ oldAndNew.old.sum_not_blocked }}</td>
                                  <td>{{ oldAndNew.new.sum_not_blocked }}</td>
                                  <td>{{ oldAndNew.new.sum_not_blocked - oldAndNew.old.sum_not_blocked }}</td>
                                </tr>
                                <tr style="background-color: #bab0ac">
                                  <td>{{ $t('uncertain') }}</td>
                                  <td>{{ oldAndNew.old.sum_unc }}</td>
                                  <td>{{ oldAndNew.new.sum_unc}}</td>
                                  <td>{{ oldAndNew.new.sum_unc - oldAndNew.old.sum_unc}}</td>
                                </tr>
                                <tr style="background-color: #e15759">
                                  <td>{{ $t('offline') }}</td>
                                  <td>{{ oldAndNew.old.sum_blocked }}</td>
                                  <td>{{ oldAndNew.new.sum_blocked }}</td>
                                  <td>{{ oldAndNew.new.sum_blocked - oldAndNew.old.sum_blocked }}</td>
                                </tr>
                              </table>
                              <div class="d-flex justify-center mt-3">
                               <v-btn @click="back()" class="mr-2" small >{{ $t('back') }}</v-btn>
                               <v-btn @click="save()" class="ml-2" small >{{ $t('save') }}</v-btn>
                              </div>
                            </div>
                          </v-col>
                        </v-list-item-content>
                      </v-list-item>
                    </v-list>
                  </v-row>
                </v-col>

              </div>
            </v-col>
          </v-row>
        </v-container>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="dialog = false">{{ $t('close_window') }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>


<script>
import D3LineChart from "./D3LineChart";
import { mapGetters, mapActions, mapMutations } from "vuex";
export default {
  components: {
    D3LineChart
  },
  data() {
    return {
      inSubmission: false,
      number: 0,
      dialog: false,
      tmp_settig: "",
      old_setting: { acc: this.$t('empty_selection'), load: this.$t('empty_selection') },
      oldAndNew: null,
      tmp: null
    };
  },
  methods: {
    ...mapMutations(['setSelectedModerationControllSetting']),
    ...mapActions([
      "setModerationStrategy",
      "fetchModerationDiff",
      "fetchTimechartData",
      "fetchSelectedModerationControllSetting",
      "fetchBarChartData",
      "fetchBarChartData2",
      "fetchComments"
    ]),
    back() {
      this.oldAndNew = null
      this.inSubmission = false
    },
    save() {
      this.setSelectedModerationControllSetting(this.tmp)

      var request = this.setModerationStrategy()
      request.then((value) => {
        this.dialog = false;
        this.oldAndNew = null
        this.inSubmission = false
        // UPDATE ALL
        this.fetchTimechartData()
        this.fetchBarChartData({})
        this.fetchBarChartData2({})
        this.fetchComments({offset:0, limit:4})
      })
      
    },
    submit(value) {
      value.unc = 1-value.unc

      let unc_new = value.unc;
      let unc_old = this.getSelectedModerationControllSetting.unc;
      var request = this.fetchModerationDiff({
        unc_old: unc_old,
        unc_new: unc_new
      });
      request.then(value => {
        this.inSubmission = true
        this.oldAndNew = value.data.data;
      });
      this.tmp = value
    },
    tmpsettig(value) {
      this.tmp_settig = value;
    },
    oldsetting(value) {
      this.old_setting = value;
    }
  },
  computed: {
    ...mapGetters([
      "getModerationControllData",
      "getSelectedModerationControllSetting",
    ])
  },
};
</script>

<style scoped>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td,
th {
  border: 1px solid #dddddd;
  text-align: center;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #f0eeee;
}

.fixhight {
   position: relative;
   top:-12px;
}
</style>