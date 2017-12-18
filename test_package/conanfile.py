from conans import ConanFile, tools


class TestFindWindowsSigntool(ConanFile):
    settings = {"os": ["Windows"], "arch": ["x86", "x86_64"]}
        
    def test(self):
        with tools.pythonpath(self):
            from find_windows_signtool import find_signtool
            signtool = find_signtool(str(self.settings.arch))
            self.output.info("signtool path: %s" % signtool)
