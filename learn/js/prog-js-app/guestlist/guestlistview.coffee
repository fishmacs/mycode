$ = require 'query-browerify'

checkedinClass = 'icon-check'
listClass = 'dropdown-menu'
guestClass = 'guest'

toggleCheckedIn = (e) ->
  $(this).toggleClass checkedinClass

$listView = $('<ol>', id: 'guestlist-view', class: listClass)
  .on('click', '.' + guestClass, toggleCheckedIn)

render = (guestlist) ->
  $listView.empty()
  guestlist.forEach (guest) ->
    $guest = $ "<li class=\"#{guestClass}\"><span class=\"name\">
      #{guest}</span></li>"
    $guest.appendTo($listView)
  $listView

exports.api = render: render
