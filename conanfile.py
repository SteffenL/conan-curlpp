import os
from conans import ConanFile, CMake, tools

class CurlppConan(ConanFile):
    name = "curlpp"
    version = "0.8.1"
    url = "https://github.com/SteffenL/conan-curlpp"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    license = "Apache-2.0"

    source_dir = "curlpp"

    def source(self):
        git = tools.Git(folder=self.source_dir)
        git.clone("https://github.com/jpbarrette/curlpp.git", "v" + self.version)

    def build(self):
        with tools.chdir(self.source_dir):
            tools.replace_in_file("CMakeLists.txt", "${CMAKE_CURRENT_SOURCE_DIR}/conanbuildinfo.cmake", "${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
            tools.replace_in_file("CMakeLists.txt", "include(FindCURL)", "")
            tools.replace_in_file("CMakeLists.txt", "find_package(CURL REQUIRED)", "")
            tools.replace_in_file("CMakeLists.txt", "message(FATAL_ERROR \"Could not find CURL\")", "")
        cmake = CMake(self)
        cmake.configure(source_dir=self.source_dir)
        cmake.build()

    def package(self):
        self.copy("*.hpp", dst="include", src=os.path.join(self.source_dir, "include"))
        self.copy("*.inl", dst="include", src=os.path.join(self.source_dir, "include"))

        if self.settings.os == "Windows":
            if self.options.shared:
                self.copy("*/curlpp.lib", dst="lib", keep_path=False)
            else:
                self.copy("*/libcurlpp.lib", dst="lib", keep_path=False)

        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so*", dst="lib", keep_path=False)
        self.copy("*.dylib*", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)


    def package_info(self):
        if self.settings.os == "Windows" and not self.options.shared:
            self.cpp_info.libs = ["libcurlpp"]
        else:
            self.cpp_info.libs = ["curlpp"]

    def requirements(self):
        self.requires("libcurl/[>=7.64.1]@bincrafters/stable")
