from conans import ConanFile


class FindWindowsSigntool(ConanFile):
    name = "find_windows_signtool"
    version = "1.0"
    license = "MIT"
    url = "https://github.com/odant/conan-find_windows_signtool"
    description = "Python module for find path Microsoft signtool"
    settings = {"os": ["Windows"]}
    exports = "*"
    build_policy = "missing"
    
    def package(self):
        self.copy("*.py")
        
    def package_info(self):
        self.env_info.PYTHONPATH.append(self.package_folder)
