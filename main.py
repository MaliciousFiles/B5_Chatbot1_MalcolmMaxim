# Makes repl run our main.py when we click run
from src.main import main

# Skip intro... for now
try:
    main(skip_intro=True)
except (KeyboardInterrupt, EOFError):
    print("\nThank you for talking to me!")