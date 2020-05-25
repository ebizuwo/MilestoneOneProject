echo "creating virtual environment"
python3 -m venv venv
echo "done"

echo "sourcing the virtual environment"
source venv/bin/activate

echo "install requirements"
pip install -r requirements.txt

echo "setting the ipykernel"
python -m ipykernel install --user --name=venv

echo "all done"
source venv/bin/activate