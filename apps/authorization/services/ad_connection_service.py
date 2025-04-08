from typing import Optional

import ldap
from django.http.request import HttpRequest

from apps.authorization.services.authenticator_service import AuthenticatorService
from datetime import datetime


class ADConnectionService:
    def __init__(
        self,
        address: str,
        user_dn: Optional[str],
        user_dn_password: Optional[str],
        base_dn: Optional[str],
    ):
        self.address = address
        self.user_dn = user_dn
        self.user_dn_password = user_dn_password
        self.base_dn = base_dn
        self.connection = None
        self.REQUIRE_CERT = ldap.OPT_X_TLS_REQUIRE_CERT  # type: ignore
        self.TLS_NEVER = ldap.OPT_X_TLS_NEVER  # type: ignore
        self.VERSION = ldap.VERSION3  # type: ignore
        self.SCOPE = ldap.SCOPE_SUBTREE  # type: ignore

    def close_connection(
        self,
        connection: ldap.ldapobject.LDAPObject,  # type: ignore
    ) -> None:
        try:
            connection.unbind_s()
        except Exception as e:
            print(f"Error closing connection: {e}")

    def authenticate(
        self,
        request: HttpRequest,
        username: str,
        password: str,
    ) -> bool:
        try:
            ldap.set_option(self.REQUIRE_CERT, self.TLS_NEVER)

            self.connection = ldap.initialize(self.address)
            self.connection.protocol_version = self.VERSION
            self.connection.simple_bind_s(self.user_dn, self.user_dn_password)

            search_filter = f"(sAMAccountName={username})"
            result = self.connection.search_s(
                self.base_dn,
                self.SCOPE,
                search_filter,
                ["distinguishedName"],
            )
            self.close_connection(self.connection)

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
            user_connection.protocol_version = self.VERSION
            user_connection.simple_bind_s(user_founded, password)
            self.close_connection(user_connection)

            authenticator = AuthenticatorService(request=request)
            authenticator.authenticate_user(username=username)
            return True
        except ldap.INVALID_CREDENTIALS:  # type: ignore
            print(">>> Invalid credencials <<<")
            raise ConnectionRefusedError()
        except ldap.SERVER_DOWN:  # type: ignore
            print(">>> Server down <<<")
            raise ConnectionError()
        except ldap.LDAPError as error:  # type: ignore
            print("LDAP error: " + str(error))
            raise ConnectionRefusedError()
        except Exception as error:
            raise ConnectionRefusedError()
        finally:
            if self.connection is not None:
                self.connection.unbind_s()

    def search_users(self, search: str) -> list[dict]:
        try:
            self.connection = ldap.initialize(self.address)
            self.connection.protocol_version = self.VERSION
            self.connection.simple_bind_s(self.user_dn, self.user_dn_password)

            search_filter = f"(|(sAMAccountName=*{search}*)(displayName=*{search}*))"
            result = self.connection.search_s(
                self.base_dn,
                self.SCOPE,
                search_filter,
                [
                    "distinguishedName",  # dn - AD path to reference user
                    "displayName",  # name
                    "sAMAccountName",  # username
                    "whenCreated",  # created_at
                    "lastLogon",  # last_login
                    "userAccountControl",  # is_enabled
                    "mail",  # email
                ],
            )
            self.close_connection(self.connection)

            if result is None:
                print(">>> User not found <<<")
                return []

            users = []
            for item in result:
                if item[0] is not None:
                    user_attrs = item[1]
                    user = {
                        "dn": user_attrs.get("distinguishedName", [b""])[0].decode(
                            "utf-8"
                        ),
                        "name": user_attrs.get("displayName", [b""])[0].decode("utf-8"),
                        "username": user_attrs.get("sAMAccountName", [b""])[0].decode(
                            "utf-8"
                        ),
                        "created_at": user_attrs.get("whenCreated", [b""])[0].decode(
                            "utf-8"
                        ),
                        "last_login": user_attrs.get("lastLogon", [b""])[0].decode(
                            "utf-8"
                        ),
                        "mail": user_attrs.get("mail", [b""])[0].decode("utf-8"),
                        "is_enabled": int(
                            user_attrs.get("userAccountControl", [b"0"])[0].decode(
                                "utf-8"
                            )
                        )
                        & 2
                        == 0,
                        "server": self.address,
                    }
                    users.append(user)

            return self.format_users_data(users)
        except ldap.INVALID_CREDENTIALS:  # type: ignore
            return []

    def format_users_data(self, users: list) -> list[dict]:
        formatted_users = []
        for user in users:
            created_at = ""
            last_login = ""

            if user["created_at"]:
                created_at = self.convert_ldap_date(user["created_at"])
            if user["last_login"]:
                last_login = self.convert_ldap_date(user["last_login"])

            formatted_user = {
                "dn": user["dn"],
                "name": user["name"],
                "username": user["username"],
                "created_at": created_at,
                "last_login": last_login,
                "is_enabled": user["is_enabled"],
                "server": user["server"],
                "mail": user["mail"],
            }
            formatted_users.append(formatted_user)
        return formatted_users

    def convert_ldap_date(self, date_string: str) -> str:
        date_format = "%d/%m/%Y"
        try:
            if not date_string or date_string == "0":
                return ""

            if "Z" not in date_string:
                timestamp = int(date_string)
                seconds_since_1601 = timestamp / 10000000  # Convert to seconds
                epoch_adj = 11644473600  # Seconds between 1601-01-01 and 1970-01-01
                unix_timestamp = seconds_since_1601 - epoch_adj
                return datetime.fromtimestamp(unix_timestamp).strftime(date_format)

            return datetime.strptime(date_string, "%Y%m%d%H%M%S.0Z").strftime(
                date_format
            )
        except:
            return ""
