const messages = {
  // english
  en: { // {{ $t('hello') }}
      hello: 'hello world',
      tool_name: 'REM',

      // login
      login_user : 'User',
      login_pwd: 'Password',
      login_fail_msg: 'Access denied.', 
      login: 'Login',

      // Filter
      filter: 'filter',
      active_filter: 'Active Filter:',
      topic_filter: 'Topic Filter',
      user_filter: 'User Filter',
      abv_hour: 'H',

      // Controll View
      curr_strategy: 'Current Strategy',
      strategy: 'Strategy',
      expected: 'Expected',
      acc: 'Accuracy',
      effort: 'Effort',
      apply: 'Apply',
      recommendation: 'Recommendation',
      recommendation_text: 'best efficency',
      custom: 'Custom',
      change_strategy: 'Strategy Selection',
      info_text: 'Define a custom strategy via visualization',
      submit_selection: 'Confirm new Strategy',
      submit_info_text: 'Effect on automatically classified comments of the last 72 hours',
      select : 'Select',
      strategy: 'Strategy',
      moderation_vis_title: 'Strategy Overview',
      controll_view_title: 'Moderation Strategy Selection',
      quick_selection: 'Quick Selection',
      per_day: 'per day',
      category: 'Category',
      before: 'Before',
      later: 'Later',
      difference: 'difference',
      


      // charts
      time_chart_title: 'Distribution of Comments',
      time_chart_y_label: 'Number of Comments',
      bar_chart1_title: 'Comments by ...',
      bar_chart2_title: 'Comments by User',
      moderation_box_tiltle: 'Moderation-View',
      
      // Filter options
      online: 'Valid',
      uncertain: 'Uncertain',
      uncertainty: 'Uncertainty',
      offline: 'Blocked',
      sum: 'Total',
      date: 'Date',
      all: 'All',
      block: 'Block',
      acept: 'Valid',
      agree: 'Agree',
      min: 'Minutes',
      hour: 'Hours',
      day: 'Days',

      user: 'User',
      likes: 'Likes',
      topic: 'Topic',
      article: 'Article',

      none: 'none', 
      empty_selection: 'No comments here...',
      close_window:'close window',
      black: 'back',
      save: 'save',

      // sort by      
      sort: 'Sort by ...',
      group: 'Group by ...',

    },
  // german
  de: {
      hello: 'Hallo Welt',
      tool_name: 'REM',

      // login
      login_user : 'Benutzer',
      login_pwd: 'Passwort',
      login_fail_msg: 'Zugang abgelehnt.', 
      login: 'Anmelden',

      // charts
      time_chart_title: 'Kommentaraufkommen',
      time_chart_y_label: 'Anzahl Kommentare',
      bar_chart1_title: 'Kommentare nach ...',
      bar_chart2_title: 'Kommentare nach Nutzern',
      moderation_box_tiltle: 'Moderationsansicht',

      user: 'Nutzer',
      likes: 'Gefällt',
      topics: 'Themen',
      articles: 'Artikel',
      none: 'keine',
      abv_hour: 'Std',

      // Filter
      filter: 'filter',
      active_filter: 'Aktive Filter:',
      topic_filter: 'Themenfilter',
      article_filter: 'Artikelfilter',
      user_filter: 'Nutzerfilter',

      // Filter options
      online: 'Online',
      uncertain: 'Unsicher',
      uncertainty: 'Unsicherheit',
      offline: 'Offline',
      sum: 'Summe',
      date: 'Datum',
      all: 'Gesamtheit',
      block: 'Blockieren',
      acept: 'Akzeptieren',
      agree: 'Zustimmen',
      min: 'Minutes',
      hour: 'Hours',
      day: 'Days',

      empty_selection: 'Keine Auswahl',
      close_window:'Fenster schließen',

      // sort by      
      sort: 'Sortieren nach...',
      group: 'Grupieren nach...',

      black: 'Zurück',
      save: 'Speichern',

      // Controll View
      curr_strategy: 'Aktuelle Konfiguration',
      strategy: 'Strategy',
      expected: 'Expected',
      acc: 'Accuracy',
      effort: 'Effort',
      apply: 'Anwenden',
      recommendation: 'Empfehlung',
      recommendation_text: 'optimaler Ertrag',
      custom: 'Benutzerdefiniert',
      change_strategy: 'Konfiguration anpassen',
      info_text: 'Benutzerdefiniert Auswahl über Abbildung',
      submit_selection: 'Konfiguration Bestätigen',
      submit_info_text: 'Auswirkung auf automatisch klassifierite Kommentare der Letzten 72h',
      select : 'Auswahl',
      strategy: 'Strategie',
      moderation_vis_title: 'Konfigurationen',
      controll_view_title: 'Konfiguration: Zielgenauigkeit / Moderationsaufwand',
      quick_selection: 'Schnellauswahl',
      per_day: 'pro Tag',
      category: 'Kategorie',
      before: 'Vorher',
      later: 'Nachher',
      difference: 'Differenz',

  }
}

export default { messages }