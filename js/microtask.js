function test1() {
  console.log('script start');

  setTimeout(() => {
    console.log('setTimeout')
  }, 0);

  Promise.resolve().then(() => {
    console.log('promise1')
  }).then(() => {
    console.log('promise2')
  });

  console.log('script end');
}

let functions = {test1}

let i = process.argv[2]
functions['test' + i]()
