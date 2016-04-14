Scripting Helper Library
========================

This is a collection of functions I use frequently when writing scripts for system adminstration.  Far and away the function I use most often is `process`, which accepts a shell command and returns a tuple containing (return code, standard out, standard error).

```
>>> from scripting import process
>>> process('uname')
(0, 'Linux\n', '')
>>> process('/bin/false')
(1, '', '')
```

The other tool in this repository that I wound up using a lot is [switchbranch](https://github.com/dmf24/pyscripting/blob/master/scripting/switchbranch.py).  I've included an sample installation guide below for anyone who wants to try it out.  

## switchbranch

This is an interactive tool to switch between branches in a git repository using a mini-menu.  Sometimes I find it more convenient (and fun to use) than tab-complete.  Running it gives you a menu that looks like the following, allowing you to use keys to move the cursor to the desired branch then hit enter to switch to it.  The asterisk indicates the current branch.

```
> branch1
  * branch2
  master
  NONE
```

Warning: this is an extremely simple program.  It does not use curses to update the terminal, it simply rewrites the entire buffer on every update.  There's also no package, no installer, and no versioning.

#### Setup guide

This is best used as an example, the steps are simple and you should modify them based on what you want.  Someday I will may try to create a legitimate python package that can be installed with pip.  Until then do something like this.

Create a fresh python virtualenv:

```
BASEDIR=$(pwd)
virtualenv venv01
```

Clone the pyscripting repo:

```
git clone git@github.com:dmf24/pyscripting.git
```

Symlink the scripting library from the virtualenv's site-packages:

```
ln -s pyscripting/scripting venv01/lib/python2.7/site-packages/scripting $BASEDIR/pyscripting/scripting
```

Replace `python2.6` with your python version.  You might be able to get the string using this:
```
VSTRING=$(venv01/bin/python -c "import sys; sys.stdout.write(set([x.split('/')[-2] for x in sys.path if x.endswith('site-packages')]).pop())")
ln -s $BASEDIR/pyscripting/scripting venv01/lib/$VSTRING/site-packages/scripting
```

Create an executable script:
```
mkdir $BASEDIR/bin
echo "$BASEDIR/venv01/bin/python $BASEDIR/pyscripting/scripting/switchbranch.py" > $BASEDIR/bin/git-switch-branch
chmod 755 $BASEDIR/bin/git-switch-branch

```


Create a new git repo, add a file, and create a couple of new branches:

```
git init btest
cd btest
echo file0 > file0
git add file0 && git commit -m "Adding file0"
git checkout -b branch1
echo file1 > file1
git add file1 && git commit -m "Adding file1"
git checkout master
git checkout -b branch2
echo file2 > file2
git add file2 && git commit -m "Adding file2"

git-switch-branch

> branch1
  * branch2
  master
  NONE

# Press "d" twice for master

  branch1
  * branch2
> master
  NONE

# Press "w" to twice to go back up to branch1

> branch1
  * branch2
  master
  NONE

# Press enter when done
Switched to branch 'branch1'
```

