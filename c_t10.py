from dsl import *
import c_t10a, c_t10b


def build():
    return topic('Множества, словари', 'множества, операции над ними, словари, подсчёт частот', c_t10a.build() + c_t10b.build())
