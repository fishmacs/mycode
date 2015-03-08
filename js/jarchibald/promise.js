function get(url) {
  return new Promise((resolve, reject) => {
    var req = new XMLHttpRequest();
    req.open('GET', url);
    
    req.onload = () => {
      if (req.status == 200)
        resolve(req.response);
      else
        reject(Error(req.statusText));
    };

    req.onerror = () => {
      reject(Error('Network Error'));
    };

    req.send();
  });
}

function getJSON(url) {
  return get(url).then(JSON.parse);
}

// the chapters order broken
story.chapterUrls.forEach((chapterUrl) => {
  getJSON(chapterUrls).then((chapter) => {
    addHtmlToPage(chapter.html);
  });
});

// chapters in order
let sequence = Promise.resolve();
story.chapterUrls.forEach((chapterUrl) => {
  sequence = sequence.then(() => {
    return getJSON(chapterUrl);
  }).then((chapter) => {
    addHtmlToPage(chapter.html);
  });
});

story.chapterUrls.reduce((sequence, chapterUrl) => {
  return sequence.then(() => {
    return getJSON(chapterUrl);
  }).then((chapter) => {
    addHtmlToPage(chapter.html);
  });
}, Promise.resolve());

// synchronized downloading
getJSON('story.json').then((story) => {
  addHtmlToPage(story.heading);
  return story.chapterUrls.reduce((sequence, chapterUrl) => {
    return sequence.then(() => {
      return getJSON(chapterUrl);
    }).then((chapter) => {
      addHtmlToPage(chapter.html);
    });
  }, Promise.resolve());
}).then(() => {
  addTextToPage("All done");
}).catch((err) => {
  addTextToPage('Argh, broken: ' + err.message);
}).then(() => {
  document.querySelector('.spinner').style.display = 'none';
});

// parallel downloading, but display only after all downloaded
getJSON('story.json').then((story) => {
  addHtmlToPage(story.heading);

  return Promise.all(story.chapterUrls.map(getJSON));
}).then((chapters) => {
  chapters.forEach((chapter) => {
    addHtmlToPage(chapter.html);
  });
  addTextToPage('All done');
}).catch((err) => {
  addTextToPage('Argh, broken: ' + err.message);
}).then(() => {
  document.querySelector('.spinner').style.display = 'none';
});

// parallel downloading, display chapter 1 after this chapter downloaded
getJSON('story.json').then((story) => {
  addHtmlToPage(story.heading);
  return story.chapterUrls.map(getJSON).reduce((sequence, chapterPromise) => {
    return sequence.then(() => {
      return chapterPromise;
    }).then((chapter) => {
      addHtmlToPage(chapter.html);
    });
  }, Promise.resolve());
}).then(() => {
  addTextToPage('All done');
}).catch((err) => {
  addTextToPage('Argh, broken: ' + err.message);
}).then(() => {
  document.querySelector('.spinner').style.display = 'none';
});

// add generator
function spawn(generatorFunc) {
  function continuer(verb, arg) {
    var result;
    try {
      result = generator[verb](arg);
    } catch(err) {
      return Promise.reject(err);
    }
    if (result.done)
      return result.value;
    else
      return Promise.resolve(result.value).then(onFufilled, onRejected);
  }
  var generator = generatorFunc();
  var onFulfilled = continuer.bind(continuer, 'next');
  var onRejected = continure.bind(continuer, 'throw');
  return onFulfilled();
}

spawn(function *() {
  try {
    let story = yield getJSON('story.json');
    addHtmlToPage(story.heading);

    let chapterPromises = story.chapterUrls.map(getJSON);
    for (let chapterPromise of chapterPromises) {
      let chapter = yield chapterPromise;
      addHtmlToPage(chapter.html);
    }
    addTextToPage('All done');
  }
  catch (err) {
    addTex('Argh, broken: ' + err.message);
  }
  document.querySelector('.spinner').style.display = 'none';
});
