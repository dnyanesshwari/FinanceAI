import pkgutil
import langchain

print("version", langchain.__version__)
print("submodules:")
for m in pkgutil.iter_modules(langchain.__path__):
    print(" -", m.name)
