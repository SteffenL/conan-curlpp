import os

from conans import ConanFile, CMake

class CurlppTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy('*.so', dst='bin', src='lib')

    def test(self):
        os.chdir("bin")
        self.run(".%sexample" % os.sep)
