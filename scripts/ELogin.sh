# main login script for the Euclid environment

my_own_prefix="%(this_install_prefix)s"
python_loc=`python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(prefix='$my_own_prefix'))"`

if [[ -r ${python_loc}/Euclid/Login.py ]]; then
  ELogin_tmpfile=`python ${python_loc}/Euclid/Login.py --shell=sh --mktemp "$@"`
  ELoginStatus="$?"  
else
  ELogin_tmpfile=`python -m Euclid.Login --shell=sh --mktemp "$@"`
  ELoginStatus="$?"
fi

unset my_own_prefix
unset python_loc

needs_cleanup=no

if [[ "$ELoginStatus" = 0 && -n "$ELogin_tmpfile" ]]; then
  . $ELogin_tmpfile
  needs_cleanup=yes
fi

rm -f $ELogin_tmpfile
unset ELogin_tmpfile

if [[ "$needs_cleanup" = "yes" ]]; then
  if [[ "x$E_NO_STRIP_PATH" ==  "x" ]] ; then

    if [[ -r ${my_own_prefix}/bin/StripPath.sh ]]; then
      stripscr=${my_own_prefix}/bin/StripPath.sh
    else
      stripscr=`/usr/bin/which StripPath.sh`
    fi
    . ${stripscr}

    unset stripscr

  fi
fi

unset needs_cleanup

$(exit $ELoginStatus)
