from cmath import e
from xmlrpc.client import Boolean
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from ..resourcesGuard import for_all_methods, reject_invalid
import sys
from flask import current_app
from importlib import resources

cypher = {
    f: resources.read_text(__package__, f)
    for f in resources.contents(__package__)
    if resources.is_resource(__package__, f) and f.split(".")[-1] == "cyp"
}


@for_all_methods(reject_invalid)
class userDAO:
    def __init__(self, driver):
        self.driver = driver

    def list_userId(self):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query)
            try:
                rows = [record for record in result]
                return [row["user.userId"] for row in rows]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def is_userId_used(self, userId) -> bool:
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, userId=userId)
            try:
                for record in result:
                    return record["Predicate"]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def create_user(self, userId, userName, email, password):
        ph = PasswordHasher()
        saltedHash = ph.hash(password)

        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
                userId=userId,
                userName=userName,
                email=email,
                saltedHash=saltedHash,
            )
            try:
                rows = [record for record in result]
                return dict(rows[0]["user"].items())
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def update_user(self, user, userId, userName, email):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            if user["email"] != email:
                result = tx.run(
                    "MATCH (user:User {email: $email}) RETURN user",
                    email=email,
                )
                result = [record["user"] for record in result]
                if len(result) > 0:
                    from ..resourcesGuard import InvalidRequest

                    raise InvalidRequest(
                        "Email already taken by another user. Contact admin if your email is taken by others."
                    )
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
                userId=userId,
                userName=userName,
                email=email,
            )
            try:
                rows = [record for record in result]
                return dict(rows[0]["user"].items())
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def assign_user_role(self, userId, role, message=""):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
                userId=userId,
                role=role,
                message=message,
                REQUIRE_USER_VERIFICATION=current_app.config[
                    "REQUIRE_USER_VERIFICATION"
                ],
            )
            return [
                {
                    "user": dict(record["user"].items()),
                    "permission_grant": dict(record["permission_grant"].items()),
                    "permission": dict(record["permission"].items()),
                }
                for record in result
            ][0]

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def remove_user_role(
        self,
        userId,
        role,
    ):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, userId=userId, role=role)
            return [
                {
                    "user": dict(record["user"].items()),
                    "permission_grant": dict(record["permission_grant"].items()),
                    "permission": dict(record["permission"].items()),
                }
                for record in result
            ][0]

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def authenticate_user(self, userId, password):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, userId=userId)
            rows = [record for record in result]
            if len(rows) > 0:
                saltedHash = rows[0]["hash"]
                ph = PasswordHasher()
                if ph.verify(saltedHash, password):
                    return dict(rows[0]["user"].items())
                else:
                    return None

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def merge_oidc_user(self, upn):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, email=upn, userId=upn.split("@")[0])
            rows = [record for record in result]
            if len(rows) > 0:
                return dict(rows[0]["user"].items())
            else:
                return None

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def get_user_permission(self, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, userId=userId)
            permission = dict()
            for row in [record for record in result]:
                for key, value in row["permissions"].items():
                    if key not in permission:
                        if isinstance(value, bool):
                            permission[key] = value
                        elif isinstance(value, str):
                            permission[key] = [value]
                    else:
                        if isinstance(value, bool):
                            if not permission[key]:
                                permission[key] = value
                        elif isinstance(value, str):
                            l = [value]
                            permission[key] = permission[key] + l
            return permission

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def get_user(self, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, userId=userId)
            try:
                rows = [record for record in result]
                return dict(rows[0]["user"].items())
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def try_activate_user_w_hash(self, hash):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, hash=hash)
            try:
                return [
                    {
                        "user": dict(record["user"].items()),
                        "activation": dict(record["activation"].items()),
                    }
                    for record in result
                ][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def reset_user_password(self, userId, oldPassword, newPassword):
        fname = sys._getframe().f_code.co_name
        try:
            self.authenticate_user(userId=userId, password=oldPassword)
        except VerifyMismatchError as e:
            from ..resourcesGuard import InvalidRequest

            raise InvalidRequest("The old password is wrong.")

        def _query(tx):
            ph = PasswordHasher()
            newSaltedHash = ph.hash(newPassword)
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
                userId=userId,
                saltedHash=newSaltedHash,
            )
            rows = [record for record in result]
            return dict(rows[0]["user"].items())

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def try_reset_user_password_w_hash(self, userId, hash, password):
        ph = PasswordHasher()
        saltedHash = ph.hash(password)

        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
                userId=userId,
                hash=hash,
                saltedHash=saltedHash,
            )
            try:
                rows = [record for record in result]
                return dict(rows[0]["user"].items())
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def set_user_activation_hash(self, userId, email):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            ph = PasswordHasher()
            result = tx.run(
                query,
                userId=userId,
                email=email,
                hash=ph.hash(userId + "@" + email).split("$")[-1],
            )
            try:
                rows = [record for record in result]
                return dict(rows[0]["activation"].items())
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def set_user_renew_password_hash(self, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            ph = PasswordHasher()
            result = tx.run(query, userId=userId, hash=ph.hash(userId).split("$")[-1])
            try:
                return [
                    {
                        "user": dict(record["user"].items()),
                        "token": dict(record["token"].items()),
                    }
                    for record in result
                ][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)
