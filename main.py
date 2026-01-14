from modules.google_sheet_concatenator import GoogleSheetConcatenator
import argparse


def main():
    parser = argparse.ArgumentParser()

    # Just the two path arguments
    parser.add_argument('--config', type=str, help="Path to config.yaml")
    parser.add_argument('--creds', type=str, help="Path to credentials.json")

    args = parser.parse_args()

    GoogleSheetConcatenator(config_yaml=args.config, credentials=args.creds)


if __name__ == "__main__":
    main()
