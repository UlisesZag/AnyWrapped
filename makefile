Windows:
	del .\AnyWrapped.exe
	pyinstaller --onefile --paths .venv\Lib\site-packages __main__.py
	move dist\__main__.exe AnyWrapped.exe
	rmdir dist

Setup:
	python -m venv .venv
	.venv\Scripts\activate
	pip install -r requirements.txt

VenvActivate:
	.venv\Scripts\activate