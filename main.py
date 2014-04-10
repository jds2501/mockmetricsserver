#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import jinja2

from google.appengine.ext import db

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Request(db.Model):
  body = db.TextProperty()
  bodyFile = db.TextProperty()
  remoteAddr = db.TextProperty()
  url = db.TextProperty(required=True)
  path = db.TextProperty()
  queryString = db.TextProperty()
  headers = db.TextProperty()
  cookies = db.TextProperty()

class MainHandler(webapp2.RequestHandler):

  def get(self):
    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render({}))

  def post(self):
    request = Request(body=str(self.request.body),
                      bodyFile=str(self.request.body_file),
                      remoteAddr=str(self.request.remote_addr),
                      url=str(self.request.url),
                      path=str(self.request.path),
                      queryString=str(self.request.query_string),
                      headers=str(self.request.headers),
                      cookies=str(self.request.cookies))
    request.put()

app = webapp2.WSGIApplication([
    ('/.*', MainHandler)
], debug=True)
