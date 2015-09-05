var arr = [1, [[2, 3], 4], [5, 6]];

var flat = function* (a) {
  var length = a.length;
  // can't use a.forEach(because yield can not exists in 普通函数)
  for(let i=0; i<length; i++) {
    let item = a[i];
    if(typeof item != 'number') {
      yield* flat(item);
    } else {
      yield item;
    }
  }
};

for(let f of flat(arr))
  console.log(f);


// 内部捕获Exception

var g = function* () {
    while (true) {
        try {
            yield;
        } catch (e) {
            if (e != 'a') {
                throw e;
            }
            console.log('内部捕获', e);
        }
    }
};

var i = g();
i.next();

try {
    i.throw('a');
    i.throw('b');
} catch (e) {
    console.log('外部捕获', e);
}
// 内部捕获 a
// 外部捕获 b


//这种函数体内捕获错误的机制，大大方便了对错误的处理。如果使用回调函数的写法，想要捕获多个错误，就不得不为每个函数写一个错误处理语句。

foo('a', function (a) {
    if (a.error) {
        throw new Error(a.error);
    }

    foo('b', function (b) {
        if (b.error) {
            throw new Error(b.error);
        }

        foo('c', function (c) {
            if (c.error) {
                throw new Error(c.error);
            }

            console.log(a, b, c);
        });
    });
});

//使用Generator函数可以大大简化上面的代码。

function* g(){
  try {
        var a = yield foo('a');
        var b = yield foo('b');
        var c = yield foo('c');
    } catch (e) {
        console.log(e);
    }
  console.log(a, b, c);
}

//如果Generator函数内部没有定义catch，那么throw方法抛出的错误，将被函数体的catch捕获。

function *foo() { }

var it = foo();
try {
  it.throw( "Oops!" );
} catch (err) {
    console.log( "Error: " + err ); // Error: Oops!
}
//上面代码中，foo函数内部没有任何语句，throw抛出的错误被函数体外的catch捕获。





