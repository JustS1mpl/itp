import importlib
def build():
    mods = ['c_intro', 'c_t1', 'c_t2', 'c_t3', 'c_t4', 'c_t5', 'c_t6', 'c_t7', 'c_t8', 'c_t9', 'c_t10', 'c_t11', 'c_t12', 'c_t13', 'c_t14', 'c_t15', 'c_t16', 'c_t17', 'c_t18', 'c_t19', 'c_t20', 'c_t21']
    out = []
    for m in mods:
        out.append(importlib.import_module(m).build())
    import post
    post.apply(out)
    out.insert(9, importlib.import_module('c_tur').build())   # доп. глава «Черепаха»: между темами 8 и 9
    return out
