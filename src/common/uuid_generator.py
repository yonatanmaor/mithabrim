from uuid import uuid4, UUID


def generate_uuid() -> UUID:
    return uuid4()


if __name__ == '__main__':
    print(generate_uuid())

