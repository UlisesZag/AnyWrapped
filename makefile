windows:
	del bin\AnyWrapped.exe
	pyinstaller --onefile --paths .venv\Lib\site-packages anywrapped\__main__.py
	move dist\__main__.exe bin\AnyWrapped.exe
	rmdir dist

setup: requirements.txt
	python -m venv .venv
	.venv\Scripts\activate
	pip install -r requirements.txt

venvactivate: .venv\Scripts\activate
	.venv\Scripts\activate