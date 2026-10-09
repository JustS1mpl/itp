from dsl import *
import c_t9a, c_t9b, c_t9c, c_t9d


def build():
    items = c_t9a.build() + c_t9b.build() + c_t9c.build() + c_t9d.build()
    return topic('Строки, кортежи, списки', 'индексы, срезы, методы, списки, кортежи, стек', items)
