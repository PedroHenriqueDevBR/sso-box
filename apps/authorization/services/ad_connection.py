import ldap


class ADConnection:
    def __init__(self, address: str):
        self.address = address
        self.connection = None

    def authenticate(self, username: str, password: str) -> bool:
        try:
            ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
            self.connection = ldap.initialize(self.address)
            self.connection.protocol_version = ldap.VERSION3
            self.connection.simple_bind_s(username, password)
            return True
        except ldap.INVALID_CREDENTIALS:
            print(">>> Invalid credencials <<<")
            raise ConnectionRefusedError()
        except ldap.SERVER_DOWN:
            print(">>> Server down <<<")
            raise ConnectionError()
        except ldap.LDAPError as error:
            if type(error.message) == dict and error.message.has_key("desc"):
                print("LDAP error: " + error.message["desc"])
            else:
                print("LDAP error: " + error)
            raise ConnectionRefusedError()
        finally:
            if self.connection is not None:
                self.connection.unbind_s()
