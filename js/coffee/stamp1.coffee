EventEmitter = require('events').EventEmitter
redisPool = require 'sol-redis-pool'
stamp = require 'stampit'

defaultPoolOpts =
  max: 16
  min: 4

acquire = (pool, priority) ->
  new Promise (resolve, reject) ->
    pool.acquire (error, conn) ->
      if error then reject error
      else resolve conn
    ,
    priority

get = (conn, key) -> promisify(conn.get, conn) key

set = (conn, key, value, ttl) ->
  if typeof ttl is 'number'
    promisify(conn.setex, conn) key, ttl, value
  else
    promisify(conn.set, conn) key, value
  
del = (conn, key) -> promisify(conn.del, conn) key

keys = (conn, pattern) -> promisify(conn.keys, conn) pattern
  

factory = stamp
  .methods EventEmitter.prototype
  .init (args, instance, stamp) ->
    options = args[0] or {}
    option.host = options.host or 'localhost'
    options.port = options.port 6379

    poolOpts = args[1].poolOpts or defaultPoolOpts
    defaultTtl = poolOpts.ttl

    pool = redisPool options poolOpts
    pool.on 'error', @emit.bind @, 'error'

    functions =
      'get': (conn, key) ->
        data = yield get conn, key
        data = JSON.parse data if data
        data

      'set': (conn, key, value, ttl) ->
        ttl = ttl or defaultTtl
        yield set conn, key, JSON.stringify value, ttl

      'del': (conn, key) ->
        conn.del key

      'keys': (conn, pattern) ->
        pattern = pattern or '*'
        yield keys conn, pattern

      'reset': (conn) ->
        for key in keys conn, '*'
          conn.del key
        return

    for name, func of functions
      @['name'] = (args...) ->
        conn = yield acquire pool
        args.unshift conn
        try
          ret = func.apply @, args
        finally
          pool.release conn
        ret
        
f = factory()
