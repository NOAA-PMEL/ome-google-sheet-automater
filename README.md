# ome-google-sheet-automater
A repo that includes code to automate the concatenation of google sheets into a single master google sheet. It includes a master extraction sheet, master sequencing sheet, and master sample sheet.

## To Run
1. install Conda environment and requirements (using `environment.yaml`)
2. Get Google authentication credentials and dowload json file and save as `credentials.json`. Must save it as this so `.gitignore` will ignore it. Warning: DO NOT PUSH credentials to github.
3. Create `config.yaml` file in the `configs` folder
4. Run `main.py --config <path to config file> --creds <path to json credentials file>`
5. Look at destination master sheet url and inspect for correctness.
