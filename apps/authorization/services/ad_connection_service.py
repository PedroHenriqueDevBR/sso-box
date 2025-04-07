from typing import Optional

import ldap
from django.http.request import HttpRequest

from apps.authorization.services.authenticator_service import AuthenticatorService


class ADConnectionService:
    def __init__(
        self,
        address: str,
        user_dn: Optional[str],
        user_dn_password: Optional[str],
    ):
        self.address = address
        self.user_dn = user_dn
        self.user_dn_password = user_dn_password
        self.base_dn = ""
        self.connection = None

    def authenticate(
        self,
        request: HttpRequest,
        username: str,
        password: str,
    ) -> bool:
        REQUIRE_CERT = ldap.OPT_X_TLS_REQUIRE_CERT  # type: ignore
        TLS_NEVER = ldap.OPT_X_TLS_NEVER  # type: ignore
        VERSION = ldap.VERSION3  # type: ignore
        SCOPE = ldap.SCOPE_SUBTREE  # type: ignore
        try:
            ldap.set_option(REQUIRE_CERT, TLS_NEVER)

            self.connection = ldap.initialize(self.address)
            self.connection.protocol_version = VERSION
            self.connection.simple_bind_s(self.user_dn, self.user_dn_password)

            search_filter = f"(sAMAccountName={username})"
            result = self.connection.search_s(
                self.base_dn,
                SCOPE,
                search_filter,
                ["distinguishedName"],
            )

            if result is None:
                print(">>> User not found <<<")
                raise ConnectionRefusedError()

            user_founded = None
            if len(result) != 1:
                for item in result:
                    if item[0] is not None:
                        user_founded = item[0]
                        break

            if user_founded is None:
                print(">>> User not found or multiple users found. <<<")
                raise ConnectionRefusedError()

            print(f"Found user DN: {user_founded}")
            user_connection = ldap.initialize(self.address)
            user_connection.protocol_version = VERSION
            user_connection.simple_bind_s(user_founded, password)

            authenticator = AuthenticatorService(request=request)
            authenticator.authenticate_user(username=username)
            return True
        except ldap.INVALID_CREDENTIALS:
            print(">>> Invalid credencials <<<")
            raise ConnectionRefusedError()
        except ldap.SERVER_DOWN:
            print(">>> Server down <<<")
            raise ConnectionError()
        except ldap.LDAPError as error:
            print("LDAP error: " + str(error))
            raise ConnectionRefusedError()
        except Exception as error:
            raise ConnectionRefusedError()
        finally:
            if self.connection is not None:
                self.connection.unbind_s()
