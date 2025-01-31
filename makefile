windows:
	del bin\AnyWrapped.exe
	cd anywrapped
	pyinstaller --onefile --paths .venv\Lib\site-packages --add-data assets:assets --noconsole anywrapped.py 
	move dist\anywrapped.exe bin\AnyWrapped.exe
	rmdir dist

setup: requirements.txt
	python -m venv .venv
	.venv\Scripts\activate
	pip install -r requirements.txt

venvactivate: .venv\Scripts\activate
	.venv\Scripts\activate