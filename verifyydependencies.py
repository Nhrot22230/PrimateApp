import subprocess

def is_installed(library):
  try:
    __import__(library)
    return True
  except ImportError:
    return False

libraries = [
    "tk",
    "ttkthemes",
    "pandas",
    "numpy",
    "os",
    "librosa",
    "soundfile",
    "matplotlib",
    "tensorflow",
    "tensorflow-io",
    "io",
]

def is_windows():
  import platform
  return platform.system() == "Windows"

def install_dependencies():
  for library in libraries:
    if not is_installed(library):
       print(f"Installing {library}...")
       subprocess.run(["pip", "install", library])
    else:
        print(f"{library} is already installed.")
        
  print("Installation complete!")


if __name__ == "__main__":
    install_dependencies()