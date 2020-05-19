echo "creating virtual environment"
python3 -m venv venv
echo "done"

echo "sourcing the virtual environment"
source venv/bin/activate

echo "install requirements"
pip install -r requirements.txt

echo "pulling down the repo and initializing the directories"
git clone https://github.com/ebizuwo/MilestoneOneProject.git

echo "all done"