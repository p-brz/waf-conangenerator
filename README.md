# Waf Conan Generator

A [Conan](https://www.conan.io/) generator to easy the use of [Waf](https://waf.io) build system on conan.


**NOTE**: i am just a fan of *Waf* and *Conan*. I am still learning both.
So any correction, suggestion or contribution is welcome.

## Quickstart

See [quickstart template](https://github.com/paulobrizolara/waf-conangenerator-template)

## How to use

Add the generator on 'requires' section of your conanfile
(see Conan [Getting Started](http://docs.conan.io/en/latest/getting_started.html)
if you do not know Conan yet).
If you want learn how to use Waf, see the [waf-book](https://waf.io/book/).

### Prepare conanfile

In conanfile.txt:

    [requires]
    ...
    WafGenerator/0.0.1@paulobrizolara/experimental

    [generators]
    ...
    Waf

Or if you are using a conanfile.py:

    class YourConanFileClass(ConanFile):
        ...

        requires = (
            ... ,
            "WafGenerator/0.0.1@paulobrizolara/experimental"
        )

        generators = "Waf"

### Install dependencies

Then, install your project:

        $ conan install .

### Prepare wscript

After install, a file 'conanbuildinfo_waf' will be generated (on the path used while installing).
Load this file on your *configure* method (like a module) in your *wscript* file. Example:

        ...
        def configure(conf):
            ...
            conf.load('conanbuildinfo_waf', tooldir=".");

Then, include the dependencies on 'use' argument for each target.
Example:

        def build(bld):
            ...
            bld.program(
                target   = 'exec_name',

                #compile all cpp files below src dir
                source   = bld.path.ant_glob('src/**/*.cpp')),
                includes = ['src'],

                #List here the conan dependencies
                use      = ['Poco', 'OpenSSL'])

**NOTE**: The Conan dependencies on 'use' argument should be the names on conan packages.
That is, for a package 'Abc@X.Y.Z@user/channel', the dependency should be 'Abc'.

## Run build from conan

If you are using a conanfile.py, you can run the build from conan (using 'conan build' command).

To allow that, add a 'build' method on conanfile.py with the below content:

        def build(self):
            import os #this can be put on file start

            # Change the current dir to the conanfile directory
            # (assuming that the 'wscript' file is on this dir)
            os.chdir(self.conanfile_directory)

            # Require the 'waf' file on this directory
            waf = os.path.join(self.conanfile_directory, 'waf')

            # Execute 'waf configure build'
            self.run('%s configure build' % waf)
