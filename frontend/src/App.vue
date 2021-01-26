<template>
  <v-app >
    <div v-if="!getToken">
      <LogInPage />
    </div>
    <div v-if="getToken && getInit">
    <v-app-bar app color="green" dark dense>
      <div class="d-flex align-center">
        <v-toolbar-title>REM</v-toolbar-title>
      </div>

      <!-- Active Filter -->
      <v-spacer></v-spacer>
      {{ $t('active_filter') }}
        <SelectionTokens />
      <v-spacer></v-spacer>

      <!-- Controll-View -->
      <div v-if="getRole">
        <ModerationControll />
      </div>


      <AutoUpdater/>

    </v-app-bar>

    <v-main>
      <div class="main_frame">
        <v-layout row justify-space-around class="ml-0" style="background:#F5F5F5;">
          
          <!-- Context-View -->
          <v-flex style="width: 0vh;">
            <v-container>

              <!-- Time Chart -->
              <v-card>
                <v-toolbar dense elevation="0" style="background:white;">
                  <v-toolbar-title>{{ $t('time_chart_title') }}</v-toolbar-title>
                  <v-spacer></v-spacer>
                  <ButtonGroup />
                  <v-spacer></v-spacer>
                  <TimeSelector />
                </v-toolbar>
                <D3StackedBarchart></D3StackedBarchart>
              </v-card>
            </v-container>

            <!-- BarCharts -->
            <v-container row justify-space-around class="ml-0 pt-0">
              <v-card width="49%" min-width="300px" class="mr-1">
                <D3GroupedBarchart />
              </v-card>
              <v-card width="49%" min-width="300px" class="ml-2">
                <D3GroupedBarchart2 />
              </v-card>
            </v-container>
          </v-flex>

          
          <!-- Moderation-View -->
          <v-flex style="max-width: 50%">
            <CommentBox />
            <CommentsTable />
          </v-flex>

        </v-layout>
      </div>
    </v-main>
    </div>
  </v-app>
</template>

<script>

import LogInPage from "./components/LogInPage";
import AutoUpdater from "./components/AutoUpdater";
import SelectionTokens from "./components/SelectionTokens";

import ButtonGroup from "./components/context-view/ButtonGroup";
import D3StackedBarchart from "./components/context-view/D3StackedBarchart";
import TimeSelector from "./components/context-view/TimeSelector";
import D3GroupedBarchart from "./components/context-view/D3GroupedBarchart";
import D3GroupedBarchart2 from "./components/context-view/D3GroupedBarchart2";

import CommentBox from "./components/moderation-view/CommentBox";
import CommentsTable from "./components/moderation-view/CommentsTable";
import ButtonGroup2 from "./components/moderation-view/ButtonGroup2";

import ModerationControll from "./components/controll-view/ModerationControll";

import { mapGetters, mapActions, mapMutations } from "vuex";

export default {
  name: "App",

  components: {
    SelectionTokens,
    CommentsTable,
    ButtonGroup,
    ButtonGroup2,
    CommentBox,
    D3StackedBarchart,
    D3GroupedBarchart,
    D3GroupedBarchart2,
    TimeSelector,
    AutoUpdater,
    ModerationControll,
    LogInPage,
  },
  methods: {
    ...mapActions(["fetchModerationControllData"])
  },
  computed: {
    ...mapGetters(['getInit', 'getToken', 'getRole']),
  },
  data: () => ({
    load : true
  })
};
</script>

<style scoped>
.main_frame {
  min-width: 1300px;
  overflow-x: auto;
}
</style>
