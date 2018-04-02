#!/usr/bin/env python

import os
import jinja2
import webapp2

from models import Message

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))


class MainHandler(BaseHandler):#mostrarformulario
    def get(self):
        return self.render_template("hello.html")


class ResultHandler(BaseHandler):#peticionyenvio
    def post(self):
        n = self.request.get("some_name")
        e = self.request.get("some_email")
        t = self.request.get("some_text")

        if not n:
            n = "blank"
        if not e:
            e = "blank"

        msg = Message(name=n, email=e, text=t, created=cr)
        msg.put()

class EntriesHandler(BaseHandler):#mostrarentradas
    def get(self):
        all_entries = Message.query().fetch()
        params = {"everything": all_entries}
        return self.render_template("entries.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/result', ResultHandler),
    webapp2.Route('/entries', EntriesHandler)
], debug=True)
