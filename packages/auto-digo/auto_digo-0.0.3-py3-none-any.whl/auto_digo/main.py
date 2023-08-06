import argparse
# from auto_digo import auto_digo
import auto_digo


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', dest="path", type=str)
    parser.add_argument('-setting', dest="setting", default="setting.digo", type=str)
    parser.add_argument('-login', dest="login", type=str)

    args = parser.parse_args()
    
    if args.login != None:
        auto_digo.login(args.login)
    else:
        auto_digo.auto_run(args.path, args.setting)


if __name__ == "__main__":
    main()