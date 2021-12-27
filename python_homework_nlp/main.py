def cli_parser():
    pass


def workflow(*args, **kwargs):
    pass


def main():
    # TODO: argparse
    parsed_args = cli_parser()
    # TODO: call main workflow.
    ret_val = workflow(**parsed_args)
    # TODO: Render results


if __name__ == "__main__":
    main()
