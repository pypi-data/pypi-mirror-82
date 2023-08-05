# Welcome to `rebl` - a Regular Expression Based Linter.

Linters are thoroughly useful tools in a bid to improve code quality. However typically their behaviour is fixed or they are difficult to extend.

While one can use `grep` to scan a file for a pattern, when scanning a file for many patterns this gets either slow (because the file is scanned once per pattern) or unmaintainable (as the patterns get very, very long indeed).

`rebl` is a small linter which seeks to balance the simplicity of `grep` with the usefulness of a regular linter.

# Aren't regular expressions unsuitable to deal with language syntax?

Absolutely. This linter was developed with the full understanding that line-based regular expressions have such limitations. This linter solidly intends to provide 80% usability with 20% of the effort.

# Stuff you need to know

The pattern configuration file for this linter is a python module. Why should you care? For two reasons -

- the file lives in its own directory, and
- that directory should also contain an empty `__init__.py` file.

The default pattern configuration file is kept in `(path of rebl)/.reblrc/config.py` but additional paths will be searched (see below).

There are two ways to override the default path; one is to specify `--config=/absolute/path/to/config.py` on the command line. The other is to have a file called `.reblrc` containing `--config=relative/path/to/config.py`. Note that if a file `.reblrc` isn't found in the current working directory, `rebl` will look in the parent directory. If no `.reblrc` file is found anywhere it proceeds checking further paths. The `relative/path/to/config.py` is relative to the directory where the `.reblrc` file was found.

If no pattern configuration is specified, `rebl` will look for one
- in the current working directory, then checking parent directories (project- or multi-project config - likely to hit user's home directory)
- in the rebl program directory (user-wide config)
- in `/etc/rebl/config.py` (i.e. system wide config)

# Example pattern configuration
For your convenience an example pattern configuration is provided in the .reblrc directory of this repository. A symbolic link `_reblrc` is provided to make it visible.

Example config:

```
patterns = {}
patterns['.py'] = {
  "HW0025": (
    "No need for exc_info when using log.exception",
    ["log.exception", "exc_info"],[],[] ),
}
```
where

- .py is the file extension to which the pattern applies
- HW0025 is pattern key, must be unique for each pattern Fist char is confidence (HML for High, Medium, Low) Second char is error level (EWI for Error, Warning, Info) Next set of digits is the rest of the pattern unique identifier
- String given on the next line is the user friendly linter message, 1 line
- next line has 3 lists, the "all of", "any of" and "none of" lists.

  A line flags up when

  - it matches all of the regexes in the "all of" list
  - it matches any of the regexes in the "any of" list
  - it matches none of the regexes in the "none of" list.

  Regexes are automatically anchored.

  This means that a pattern `hello` will match any line containing the word "hello" - it is automatically rewritten to `"^.*hello.*$"` to make `rebl` behave more like `grep`.

## Advanced detection

All of, any of and none of lists can be combined.

If that's not enough, If all three lists are empty, rebl will look for a function called `detect_[ext]_[pattern key]` which accepts filename and line arguments - for example,

```
def detect_py_HW0025(filename, line):
    return True if 'hello' in line else False
```

will be called for each line and should

- return True on match; or
- return False on no match.

## Fixers

If a function `fix_[ext]_[pattern key]` exists, this can be used to
perform fixes in batch.
for example,

```
def fix_py_MW0049(filename, line):
    return line.replace("import csv", "import unicodecsv as csv")
```

would automatically be invoked if `rebl` is run with `--fix` and lines match the pattern as given for pattern key MW0049.

## Line hook/context collector

It is possible to define a line hook to collect context on every line, e.g.

```
def linehook_<ext>(filename, lines, linenum, context):
```

This will be called on every line if defined - permits collecting state data such as current function name, errors found thusfar, whatever.

As the linehook is called frequently, ideally it should be kept light; that is, try to avoid too many loops in here.

State should be kept in dict `context` - this dict is reset each file.
