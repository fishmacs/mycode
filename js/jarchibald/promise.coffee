get = (url) ->
  new Promise (resolve, reject) ->
    req = new XMLHttpRequest
    req.open 'GET', url

    req.onload = ->
      if req.status is 200
        resolve req.response
      else
        reject Error(req.statusText)
    
    req.onerror = ->
      reject Error('Network Error')
  
    req.send()

getJSON = (url) -> get(url).then JSON.parse

# the chapters order broken
story.chapterUrls.forEach (chapterUrl) ->
  getJSON(chapterUrls).then (chapter) ->
    addHtmlToPage chapter.html

story.chapterUrls.reduce (sequence, chapterUrl) ->
  sequence
    .then(-> getJSON chapterUrl)
    .then((chapter) -> addHtmlToPage(chapter.html))
,
   Promise.resolve()

# synchronized downloading
getJSON('story.json')
  .then (story) ->
    addHtmltoPage story.heading
    story.chapterUrls.reduce (sequence, chapterUrl) ->
      sequence
        .then(-> getJSON chaterUrl)
        .then((chapter) -> addHtmlToPage chapter.html)
    ,
      Promise.resolve()
  .then -> addTextToPage 'All done'
  .catch (err) -> addTextToPage "Argh, broken: #{err.message}"
  .then -> document.querySelector('.spinner').style.display = 'none'

# parallel downloading
getJSON('story.json')
  .then (story) ->
    addHtmlToPage story.heading
    Promise.all story.chapterUrls.map getJSON
  .then (chapters) ->
    chapters.forEach (chapter) ->
      addHtmlToPage chapter.html
    addTextToPage 'All done'
  .catch (err) -> addTextToPage "Argh, broken: #{err.message}"
  .then -> document.querySelector('.spinner').style.display = 'none'

# parallel downloading and displaying
getJSON('story.json')
  .then (story) ->
    addHtmlToPage story.heading
    story.chapterUrls.map(getJSON).reduce (sequence, chaterPromise) ->
      sequence
        .then -> chaterPromise
        .then chapter -> addHtmlToPage chapter.html
    ,
      Promise.resolve()
  .then -> addTextToPage 'All done'
  .catch (err) -> addTextToPage "Argh, broken: #{err.message}"
  .then -> document.querySelector('.spinner').style.display = 'none'

#generator
spawn = (generatorFunc) ->
  continure = (verb, arg) ->
    try
      result = generator[verb] arg
    catch err
      return Promise.reject err
    if result.done
      return result.value
    else
      return Promise.resolve(result.value).then onFufilled, onRejected

  generator = generatorFunc()
  onFulfilled = continuer.bind continuer, 'next'
  onRejected = continure.bind continuer, 'throw'
  onFulfilled()

spawn ->
  try
    story = yield getJSON 'story.json'
    addHtmlToPage story.heading

    for chapterPromise in story.chapterUrls.map getJSON
      chapter = yield chapterPromise
      addHtmlToPage chapter.html

    addTextToPage 'All done'
  catch err
    addTextToPage "Argh, broken: #{err.message}"
  document.querySelector('.spinner').style.display = 'none'
