# Create virtual environment in .venv folder
python -m venv .venv

# Activate the venv
.\.venv\Scripts\Activate.ps1

# Install all required packages for the project
pip install -r requirements.txt


echo "Installation of module graphanime ...."
cd graphanime
python setup.py install
cd ..
echo "End Installation"