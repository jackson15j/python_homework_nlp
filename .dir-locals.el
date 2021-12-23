;;; Directory Local Variables
;;; For more information see (info "(emacs) Directory Variables")

((nil . ((compile-command . "cd $(git rev-parse --show-toplevel) && poetry run black .;pycodestyle .;flake8 .;mypy .;pytest")))
 (python-mode . ((compile-command . "cd $(git rev-parse --show-toplevel) && poetry run black .;pycodestyle .;flake8 .;mypy .;pytest"))))
