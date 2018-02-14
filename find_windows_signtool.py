import winreg
import os


from conans.errors import ConanException


def get_winsdk_bin_pathes():
    ret = []
    hk = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "Software\\Microsoft\\Windows Kits\\Installed Roots")
    # Find SDK 8.x
    for key in ["KitsRoot", "KitsRoot81"]:
        try:
            p = winreg.QueryValueEx(hk, key)[0]
            p = os.path.join(p, "bin")
            ret.append(p)
        except WindowsError:
            continue
    # Find SDK 10
    try:
        p10 = winreg.QueryValueEx(hk, "KitsRoot10")[0]
        i = 0
        while True:
            try:
                ver = winreg.EnumKey(hk, i)
                p = os.path.join(p10, "bin", ver)
                ret.append(p)
                i += 1
            except:
                break
    except:
        pass
    return ret[::-1]

def find_signtool(arch):
    if arch == "x86_64":
        arch = "x64"
    for winsdk_path in get_winsdk_bin_pathes():
        signtool = os.path.join(winsdk_path, arch, "signtool.exe")
        if os.path.isfile(signtool):
            return signtool
    raise ConanException("Can`t find signtool.exe!")
