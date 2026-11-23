"""Ways to confirm that the customer really is the customer."""


def authorize_sms() -> bool:
    print("  SMS code accepted")
    return True


def authorize_google() -> bool:
    print("  Google sign-in accepted")
    return True


def authorize_robot() -> bool:
    print("  not a robot")
    return True


def authorize_fingerprint() -> bool:
    print("  fingerprint matched")
    return True
