from distutils.core import setup
from distutils.command.install import install as _install

import os
import sys
from subprocess import call


def get_data_files(input_dir, output_dir):
    result = []
    for root, dirs, files in os.walk(input_dir) :
        da_files = []
        for f in files :
            da_files.append(os.path.join(root,f))
        result.append((os.sep.join([output_dir]+root.split(os.sep)[1:]),da_files))
    return result

these_files = get_data_files("data/cmake", "EuclidEnv")
these_files += get_data_files("data/texmf", "EuclidEnv")

skip_install_fix=False

# disable the postinstall script if needed. This is especially needed for the RPM
# creation. In that case the postinstall is done by the RPM spec file.
for a in sys.argv: 
    if a.startswith("--skip-install-fix") :
        skip_install_fix = True
        sys.argv.remove(a)



class my_install(_install):
    def run(self):
        _install.run(self)
        # postinstall
        if not skip_install_fix :
            # print "This is the install base %s" % self.install_base
            # print "This is the install platbase %s" % self.install_platbase
            # print "This is the install root %s" % self.root
            # print "This is the install purelib %s" % self.install_purelib
            # print "This is the install platlib %s" % self.install_platlib
            # print "This is the install lib %s" % self.install_lib
            # print "This is the install headers %s" % self.install_headers
            # print "This is the install scripts %s" % self.install_scripts
            # print "This is the install data %s" % self.install_data

            if os.path.exists(os.path.join(self.install_scripts, "FixInstallPath")) :
                fixscript = os.path.join(self.install_scripts, "FixInstallPath")
                proc_list = []
                for c in [ "ELogin", "Euclid_group_login", "Euclid_group_setup" ]  :
                    for s in ["sh" , "csh"] :
                        file2fix = os.path.join(self.install_scripts, "%s.%s" % (c,s) )
                        if os.path.exists(file2fix) :
                            proc_list.append(file2fix)
                file2fix = os.path.join(self.install_lib, "Euclid", "Login.py")
                if os.path.exists(file2fix) :
                    proc_list.append(file2fix)
            for p in proc_list : 
                print "Fixing %s with the %s prefix path" % (p, self.install_base)
                call(["python", fixscript, self.install_base, p])
                

setup (name="EuclidEnv",
       version="1.2.2",
       description="Euclid Environment Scripts",
       author="Hubert Degaudenzi",
       author_email="Hubert.Degaudenzi@unige.ch",
       url="http://www.isdc.unige.ch/redmine/projects/euclidenv",
       package_dir={"":"python"},
       packages = ["Euclid", "Euclid.Run"],
       scripts  = [ os.path.join("scripts","ELogin.sh"),
                    os.path.join("scripts","ELogin.csh"),
                    os.path.join("scripts", "Euclid_config.sh"),
                    os.path.join("scripts", "Euclid_config.csh"),
                    os.path.join("scripts", "Euclid_group_login.sh"),
                    os.path.join("scripts", "Euclid_group_login.csh"),
                    os.path.join("scripts", "Euclid_group_setup.sh"),
                    os.path.join("scripts", "Euclid_group_setup.csh"),
                    os.path.join("scripts", "runpy"),
                    os.path.join("scripts", "StripPath.csh"),
                    os.path.join("scripts", "StripPath.sh"),
                    os.path.join("scripts", "WhereAmI"),
                    os.path.join("scripts", "ERun"),
                    os.path.join("scripts", "E-Run"),
                    os.path.join("scripts", "FixInstallPath"),
                  ],
       data_files = [("/etc/profile.d", [os.path.join("data", "profile", "euclid.sh"),
                                         os.path.join("data", "profile", "euclid.csh")]),
                     ("/etc/sysconfig", [os.path.join("data", "sys", "config", "euclid")])
                     ] + these_files,
       cmdclass={"install": my_install},
       )
