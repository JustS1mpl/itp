import importlib
def build():
    # v7: список тем пишется заново (см. docs/CURRICULUM.md); пока только временная заглушка
    stub = importlib.import_module('c_stub')
    return [stub.build_intro(), stub.build()]
