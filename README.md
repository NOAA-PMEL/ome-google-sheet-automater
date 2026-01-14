# ome-google-sheet-automater
A repo that includes code to automate the concatenation of google sheets into a single master google sheet. It includes a master extraction sheet, master sequencing sheet, and master sample sheet.

## To Run
1. Clone this repo
2. Open terminal and navigate to repo
3. install Conda environment and requirements (using `environment.yaml`)
4. Get Google authentication credentials and dowload json file and save as `credentials.json`. Must save it as this so `.gitignore` will ignore it. Warning: DO NOT PUSH credentials to github.
5. Create `config.yaml` file in the `configs` folder
6. Get the google authentication email address should be something like 'python-api@zalmanek-brynn.iam.gserviceaccount.com' and share each sheet you are wanting to concatenate with that email, including the destination sheet. This allows you to access them through the API.
7. Run `main.py --config <path to config file> --creds <path to json credentials file>` in the terminal.
8. Look at destination master sheet url and inspect for correctness.
