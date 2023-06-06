import ldap


class ADConnection:
    def __init__(self, address: str):
        self.address = address

    def authenticate(self, username: str, password: str):
        try:
            ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
            connection = ldap.initialize(self.address)
            connection.protocol_version = ldap.VERSION3
            connection.simple_bind_s(username, password)
            print("Authenticated")
            return True
        except ldap.INVALID_CREDENTIALS:
            print("Invalid credentials")
            return True
        except ldap.SERVER_DOWN:
            print("LDAP error: Server down")
        except ldap.LDAPError as e:
            if type(e.message) == dict and e.message.has_key("desc"):
                print("LDAP error: " + e.message["desc"])
            else:
                print("LDAP error: " + e)
            return False
        finally:
            print("LDAP closed connection")
            connection.unbind_s()
