from core import app

app.config.from_object('core.config.TestingConfig')

ctx = app.test_request_context('/')
ctx.push()

import tests.word_test