// promisify :: (a -> (Error -> b -> ()) -> ()) -> (a -> Promise b)
function promisify(fn, receiver) {
  return function() {
    var slice = Array.prototype.slice,
        args = slice.call(arguments, 0, fn.length - 1),
        promise = new Promise((resolve, reject) => {
          args.push(() => {
            var results = slice.call(arguments),
                error = results.shift();
            if (error) reject(error);
            else resolve(results);
          });
          fn.apply(receiver, args);
        });
    return promise;
  };
}


// list :: [Promise a] -> Promise [a]
function list(promises) {
  return new Promise((resolve, reject) => {
    let results = [], done = 0;
    promises.forEach((promise, i) => {
      promise.then(
        (result) => {
          results[i] = result;
          done += 1;
          if (done == promises.length) {
            resolve(results);
          }
        },
        (error) => {
          reject(error);
        });
    });
    if (promises.length === 0)
      resolve(results);
  });
}                                
                                 
var fs = require('fs');
var fs_stat = promisify(fs.stat);
var sp = ['/Users/zw/abc1.txt', '/Users/zw/dbdump', '/Users/zw/bupt48.pdf'].map(fs_stat);
// for (let p of sp)
//   p.then((result) => { console.log(result); });

let statPromises = list(sp);
statPromises.then((stats) => {
  stats.forEach((stat) => { console.log(stat); });
});


// functions in async's equivalents:
async.map(inputs, fn, (error, results) {});
// ===
list(inputs.map(promisify(fn))).then((results) => {}, (error) => {});

async.mapSeries(dirs, fs.rmdir, (error) => {});
// ===
let fs_rmdir = promisify(fs.rmdir);
let rm_rf = dirs.reduce((promise, path) => {
  return promise.then(() => {return fs_rmdir(path);});
}, unit());
rm_rf.then(() => {}, (error) => {});

function unit(a) {
  return new Promise((resolve, reject) => {
    resolve(a);
  });
}                 

let LazyPromise = (factory) => {
  this._factory = factory;
  this._started = false;
};

util.inherits(LazyPromise, Promise);

LazyPromise.prototype.then = () => {
  if (!this._started) {
    this._started = true;
    let self = this;
    this._factory((error, result) => {
      // todo, confine ES6 Promise protocol
      if (error) self.reject(error);
      else self.resolve(result);
    });
  }
  return Promise.prototype.then.apply(this, arguments);
};

const DELAY = 1000;

let Module = (name, deps, factory) => {
  this._factory = (callback) => {
    list(deps).then((apis) => {
      console.log('-- module LOAD: ' + name);
      setTimeout(() => {
        console.log('-- module done: ' + name);
        let api = factory.apply(this, apis);
        callback(null, api);
      }, DELAY);
    });
  };
};

util.inherits(Module, LazyPromise);











