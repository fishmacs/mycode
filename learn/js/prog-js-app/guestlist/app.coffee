$ = require 'jquery-browserify'
guestListModel = require './guestlistmodel'
guestListView = require './guestlistview'

$container = $ '#container'

$ ->
  guestListData = guestListModel.load()
  $guestList = guestListView.render(guestListData)
  $container.empty().append($guestList)
