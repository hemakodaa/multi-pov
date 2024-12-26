from commands import generate_command

url_example = "https://www.youtube.com/watch?v=gOQKbJyLyuk"


def main():
    generate_command(url_example, "53:00", "54:00")


if __name__ == "__main__":
    main()
