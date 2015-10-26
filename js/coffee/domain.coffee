domain = require 'domain'

d = domain.create()

d.on 'error', console.log.bind console

# Enter this domain
d.run -> console.log process.domain is d

# domain has now exited
