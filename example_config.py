# Rename this file to config.py once you're done with setting the server values.


server_ip = "104.236.202.106"  # IP of the server you're deploying to
server_user = "newuser"  # Username of the user on the remote server
server_password = "root"  # password of the user above


def create_password():
    import hashlib

    new_password = raw_input("New password:")
    password = hashlib.sha512(new_password).hexdigest()
    print "Set the password_hash to:\n{}".format(password)


def create_secret():
    import os

    print "Set flask secret_key to:\n{}\n\n".format(repr(os.urandom(24)))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--create_password", help="Generate new password hash to be used", action="store_true")
    parser.add_argument("--create_secret", help="Generate new secret key to be used by flask", action="store_true")
    args = parser.parse_args()

    if args.create_password:
        create_password()

    if args.create_secret:
        create_secret()
