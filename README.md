# Waf Conan Generator

A [Conan](https://www.conan.io/) generator to easy the use of [Waf](https://waf.io) build system.

## How to use

Add the generator on 'requires' section of your conanfile
(see Conan [Getting Started](http://docs.conan.io/en/latest/getting_started.html)
if you do not know Conan yet).
If you want learn how to use Waf, see the [waf-book](https://waf.io/book/).

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

Then, install your project:

        $ conan install . --build=missing

The "--build" option is required by now.

After install, a file 'conanbuildinfo_waf' will be generated (on the path used while installing).
Load this file on your *configure* method (like a module) in your *wscript* file. Example:

        ...
        def configure(conf):
            ...
            conf.load('conanbuildinfo_waf', tooldir=".");
