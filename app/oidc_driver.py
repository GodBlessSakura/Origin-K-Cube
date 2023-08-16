from oic.oic import Client
from oic.utils.authn.client import CLIENT_AUTHN_METHOD
from flask import current_app, g
from oic import rndstr
from oic.utils.http_util import Redirect
from flask import session, request
import time
from functools import wraps


class oidcError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


def init_oidc():
    # state is for anti-csrf, nonce is for anti-reply attack
    session["oidc_state"] = rndstr()
    session["oidc_nonce"] = rndstr()
    session["oidc_state_time"] = time.time()


def oidc_validate(aresp):
    try:
        assert time.time() - session["oidc_state_time"] < 600
    except AssertionError:
        raise oidcError("Login atempt timeout. Try login again.")
    except KeyError:
        raise oidcError("Login atempt not initialized. Try login again.")
    try:
        assert aresp["state"] == session["oidc_state"]
    except AssertionError:
        raise oidcError("Login atempt timeout. Try login again.")
    except KeyError:
        raise oidcError("Login atempt not initialized. Try login again.")
    try:
        assert aresp["id_token"]["nonce"] == session["oidc_nonce"]
    except AssertionError:
        raise oidcError("Login session mismatch. Try login again.")
    except KeyError:
        raise oidcError("Login atempt not initialized. Try login again.")


def oidc_args():
    from oic.oic.message import ClaimsRequest, Claims

    claims_request = ClaimsRequest(
        id_token=Claims(),
        userinfo=Claims(
            polyuCurrentStaff={"essential": True},
            polyuCurrentStudent={"essential": True},
        ),
    )
    return {
        "response_type": ["id_token"],
        "scope": ["openid", "profile"],
        "nonce": session["oidc_nonce"],
        "redirect_uri": current_app.config["OIDC"]["redirect_uris"][0],
        "state": session["oidc_state"],
        "claims": claims_request,
    }


def get_oidc_driver() -> Client:
    if "oidc_driver" not in g:
        g.oidc_driver = Client(client_authn_method=CLIENT_AUTHN_METHOD)
        g.oidc_driver.provider_config(current_app.config["OIDC"]["issuer"])
        from oic.oic.message import RegistrationResponse

        info = {
            "client_id": current_app.config["OIDC"]["client_id"],
            "client_secret": current_app.config["OIDC"]["client_secret"],
        }
        client_reg = RegistrationResponse(**info)
        g.oidc_driver.store_registration_info(client_reg)
    return g.oidc_driver


def redirect_to_oidc_login():
    init_oidc()
    auth_req = get_oidc_driver().construct_AuthorizationRequest(
        request_args=oidc_args()
    )
    login_url = auth_req.request(get_oidc_driver().authorization_endpoint)
    print(login_url)
    return Redirect(login_url)


def get_user_id_token():
    from oic.oic.message import AuthorizationResponse

    aresp = get_oidc_driver().parse_response(
        AuthorizationResponse,
        info=request.query_string.decode("utf-8"),
        sformat="urlencoded",
    )
    oidc_validate(aresp)
    get_oidc_driver().do_access_token_request(
        state=session["oidc_state"],
        request_args=oidc_args(session["oidc_state"]),
    )
    return get_oidc_driver().do_user_info_request(state=aresp["state"])

def parse_authorization_query(response):
    from oic.oic.message import AuthorizationResponse
    try:
        aresp = get_oidc_driver().parse_response(AuthorizationResponse, info=response,
                              sformat="urlencoded")
    except:
        raise oidcError("Login atempt failed. Try login again.")
    oidc_validate(aresp)
    return aresp
    #jwt_assert(jwt)



def init_app(app):
    app.teardown_appcontext(close_oidc_driver)


def close_oidc_driver(e=None):
    oidc_driver = g.pop("oidc_driver", None)

    if oidc_driver is not None:
        pass
