"""flask-smorest overrides

This module customizes and republishes flask-smorest stuff
"""
import http

from flask_smorest import Api as FSApi, Blueprint as FSBlueprint, abort  # noqa

from pyodhean_server.auth import auth


class Api(FSApi):
    def __init__(self, app=None, *, spec_kwargs=None):
        spec_kwargs = spec_kwargs or {}
        super().__init__(app, spec_kwargs=spec_kwargs)
        self.spec.components.security_scheme(
            "BasicAuthentication", {"type": "http", "scheme": "basic"})


class Blueprint(FSBlueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._prepare_doc_cbks.append(self._prepare_auth_doc)

    @staticmethod
    def login_required(func):
        # Note: we don't use "role" and "optional" parameters in the app,
        # we always call login_required with not parameter
        func = auth.login_required(func)
        getattr(func, "_apidoc", {})["auth"] = True
        return func

    @staticmethod
    def _prepare_auth_doc(doc, doc_info, **kwargs):
        if doc_info.get("auth", False):
            doc.setdefault("responses", {})["401"] = http.HTTPStatus(401).name
            doc["security"] = [{"BasicAuthentication": []}]
        return doc
