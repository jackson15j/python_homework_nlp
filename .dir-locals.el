;;; Directory Local Variables
;;; For more information see (info "(emacs) Directory Variables")

((nil . ((compile-command . "cd $(git rev-parse --show-toplevel) && poetry run black .;poetry run pycodestyle .;poetry run flake8 .;poetry run mypy .;poetry run pytest -vv")))
 (python-mode . ((compile-command . "cd $(git rev-parse --show-toplevel) && poetry run black .;poetry run pycodestyle .;poetry run flake8 .;poetry run mypy .;poetry run pytest -vv"))))
