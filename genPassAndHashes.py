import createPasswordsThreaded


def gen_pass_and_hashes():
    password = createPasswordsThreaded.create_random_password()
    return password


if __name__ == "__main__":
    gen_pass_and_hashes()

