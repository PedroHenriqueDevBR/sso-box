import ldap

# Install to work
# sudo apt-get install python3-dev libxml2-dev libxslt1-dev zlib1g-dev libsasl2-dev libldap2-dev build-essential libssl-dev libffi-dev libmysqlclient-dev libjpeg-dev libpq-dev libjpeg8-dev liblcms2-dev libblas-dev libatlas-base-dev


def authenticate(address, username, password):
    try:
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        connection = ldap.initialize(address)
        connection.protocol_version = ldap.VERSION3
        connection.simple_bind_s(username, password)
        return True
    except ldap.INVALID_CREDENTIALS:
        return False
    except ldap.LDAPError as error:
        print("Error:", error)
        return False
    finally:
        connection.unbind_s()


if __name__ == "__main__":
    username = input("Username: ")
    password = input("Password: ")
    address = "ldap://192.168.0.18"
    print(authenticate(address=address, username=username, password=password))
