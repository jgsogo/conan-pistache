from conans import ConanFile, CMake, tools
from conans.errors import ConanException


class PistacheConan(ConanFile):
    name = "pistache"
    version = "master"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Pistache here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    @property
    def src_folder(self):
        return "{}-{}".format(self.name, self.version)

    def configure(self):
        if self.settings.compiler == 'gcc' and float(self.settings.compiler.version.value) >= 5.1:
            if self.settings.compiler.libcxx != 'libstdc++11':
                raise ConanException("You must use the setting compiler.libcxx=libstdc++11")

    def source(self):
        git = tools.Git(folder=self.src_folder)
        git.clone("https://github.com/oktal/pistache.git", "master")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["PISTACHE_BUILD_TESTS"] = False
        cmake.definitions["PISTACHE_BUILD_EXAMPLES"] = True
        cmake.configure(source_folder=self.src_folder)
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.definitions["PISTACHE_BUILD_TESTS"] = False
        cmake.definitions["PISTACHE_BUILD_EXAMPLES"] = False
        cmake.configure(source_folder=self.src_folder)
        cmake.install()

    def package_info(self):
        self.cpp_info.includedirs = ['include', ]
        self.cpp_info.libs = ["pistache", ]

        if not self.settings.os == "Windows":
            self.cpp_info.cppflags = ["-pthread"]

